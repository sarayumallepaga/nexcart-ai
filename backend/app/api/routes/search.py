from typing import List, Optional

from fastapi import APIRouter, Depends
from app.security.oauth2 import get_current_user
from app.schemas.product import Product
from app.services.search_service import (
    search_products,
    view_search_history,
)

router = APIRouter()


@router.get("/search", response_model=List[Product])
def search(
    q: str = "",
    brand: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    min_rating: Optional[float] = None,
    current_user=Depends(get_current_user),
):
    return search_products(
        current_user["email"],
        q,
        brand,
        category,
        min_price,
        max_price,
        min_rating,
    )


@router.get("/history")
def history(
    current_user=Depends(get_current_user),
):
    return view_search_history(
        current_user["email"]
    )