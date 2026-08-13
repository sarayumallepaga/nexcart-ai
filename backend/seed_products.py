from app.database.mongodb import products_collection
from app.database.products import products

# Clear existing products
products_collection.delete_many({})

# Insert new products
products_collection.insert_many(products)

print(f"✅ Inserted {len(products)} products into MongoDB!")