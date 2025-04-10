# 떡상🚀🚀(주식 예측 서비스) - 크롤러
* [FinanceDataReader github](https://github.com/FinanceData/FinanceDataReader)
위 깃허브를 참고하여 만들었다.

- 한국 전체 주식 수집
fdr.StockListing('KRX') 는 한국거래소(KOSPI, KOSDAQ, KONEX)에서 거래되고 있는 모든 종목의 주식을 가져온다.
여기서 Code와 Name 만 필요해서 해당 데이터만 수집하였다.
  - 전체 코드: [stock_info.py(def update_stock_kr)](service/stock_info.py)
  - 핵심 코드: fdr_stock_kr = fdr.StockListing('KRX')
  - 응답: 
```
        Code        ISU_CD            Name         Market             Dept    Close ChangeCode  Changes  ChagesRatio     Open     High      Low    Volume         Amount           Marcap      Stocks MarketId
0     005930  KR7005930003            삼성전자          KOSPI                     56100          2    -1500        -2.60    56200    58200    55700  23527139  1330710237050  332091687424200  5919637922      STK
1     000660  KR7000660001          SK하이닉스          KOSPI                    182200          2   -12400        -6.37   187900   189600   178400   9182017  1685984859300  132642030903000   728002365      STK
```

- 미국 전체 주식 수집
fdr.StockListing('NASDAQ') 는 NASDAQ 에서 거래되고 있는 모든 종목의 주식을 가져온다. NYSE 나 AMEX 주식도 가져오고 싶다면 fdr.StockListing('NYSE') 이런식으로 변경해주면 된다.
데이터 출력이 한국 주식 데이터와 다르며 여기서 Symbol과 Name 만 필요해서 해당 데이터만 수집하였다.
  - 전체 코드: [stock_info.py(def update_stock_us)](service/stock_info.py)
  - 핵심 코드: fdr_stock_kr = fdr.StockListing('NASDAQ')
  - 응답:
```
     Symbol         Name            IndustryCode        Industry
0      AAPL        Apple Inc         57106020          전화 및 소형 장치
1      MSFT       Microsoft Corp     57201020           소프트웨어
```

- 기능
  - 수동 동기화(Fast API)
    - 한국 주식 수동 동기화: [POST]/api/stocks/update-stock-kr
    - 미국 주식 수동 동기화: [POST]/api/stocks/update-stock-us