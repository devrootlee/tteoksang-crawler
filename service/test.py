import pandas as pd
import FinanceDataReader as fdr

# 출력 옵션 설정 (행/열 모두 보기)
pd.set_option('display.max_rows', None)  # 모든 행 출력
pd.set_option('display.max_columns', None)  # 모든 열 출력
pd.set_option('display.width', None)  # 너비 제한 없음
pd.set_option('display.max_colwidth', None)  # 열 내용 길이 제한 없음


# fdr_stock_kr = fdr.StockListing('NASDAQ')
# fdr.DataReader('NAVER:000100', '2023')
print(fdr.DataReader('NAVER:000100', '2023'))