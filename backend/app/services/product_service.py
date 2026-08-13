from app.database.products import products


def get_product_by_id(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    return None