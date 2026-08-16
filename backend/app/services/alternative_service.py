from fastapi import HTTPException

from app.ai.groq_client import client
from app.database.mongodb import products_collection


def recommend_alternatives(product_id: int):

    product = products_collection.find_one({"id": product_id})

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    alternatives = list(products_collection.find({
        "category": product["category"],
        "id": {"$ne": product_id}
    }))

    prompt = f"""
You are an expert shopping advisor.

Original Product:

Name: {product["name"]}
Brand: {product["brand"]}
Price: ₹{product["price"]}
Rating: {product["rating"]}

Possible Alternatives:

{alternatives}

Recommend the best alternatives.

Explain:

1. Best overall alternative
2. Best value for money
3. Budget recommendation
4. Premium recommendation

Keep your response under 200 words.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )

    return {
        "recommendation": response.choices[0].message.content
    }