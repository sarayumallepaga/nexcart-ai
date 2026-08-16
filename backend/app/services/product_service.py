from fastapi import HTTPException


from app.repositories.product_repository import (
    get_all_products as repo_get_all_products,
    get_product_by_id,
    get_products_by_category,
)

from app.schemas.product_schema import (
    product_serializer,
    products_serializer,
)
from datetime import datetime

from app.repositories.recently_viewed_repository import (
    add_recently_viewed,
)


def get_all_products():
    products = repo_get_all_products()
    return products_serializer(products)


def get_product(product_id: str, email=None):
    product = get_product_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    # Save recently viewed product
    if email:
        add_recently_viewed(
            {
                "user_email": email,
                "product_id": (product_id),
                "viewed_at": datetime.utcnow(),
            }
        )

    return product_serializer(product)


def get_similar_products(product_id: str):
    # Get selected product
    product = get_product_by_id((product_id))

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    category = product["category"]
    price = product["price"]

    # Get all products in same category
    all_products = get_products_by_category(category)

    similar_products = []

    for item in all_products:
        if (
            item["id"] != (product_id)
            and abs(item["price"] - price) <= 50000
        ):
            similar_products.append(item)

    return products_serializer(similar_products)