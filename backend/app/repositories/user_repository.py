from app.database.mongodb import users_collection


def get_user_by_email(email: str):
    return users_collection.find_one({"email": email})


def create_user(user: dict):
    return users_collection.insert_one(user)


def get_user_by_id(user_id):
    return users_collection.find_one({"_id": user_id})