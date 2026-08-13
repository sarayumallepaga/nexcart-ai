from fastapi import APIRouter

from app.services.product_service import (
    get_all_products,
    get_product,
)

router = APIRouter()


@router.get("/products")
def all_products():
    return get_all_products()


@router.get("/products/{product_id}")
def product(product_id: str):
    return get_product(product_id)