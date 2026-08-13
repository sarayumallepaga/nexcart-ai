from fastapi import HTTPException

from app.database.products import products


def compare_products(product_ids: list[int]):
    selected_products = []

    # Find products by ID
    for product_id in product_ids:
        product = next(
            (p for p in products if p["id"] == product_id),
            None
        )

        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID {product_id} not found"
            )

        selected_products.append(product)

    # For Sprint 3, compare only two products
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