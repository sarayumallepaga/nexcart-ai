from typing import List, Optional

from fastapi import APIRouter

from app.schemas.product import Product
from app.services.search_service import search_products

router = APIRouter()


@router.get("/search", response_model=List[Product])
def search(
    q: str = "",
    brand: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    min_rating: Optional[float] = None,
):
    return search_products(
        q,
        brand,
        category,
        min_price,
        max_price,
        min_rating,
    )