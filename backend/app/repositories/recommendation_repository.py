from app.database.mongodb import products_collection


def get_product_by_id(product_id: int):
    return products_collection.find_one({"id": product_id})


def get_products_by_category(category: str):
    return list(
        products_collection.find({"category": category})
    )