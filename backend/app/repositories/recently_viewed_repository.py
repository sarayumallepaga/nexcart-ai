from app.database.mongodb import db

recently_viewed_collection = db["recently_viewed"]


def add_recently_viewed(data):
    recently_viewed_collection.insert_one(data)


def get_recently_viewed(email):
    return recently_viewed_collection.find(
        {"user_email": email}
    ).sort("viewed_at", -1)