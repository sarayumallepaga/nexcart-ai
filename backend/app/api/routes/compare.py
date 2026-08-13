from fastapi import APIRouter

from app.schemas.compare import CompareRequest, ComparisonResponse
from app.services.compare_service import compare_products

router = APIRouter()


@router.post("/compare", response_model=ComparisonResponse)
def compare(request: CompareRequest):
    return compare_products(request.product_ids)