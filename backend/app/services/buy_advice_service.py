from fastapi import HTTPException

from app.ai.groq_client import client
from app.database.mongodb import products_collection


def get_buy_advice(product_id: int):

    product = products_collection.find_one({"id": product_id})

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    prompt = f"""
You are an expert shopping advisor.

Analyze this product carefully.

Name: {product["name"]}
Brand: {product["brand"]}
Category: {product["category"]}
Price: ₹{product["price"]}
Rating: {product["rating"]}

Specifications:
{product["specifications"]}

Reviews:
{product["reviews"]}

Warranty:
{product["warranty"]}

Reply ONLY in this format:

Decision:
BUY NOW / WAIT / CONSIDER ALTERNATIVES

Confidence:
High / Medium / Low

Reasons:
- reason
- reason
- reason

Summary:
2-3 sentences.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return {
        "advice": response.choices[0].message.content
    }