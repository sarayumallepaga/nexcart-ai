from datetime import datetime

from app.database.mongodb import products_collection
from app.schemas.product_schema import products_serializer

from app.repositories.search_repository import (
    save_search,
    get_user_searches,
)


def search_products(
    email=None,
    query="",
    brand=None,
    category=None,
    min_price=None,
    max_price=None,
    min_rating=None,
):
    # Automatically save search history
    if email and query:
        save_search(
            {
                "user_email": email,
                "query": query,
                "searched_at": datetime.utcnow(),
            }
        )

    mongo_query = {}

    # Search by name, brand or category
    if query:
        mongo_query["$or"] = [
            {
                "name": {
                    "$regex": query,
                    "$options": "i",
                }
            },
            {
                "brand": {
                    "$regex": query,
                    "$options": "i",
                }
            },
            {
                "category": {
                    "$regex": query,
                    "$options": "i",
                }
            },
        ]

    # Brand filter
    if brand:
        mongo_query["brand"] = {
            "$regex": f"^{brand}$",
            "$options": "i",
        }

    # Category filter
    if category:
        mongo_query["category"] = {
            "$regex": f"^{category}$",
            "$options": "i",
        }

    # Price filter
    if min_price is not None or max_price is not None:

        mongo_query["price"] = {}

        if min_price is not None:
            mongo_query["price"]["$gte"] = min_price

        if max_price is not None:
            mongo_query["price"]["$lte"] = max_price

    # Rating filter
    if min_rating is not None:
        mongo_query["rating"] = {
            "$gte": min_rating
        }

    products = products_collection.find(mongo_query)

    return products_serializer(products)


def view_search_history(email: str):
    return get_user_searches(email)