from fastapi import APIRouter, HTTPException

from app.database.mongodb import products_collection
from app.schemas.compare import CompareRequest
from app.schemas.product_schema import product_serializer
from app.services.ai_compare_service import compare_with_ai

router = APIRouter()


@router.post("/compare-ai")
def compare_ai(request: CompareRequest):

    product1 = products_collection.find_one(
        {"id": request.product_ids[0]}
    )

    product2 = products_collection.find_one(
        {"id": request.product_ids[1]}
    )

    if product1 is None or product2 is None:
        raise HTTPException(
            status_code=404,
            detail="One or both products not found."
        )

    result = compare_with_ai(
        product_serializer(product1),
        product_serializer(product2),
    )

    return {
        "comparison": result
    }