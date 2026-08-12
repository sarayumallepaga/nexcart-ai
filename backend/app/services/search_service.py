from app.database.products import products


def search_products(
    query="",
    brand=None,
    category=None,
    min_price=None,
    max_price=None,
    min_rating=None,
):
    results = []

    query = query.lower()

    for product in products:

        if query:
            if (
                query not in product["name"].lower()
                and query not in product["brand"].lower()
                and query not in product["category"].lower()
            ):
                continue

        if brand:
            if product["brand"].lower() != brand.lower():
                continue

        if category:
            if product["category"].lower() != category.lower():
                continue

        if min_price is not None:
            if product["price"] < min_price:
                continue

        if max_price is not None:
            if product["price"] > max_price:
                continue

        if min_rating is not None:
            if product["rating"] < min_rating:
                continue

        results.append(product)

    return results