# 떡상🚀🚀(주식 예측 서비스) - 크롤러
* [FinanceDataReader github](https://github.com/FinanceData/FinanceDataReader)
위 깃허브를 참고하여 구축

- 한국 전체 주식 수집

fdr.StockListing("시장"): 한국거래소(KOSPI, KOSDAQ, KONEX)에서 거래되고 있는 모든 종목의 주식을 가져온다.
  - 응답 예시: 
```
        Code        ISU_CD            Name         Market             Dept    Close ChangeCode  Changes  ChagesRatio     Open     High      Low    Volume         Amount           Marcap      Stocks MarketId
0     005930  KR7005930003            삼성전자          KOSPI                     56100          2    -1500        -2.60    56200    58200    55700  23527139  1330710237050  332091687424200  5919637922      STK
1     000660  KR7000660001          SK하이닉스          KOSPI                    182200          2   -12400        -6.37   187900   189600   178400   9182017  1685984859300  132642030903000   728002365      STK
```

fdr.DataReader("종목코드", "시작일", "종료일"): 지정한 기간(시작일~종료일) 동안의 주식 데이터를 조회하며, 시가(Open), 고가(High), 저가(Low), 종가(Close), 거래량(Volume), 변동(Change)을 포함하여 반환한다.
  - 응답 예시: 
```
  Date        Open   High    Low  Close    Volume    Change                                                      
0 2025-04-15  56300  57100  56200  56600   8998640  0.007117
1 2025-04-16  56000  56200  54500  54700  14411942 -0.033569
```

  - 참고 코드
    - [krx_stock_info.py](service/krx_stock_info.py)

  - 기능
    - 수동 동기화(Fast API)
      - 한국 주식 수동 동기화: [POST]/api/stocks/update-stock-kr