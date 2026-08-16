from fastapi import HTTPException

from app.repositories.price_repository import (
    get_product_by_id,
    get_price_history,
)


def fetch_price_history(product_id: int):
    product = get_product_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return {
        "product_id": product["id"],
        "product_name": product["name"],
        "current_price": product["price"],
        "price_history": get_price_history(product_id),
    }


def predict_price(product_id: int):
    product = get_product_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    history = get_price_history(product_id)

    if len(history) < 2:
        return {
            "prediction": "Not enough price history available.",
            "trend": "Unknown",
        }

    first_price = history[0]["price"]
    last_price = history[-1]["price"]

    if last_price < first_price:
        trend = "Decreasing"
        prediction = (
            "Price is trending downward. It may decrease further."
        )
    elif last_price > first_price:
        trend = "Increasing"
        prediction = (
            "Price is trending upward. Buying now may be better."
        )
    else:
        trend = "Stable"
        prediction = (
            "Price has remained stable."
        )

    return {
        "product_id": product["id"],
        "product_name": product["name"],
        "current_price": product["price"],
        "trend": trend,
        "prediction": prediction,
        "price_history": history,
    }