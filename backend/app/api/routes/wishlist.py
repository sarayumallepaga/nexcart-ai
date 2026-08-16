from fastapi import APIRouter, Depends

from app.schemas.wishlist import WishlistRequest
from app.security.oauth2 import get_current_user
from app.services.wishlist_service import (
    add_product,
    view_wishlist,
    delete_product,
)

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.post("/{product_id}")
def add(
    product_id: int,
    current_user=Depends(get_current_user),
):
    return add_product(
        current_user["email"],
        product_id,
    )


@router.get("/")
def get(
    current_user=Depends(get_current_user),
):
    return view_wishlist(
        current_user["email"],
    )


@router.delete("/{product_id}")
def delete(
    product_id: int,
    current_user=Depends(get_current_user),
):
    return delete_product(
        current_user["email"],
        product_id,
    )