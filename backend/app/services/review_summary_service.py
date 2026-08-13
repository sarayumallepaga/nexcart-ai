from fastapi import HTTPException

from app.ai.groq_client import client
from app.database.mongodb import products_collection


def summarize_reviews(product_id: int):

    product = products_collection.find_one({"id": product_id})

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    reviews = "\n".join(product["reviews"])

    prompt = f"""
You are an expert shopping assistant.

These are customer reviews for:

{product["name"]}

Reviews:

{reviews}

Summarize them in this format.

Pros:
- point
- point

Cons:
- point
- point

Overall Verdict:
One short paragraph.
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
        "summary": response.choices[0].message.content
    }