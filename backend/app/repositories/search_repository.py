from app.database.mongodb import db

search_collection = db["search_history"]


def save_search(data):
    search_collection.insert_one(data)


def get_user_searches(email):
    return list(
        search_collection.find(
            {"user_email": email},
            {"_id": 0}
        ).sort("searched_at", -1)
    )