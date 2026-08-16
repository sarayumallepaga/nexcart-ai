from fastapi import HTTPException
from app.database.mongodb import db
from app.repositories.product_repository import get_product_by_id
from datetime import datetime
from app.repositories.wishlist_repository import (
    add_to_wishlist,
    get_user_wishlist,
    remove_from_wishlist,
    already_exists,
)

def add_product(email: str, product_id: int):

    product = get_product_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    if already_exists(email, product_id):
        raise HTTPException(
            status_code=400,
            detail="Product already in wishlist",
        )

    add_to_wishlist(
       {
    "user_email": email,
    "product_id": product_id,
    "added_at": datetime.utcnow(),
}
    )

    return {
        "message": "Added to wishlist"
    }


def view_wishlist(email: str):

    wishlist = get_user_wishlist(email)

    product_ids = [
        item["product_id"]
        for item in wishlist
    ]

    products = list(
        db["products"].find(
            {
                "id": {
                    "$in": product_ids
                }
            },
            {
                "_id": 0
            }
        )
    )

    return products


def delete_product(email: str, product_id: int):

    result = remove_from_wishlist(
        email,
        product_id,
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Product not found in wishlist",
        )

    return {
        "message": "Removed from wishlist"
    }