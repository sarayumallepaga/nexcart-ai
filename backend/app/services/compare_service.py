from fastapi import HTTPException

from app.database.mongodb import products_collection
from app.schemas.product_schema import product_serializer


def compare_products(product_ids: list[int]):
    selected_products = []

    # Fetch products from MongoDB
    for product_id in product_ids:
        product = products_collection.find_one({"id": product_id})

        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID {product_id} not found"
            )

        selected_products.append(product_serializer(product))

    # Compare only two products
    if len(selected_products) != 2:
        raise HTTPException(
            status_code=400,
            detail="Please provide exactly two product IDs."
        )

    product1, product2 = selected_products

    cheaper_product = (
        product1["name"]
        if product1["price"] < product2["price"]
        else product2["name"]
    )

    higher_rated_product = (
        product1["name"]
        if product1["rating"] > product2["rating"]
        else product2["name"]
    )

    return {
        "products": selected_products,
        "cheaper_product": cheaper_product,
        "higher_rated_product": higher_rated_product,
    }