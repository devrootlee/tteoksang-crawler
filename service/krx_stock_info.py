import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from psycopg2.extras import execute_values
from db.db_connection import db_connection

class KRXStockService:
    def __init__(self):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.expand_frame_repr', False)

        self.today = datetime.today().date()
        self.now = datetime.now()
        self.start_52w = self.today - timedelta(days=365)

    # 메인 함수
    def fetch_and_process(self):
        script_name = "krx_stock_info.py"
        start_time = datetime.now()
        status = "SUCCESS"

        try:
            marketList = ["KOSPI", "KOSDAQ", "KONEX"]
            for market in marketList:
                stock_list = fdr.StockListing(market)

                stock_codes = []
                stock_meta = {}
                krx_stock_info = []
                krx_stock_trade_info = []

                for _, stock in stock_list.iterrows():
                    stock_id = stock['Code']
                    stock_codes.append(stock_id)
                    stock_meta[stock_id] = {
                        "market": market,
                        "stock_name": stock['Name'],
                        "capacity": stock['Marcap'],
                        "close_price": stock['Close'],
                        "change_rate": stock['ChagesRatio'],
                        "open_price": stock['Open'],
                        "high_price": stock['High'],
                        "low_price": stock['Low'],
                        "volume": stock['Volume'],
                        "amount": stock['Amount'],
                    }

                results = {}
                with ThreadPoolExecutor(max_workers=10) as executor:
                    futures = {executor.submit(self.get_stock_52week_high_low, code): code for code in stock_codes}
                    for future in as_completed(futures):
                        code = futures[future]
                        try:
                            stock_id, high, low = future.result()
                            results[stock_id] = (high, low)
                        except Exception as e:
                            print(f"Error with {code}: {e}")
                            results[code] = (None, None)

                for stock_id in stock_codes:
                    meta = stock_meta[stock_id]
                    high_52w, low_52w = results.get(stock_id, (None, None))

                    krx_stock_info.append({
                        "stock_id": stock_id,
                        "market": meta['market'],
                        "stock_name": meta['stock_name'],
                        "created_at": self.now
                    })

                    krx_stock_trade_info.append({
                        "stock_id": stock_id,
                        "trade_date": self.today,
                        "close_price": meta['close_price'],
                        "change_rate": meta['change_rate'],
                        "open_price": meta['open_price'],
                        "high_price": meta['high_price'],
                        "low_price": meta['low_price'],
                        "high_52_week_price": int(high_52w) if high_52w is not None else None,
                        "low_52_week_price": int(low_52w) if low_52w is not None else None,
                        "volume": meta['volume'],
                        "amount": meta['amount'],
                        "capacity": meta['capacity'],
                        "created_at": self.now
                    })
                self.save_krx_stock(krx_stock_info, krx_stock_trade_info)

        except Exception as e:
            status = f"FAILED: {e}"
            print(f"❌ 데이터 수집 중 오류 발생: {e}")

        finally:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            self.save_log(script_name, start_time, end_time, duration, status)

    # 52주 최고가 ,최저가 구하는 함수
    def get_stock_52week_high_low(self, stock_code):
        df = fdr.DataReader(stock_code, self.start_52w, self.today)
        if df.empty:
            return stock_code, None, None
        high = df[df['High'] != 0]['High'].max() if not df.empty else None
        low = df[df['Low'] != 0]['Low'].min() if not df.empty else None
        return stock_code, high, low

    # krx stock 저장 함수
    def save_krx_stock(self, krx_stock_info, krx_stock_trade_info):
        try:
            with db_connection() as conn:
                with conn.cursor() as cur:
                    values1 = [
                        (
                            item['stock_id'],
                            item['market'],
                            item['stock_name'],
                            item['created_at']
                        ) for item in krx_stock_info
                    ]
                    sql1 = """
                        INSERT INTO kr_stock_info (stock_id, market, stock_name, created_at)
                        VALUES %s
                        ON CONFLICT (stock_id) DO UPDATE SET
                        market = EXCLUDED.market,
                        updated_at = NOW()
                    """
                    execute_values(cur, sql1, values1)

                    values2 = [
                        (
                            item['stock_id'],
                            item['trade_date'],
                            item['close_price'],
                            item['change_rate'],
                            item['open_price'],
                            item['high_price'],
                            item['low_price'],
                            item['high_52_week_price'],
                            item['low_52_week_price'],
                            item['volume'],
                            item['amount'],
                            item['capacity'],
                            item['created_at']
                        ) for item in krx_stock_trade_info
                    ]
                    sql2 = """
                        INSERT INTO kr_stock_trade_info (
                            stock_id, trade_date, close_price, change_rate,
                            open_price, high_price, low_price,
                            high_52_week_price, low_52_week_price,
                            volume, amount, capacity, created_at
                        ) VALUES %s
                        ON CONFLICT (stock_id) DO UPDATE SET
                        trade_date = EXCLUDED.trade_date,
                        close_price = EXCLUDED.close_price,
                        change_rate = EXCLUDED.change_rate,
                        open_price = EXCLUDED.open_price,
                        high_price = EXCLUDED.high_price,
                        low_price = EXCLUDED.low_price,
                        high_52_week_price = EXCLUDED.high_52_week_price,
                        low_52_week_price = EXCLUDED.low_52_week_price,
                        volume = EXCLUDED.volume,
                        amount = EXCLUDED.amount,
                        capacity = EXCLUDED.capacity,                     
                        updated_at = NOW()
                    """
                    execute_values(cur, sql2, values2)

                conn.commit()
                print("✅ 데이터 저장 완료")
        except Exception as e:
            print(f"❌ DB 저장 오류: {e}")

    # 데이터 수집 로그 저장 함수
    def save_log(self, script_name, start_time, end_time, duration, status):
        try:
            with db_connection() as conn:
                with conn.cursor() as cur:
                    sql = """
                        INSERT INTO data_ingest_log (
                            ingest_date, script_name, start_time, end_time, duration, status
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cur.execute(sql, (
                        start_time.date(),
                        script_name,
                        start_time,
                        end_time,
                        duration,
                        status
                    ))
                conn.commit()
                print("📝 수집 로그 저장 완료")
        except Exception as e:
            print(f"❌ 수집 로그 저장 실패: {e}")