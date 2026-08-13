def product_serializer(product):
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "brand": product["brand"],
        "price": product["price"],
        "rating": product["rating"],
        "category": product["category"],
        "image": product["image"],
        "description": product["description"],
        "store": product["store"],
        "specifications": product["specifications"],
        "warranty": product["warranty"],
        "reviews": product["reviews"],
    }


def products_serializer(products):
    return [product_serializer(product) for product in products]