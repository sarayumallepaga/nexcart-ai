from app.database.mongodb import db


def get_profile(email: str):
    return db["users"].find_one(
        {"email": email},
        {"_id": 0, "password": 0}
    )