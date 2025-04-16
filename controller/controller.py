from fastapi import APIRouter
from service.krx_stock_info import KRXStockService

router = APIRouter()
krx_stock_service = KRXStockService()

@router.post("/update-stock-kr")
def update_stock_kr():
    try:
        # 1. KRX 데이터 수집 및 가공
        info, trade_info = krx_stock_service.fetch_and_process()

        # 2. PostgreSQL에 저장
        krx_stock_service.save_to_postgres(info, trade_info)

        return {"status": "success", "message": "KRX 주식 정보가 성공적으로 업데이트되었습니다."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
