from fastapi import APIRouter

from app.services.price_service import (
    fetch_price_history,
    predict_price,
)

router = APIRouter()


@router.get("/price-history/{product_id}")
def price_history(product_id: int):
    return fetch_price_history(product_id)


@router.get("/price-prediction/{product_id}")
def price_prediction(product_id: int):
    return predict_price(product_id)