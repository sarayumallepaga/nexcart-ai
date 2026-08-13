from fastapi import APIRouter, HTTPException

from app.schemas.product import Product
from app.services.product_service import get_product_by_id

router = APIRouter()


@router.get("/product/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = get_product_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product