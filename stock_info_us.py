import os
import FinanceDataReader as fdr
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, date

#script명
script_name = os.path.basename(__file__)

# 오늘
run_date = date.today()

# 시간 측정
start = datetime.now()

# DB 연결
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="tteoksang",
    user="leeroot",
    password=""
)
# 주식 정보 가져오기
us_market = ["NASDAQ", "NYSE", "AMEX"]

for market in us_market:
    cur = conn.cursor()

    # DB 데이터 확인
    cur.execute(
        "SELECT stock_id FROM stock WHERE nation_type = %s AND market = %s;",
        ("미국", market)
    )
    db_stocks_id = set(row[0] for row in cur.fetchall())

    fdr_stock_us = fdr.StockListing(market)
    fdr_stocks_id = set(fdr_stock_us['Symbol'].tolist())

    #상폐 종목 삭제
    delete_stocks_id = db_stocks_id - fdr_stocks_id

    if delete_stocks_id:
        execute_values(
            cur,
            "delete from stock where stock_id in %s",
            [(tuple(delete_stocks_id))]
        )

    # 주식 정보 저장
    filtered_df = fdr_stock_us[fdr_stock_us['Industry'] != '폐쇄형 펀드']

    stock_list = [
        (
            row['Symbol'],
            "미국",  # 'Nation' 컬럼이 없으면 아래 참고
            market,
            row['Name'],
            datetime.now()
        )
        for _, row in filtered_df.iterrows()
    ]

    insert_stock_us_query = """
        insert into stock (stock_id, nation_type, market, stock_name, created_at)
        values %s
        on conflict (stock_id) do update set
        nation_type = EXCLUDED.nation_type,
        market = EXCLUDED.market,
        stock_name = EXCLUDED.stock_name,
        updated_at = NOW();
    """

    execute_values(cur, insert_stock_us_query, stock_list)
    conn.commit()

# 종료
end = datetime.now()
# 소요 시간
duration = (end - start).total_seconds()

insert_stock_ingest_log_query = """
    insert into data_ingest_duration_log (run_date, script_name, start_time, end_time, duration)
    values (%s, %s, %s, %s, %s)
"""
cur.execute(insert_stock_ingest_log_query, (run_date, script_name, start, end, duration))

# 종료
conn.commit()
cur.close()
conn.close()




