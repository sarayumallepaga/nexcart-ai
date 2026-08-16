from fastapi import APIRouter

from app.schemas.buy_advice import BuyAdviceRequest
from app.services.buy_advice_service import get_buy_advice

router = APIRouter()


@router.post("/buy-advice")
def buy_advice(request: BuyAdviceRequest):
    return get_buy_advice(request.product_id)