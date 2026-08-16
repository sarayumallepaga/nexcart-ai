from fastapi import HTTPException

from app.repositories.recommendation_repository import (
    get_product_by_id,
    get_products_by_category,
)
from app.schemas.product_schema import (
    product_serializer,
)


def get_recommendations(product_id: int):
    # Get selected product
    product = get_product_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    category = product["category"]
    price = product["price"]
    brand = product["brand"]

    # Get products in same category
    products = get_products_by_category(category)

    recommendations = []

    for p in products:
        if p["id"] == product_id:
            continue

        score = 0

        # Same category
        score += 50

        # Same brand
        if p["brand"] == brand:
            score += 20

        # Similar price (within ₹20,000)
        if abs(p["price"] - price) <= 20000:
            score += 15

        # High rating
        if p["rating"] >= 4.5:
            score += 10

        recommendations.append({
            "score": score,
            "product": product_serializer(p)
        })

    # Highest score first
    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # Return Top 5
    return recommendations[:5]