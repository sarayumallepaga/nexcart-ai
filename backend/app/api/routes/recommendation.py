from fastapi import APIRouter

from app.services.recommendation_service import get_recommendations

router = APIRouter()


@router.get("/recommendations/{product_id}")
def recommendations(product_id: int):
    return get_recommendations(product_id)