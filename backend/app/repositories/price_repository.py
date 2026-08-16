from app.database.mongodb import products_collection


def get_product_by_id(product_id: int):
    return products_collection.find_one({"id": product_id})


def get_price_history(product_id: int):
    product = get_product_by_id(product_id)

    if not product:
        return None

    return product.get("price_history", [])