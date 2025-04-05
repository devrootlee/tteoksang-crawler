from fastapi import FastAPI
from controller.controller import router  # 라우터 임포트

app = FastAPI(
    title="Stock Data API",
    description="한국/미국 주식 데이터를 업데이트하는 API",
    version="1.0.0"
)

# 라우터 등록
app.include_router(router, prefix="/api/stocks")