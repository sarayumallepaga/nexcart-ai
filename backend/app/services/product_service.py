from fastapi import HTTPException

from app.database.mongodb import products_collection
from app.schemas.product_schema import (
    product_serializer,
    products_serializer,
)


def get_all_products():
    products = products_collection.find()
    return products_serializer(products)


def get_product(product_id: str):
    product = products_collection.find_one({"id": int(product_id)})

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product_serializer(product)