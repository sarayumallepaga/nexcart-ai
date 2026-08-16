from fastapi import APIRouter, Depends

from app.security.oauth2 import get_current_user

from app.services.product_service import (
    get_all_products,
    get_product,
    get_similar_products,
)

router = APIRouter()


@router.get("/products")
def all_products(current_user=Depends(get_current_user)):
    return get_all_products()


@router.get("/products/{product_id}")
def product(
    product_id: str,
    current_user=Depends(get_current_user),
):
    return get_product(
        product_id,
        current_user["email"],
    )


@router.get("/products/similar/{product_id}")
def similar_products(
    product_id: str,
    current_user=Depends(get_current_user),
):
    return get_similar_products(product_id)