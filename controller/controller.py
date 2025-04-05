from fastapi import APIRouter
from service.stock_info import stockInfoService

router = APIRouter()
stock_service = stockInfoService()

@router.post("/update-stock-kr")
def update_stock_kr():
    try:
        result = stock_service.update_stock_kr()
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/update-stock-us")
def update_stock_us():
    try:
        result = stock_service.update_stock_us()
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}