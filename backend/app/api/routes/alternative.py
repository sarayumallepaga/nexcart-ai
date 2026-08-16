from fastapi import APIRouter

from app.schemas.alternative_request import AlternativeRequest
from app.services.alternative_service import recommend_alternatives

router = APIRouter()


@router.post("/recommend-alternatives")
def alternatives(request: AlternativeRequest):
    return recommend_alternatives(request.product_id)