from controller.controller import router  # 라우터 임포트
from fastapi import FastAPI

app = FastAPI(
    title="Stock Data API",
    description="주식 데이터 수집 API",
    version="1.0.0"
)

# 라우터 등록
app.include_router(router, prefix="")