from bson import ObjectId


def recently_viewed_serializer(item):
    return {
        "id": str(item["_id"]),
        "user_email": item["user_email"],
        "product_id": item["product_id"],
        "viewed_at": item["viewed_at"],
    }


def recently_viewed_list_serializer(items):
    return [
        recently_viewed_serializer(item)
        for item in items
    ]