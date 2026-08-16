from app.database.mongodb import db

wishlist_collection = db["wishlist"]


def add_to_wishlist(item: dict):
    return wishlist_collection.insert_one(item)


def get_user_wishlist(email: str):
    return list(
        wishlist_collection.find(
            {"user_email": email},
            {"_id": 0}
        )
    )


def remove_from_wishlist(email: str, product_id: int):
    return wishlist_collection.delete_one(
        {
            "user_email": email,
            "product_id": product_id,
        }
    )


def already_exists(email: str, product_id: int):
    return wishlist_collection.find_one(
        {
            "user_email": email,
            "product_id": product_id,
        }
    )