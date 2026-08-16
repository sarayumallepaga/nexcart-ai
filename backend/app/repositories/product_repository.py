from bson import ObjectId

from app.database.mongodb import products_collection


def get_all_products():
    return list(products_collection.find())


def get_product_by_id(product_id: str):
    if not ObjectId.is_valid(product_id):
        return None

    return products_collection.find_one({
        "_id": ObjectId(product_id)
    })


def get_products_by_category(category: str):
    return list(
        products_collection.find({"category": category})
    )


def search_products(query: str):
    return list(
        products_collection.find(
            {
                "name": {
                    "$regex": query,
                    "$options": "i"
                }
            }
        )
    )