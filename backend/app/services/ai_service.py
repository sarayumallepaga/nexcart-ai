import os
import json

from groq import Groq
from app.database.mongodb import db


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ==========================================
# BUY ADVICE
# ==========================================

def get_buy_advice(product: dict):

    prompt = f"""
You are an expert shopping advisor.

Analyze the following product.

Product Name: {product['name']}
Brand: {product['brand']}
Category: {product['category']}
Price: ₹{product['price']}
Rating: {product['rating']}
Description: {product['description']}
Specifications: {product['specifications']}
Warranty: {product['warranty']}

Respond ONLY in valid JSON.

Example:

{{
    "decision": "Buy",
    "score": 9,
    "pros": [
        "...",
        "...",
        "..."
    ],
    "cons": [
        "...",
        "..."
    ],
    "recommendation": "..."
}}

Do not write markdown.
Do not use ```json.
Return only JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.4,
    )

    return json.loads(
        response.choices[0].message.content
    )


# ==========================================
# REVIEW SUMMARY
# ==========================================

def summarize_reviews(product: dict):

    reviews = "\n".join(
        product["reviews"]
    )

    prompt = f"""
You are an expert shopping assistant.

Summarize these customer reviews.

Reviews:
{reviews}

Respond ONLY in valid JSON.

{{
    "overall_sentiment": "Positive",
    "summary": "...",
    "pros": [
        "...",
        "...",
        "..."
    ],
    "cons": [
        "..."
    ]
}}

Return only JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.3,
    )

    return json.loads(
        response.choices[0].message.content
    )


# ==========================================
# PRICE PREDICTION
# ==========================================

def predict_price(product: dict):

    prompt = f"""
You are an e-commerce pricing expert.

Analyze this product and predict whether the price is likely to increase, decrease, or stay stable over the next 30 days.

Product:
Name: {product['name']}
Brand: {product['brand']}
Category: {product['category']}
Current Price: ₹{product['price']}
Rating: {product['rating']}

Respond ONLY in valid JSON.

{{
    "prediction": "Price may decrease",
    "confidence": 85,
    "reason": "Festival sales are common for this category.",
    "best_action": "Wait"
}}

Return only JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.3,
    )

    return json.loads(
        response.choices[0].message.content
    )


# ==========================================
# COMPARE PRODUCTS
# ==========================================

def compare_products(
    product1: dict,
    product2: dict
):

    prompt = f"""
You are an expert shopping advisor.

Compare these two products and recommend the better one.

Product 1:
Name: {product1['name']}
Brand: {product1['brand']}
Price: ₹{product1['price']}
Rating: {product1['rating']}
Specifications: {product1['specifications']}

Product 2:
Name: {product2['name']}
Brand: {product2['brand']}
Price: ₹{product2['price']}
Rating: {product2['rating']}
Specifications: {product2['specifications']}

Respond ONLY in valid JSON.

{{
    "winner": "...",
    "comparison": {{
        "performance": "...",
        "camera": "...",
        "battery": "...",
        "display": "...",
        "value_for_money": "..."
    }},
    "recommendation": "..."
}}

Return only JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.3,
    )

    return json.loads(
        response.choices[0].message.content
    )


# ==========================================
# BETTER ALTERNATIVES
# ==========================================

def recommend_alternatives(
    product: dict,
    alternatives: list
):

    # --------------------------------------
    # Remove duplicate products and exclude
    # the product currently being viewed
    # --------------------------------------

    current_id = str(product.get("id", ""))

    unique_products = []
    seen_ids = set()

    for p in alternatives:

        product_id = str(
            p.get("id", "")
        )

        if not product_id:
            continue

        if product_id == current_id:
            continue

        if product_id in seen_ids:
            continue

        seen_ids.add(product_id)
        unique_products.append(p)

    # --------------------------------------
    # No alternatives available
    # --------------------------------------

    if not unique_products:
        return {
            "alternatives": []
        }

    # --------------------------------------
    # Prepare product information for AI
    # --------------------------------------

    products_text = ""

    for p in unique_products:

        products_text += f"""
Product ID: {p.get('id')}
Name: {p.get('name', '')}
Brand: {p.get('brand', '')}
Category: {p.get('category', '')}
Price: ₹{p.get('price', 0)}
Rating: {p.get('rating', 0)}
Specifications: {p.get('specifications', {})}
Description: {p.get('description', '')}

"""

    # --------------------------------------
    # AI prompt
    # --------------------------------------

    prompt = f"""
You are an expert shopping advisor for NexCart.

The user is currently viewing this product:

Name: {product.get('name', '')}
Brand: {product.get('brand', '')}
Category: {product.get('category', '')}
Price: ₹{product.get('price', 0)}
Rating: {product.get('rating', 0)}
Specifications: {product.get('specifications', {})}

Here are similar products available in the NexCart catalog:

{products_text}

Choose the best three alternatives.

Consider:
- Price
- Rating
- Specifications
- Performance
- Overall value for money
- Whether the alternative is actually better or more suitable

IMPORTANT RULES:

1. Only choose products from the provided catalog.
2. Do not invent products.
3. Do not invent product IDs.
4. Use the exact Product ID provided.
5. Do not choose the product the user is currently viewing.
6. Choose at most three products.
7. Each selected product must have a different Product ID.

Respond ONLY in valid JSON.

Use exactly this format:

{{
    "alternatives": [
        {{
            "id": "PRODUCT_ID",
            "reason": "Explain why this is a better or useful alternative."
        }},
        {{
            "id": "PRODUCT_ID",
            "reason": "Explain why this is a better or useful alternative."
        }},
        {{
            "id": "PRODUCT_ID",
            "reason": "Explain why this is a better or useful alternative."
        }}
    ]
}}

Return only JSON.
"""

    # --------------------------------------
    # Call Groq
    # --------------------------------------

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError(
                "AI returned an empty response."
            )

        content = content.strip()

        # ----------------------------------
        # Remove markdown code fences if AI
        # accidentally adds them
        # ----------------------------------

        if content.startswith("```json"):
            content = content[7:]

        elif content.startswith("```"):
            content = content[3:]

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        # ----------------------------------
        # Parse JSON
        # ----------------------------------

        try:
            ai_result = json.loads(content)

        except json.JSONDecodeError:

            # Sometimes the model adds text before
            # or after the JSON. Try extracting the
            # JSON object.

            start_index = content.find("{")
            end_index = content.rfind("}")

            if (
                start_index == -1
                or end_index == -1
                or end_index <= start_index
            ):
                raise ValueError(
                    "AI did not return valid JSON."
                )

            json_text = content[
                start_index:end_index + 1
            ]

            ai_result = json.loads(
                json_text
            )

        # ----------------------------------
        # Validate AI response
        # ----------------------------------

        if not isinstance(ai_result, dict):
            raise ValueError(
                "AI returned an invalid response."
            )

        selected = ai_result.get(
            "alternatives",
            []
        )

        if not isinstance(selected, list):
            raise ValueError(
                "AI alternatives is not a list."
            )

    except Exception as error:

        # ----------------------------------
        # Safe fallback
        # ----------------------------------
        #
        # If Groq fails or returns malformed
        # JSON, use the actual similar products
        # instead of returning a 500 error.
        #

        print(
            f"Alternative recommendation AI error: {error}"
        )

        selected = []

        for p in unique_products[:3]:

            selected.append(
                {
                    "id": str(
                        p.get("id")
                    ),
                    "reason": (
                        "A similar product from "
                        "the NexCart catalog that "
                        "may offer good value."
                    ),
                }
            )

    # --------------------------------------
    # Convert AI selections into complete
    # product objects
    # --------------------------------------

    final_alternatives = []
    selected_ids = set()

    products_by_id = {
        str(p.get("id")): p
        for p in unique_products
    }

    for selected_product in selected:

        if not isinstance(
            selected_product,
            dict
        ):
            continue

        selected_id = str(
            selected_product.get(
                "id",
                ""
            )
        )

        if not selected_id:
            continue

        if selected_id == current_id:
            continue

        if selected_id in selected_ids:
            continue

        selected_product_data = (
            products_by_id.get(selected_id)
        )

        if not selected_product_data:
            continue

        selected_ids.add(selected_id)

        p = selected_product_data

        final_product = {
            "id": p.get("id"),
            "name": p.get(
                "name",
                "Unknown Product"
            ),
            "brand": p.get(
                "brand",
                ""
            ),
            "category": p.get(
                "category",
                ""
            ),
            "price": p.get(
                "price",
                0
            ),
            "rating": p.get(
                "rating",
                0
            ),
            "store": p.get(
                "store",
                ""
            ),
            "image": p.get(
                "image",
                ""
            ),
            "description": p.get(
                "description",
                ""
            ),
            "specifications": p.get(
                "specifications",
                {}
            ),
            "warranty": p.get(
                "warranty",
                ""
            ),
            "reviews": p.get(
                "reviews",
                []
            ),
            "reason": selected_product.get(
                "reason",
                ""
            ),
        }

        final_alternatives.append(
            final_product
        )

        # Maximum 3 alternatives
        if len(final_alternatives) >= 3:
            break

    # --------------------------------------
    # If AI returned invalid/nonexistent IDs,
    # fill remaining slots with real products
    # --------------------------------------

    if len(final_alternatives) < 3:

        for p in unique_products:

            product_id = str(
                p.get("id", "")
            )

            if product_id in selected_ids:
                continue

            final_product = {
                "id": p.get("id"),
                "name": p.get(
                    "name",
                    "Unknown Product"
                ),
                "brand": p.get(
                    "brand",
                    ""
                ),
                "category": p.get(
                    "category",
                    ""
                ),
                "price": p.get(
                    "price",
                    0
                ),
                "rating": p.get(
                    "rating",
                    0
                ),
                "store": p.get(
                    "store",
                    ""
                ),
                "image": p.get(
                    "image",
                    ""
                ),
                "description": p.get(
                    "description",
                    ""
                ),
                "specifications": p.get(
                    "specifications",
                    {}
                ),
                "warranty": p.get(
                    "warranty",
                    ""
                ),
                "reviews": p.get(
                    "reviews",
                    []
                ),
                "reason": (
                    "A similar product from "
                    "the NexCart catalog that "
                    "may be worth considering."
                ),
            }

            final_alternatives.append(
                final_product
            )

            selected_ids.add(product_id)

            if len(final_alternatives) >= 3:
                break

    # --------------------------------------
    # Final response
    # --------------------------------------

    return {
        "alternatives": final_alternatives
    }


# ==========================================
# SHOPPING CHAT
# ==========================================

def shopping_chat(user_query: str):

    # --------------------------------------
    # Get products from MongoDB
    # --------------------------------------

    products = list(
        db["products"].find(
            {},
            {"_id": 0}
        )
    )

    # --------------------------------------
    # Ask AI to select products
    # --------------------------------------

    prompt = f"""
You are NexCart AI Shopping Assistant.

You have the following product catalog:

{json.dumps(products, indent=2)}

User Question:

{user_query}

Analyze the user's requirements carefully.

If the user is asking for product recommendations:

- recommend only products from the catalog
- consider budget
- consider category
- consider rating
- consider specifications
- explain why each product is suitable
- mention price and rating
- recommend up to 3 products

If the user is asking a general shopping question:

- answer naturally
- use only information from the catalog
- do not invent products

Respond ONLY in valid JSON.

For product recommendations use this format:

{{
    "response": "A natural explanation of your recommendation.",
    "recommended_products": [
        {{
            "name": "Exact product name from catalog",
            "reason": "Why this product is suitable."
        }}
    ]
}}

For a general question use:

{{
    "response": "Your answer here.",
    "recommended_products": []
}}

IMPORTANT:

- Do not invent products.
- Product names must exactly match the catalog.
- Only recommend products that exist in the catalog.
- Recommend a maximum of 3 products.
- Return ONLY valid JSON.
- Do not use markdown.
- Do not use ```json.
"""

    # --------------------------------------
    # Call Groq
    # --------------------------------------

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.3,
    )

    raw_response = (
        response.choices[0].message.content
    )

    # --------------------------------------
    # Parse AI response
    # --------------------------------------

    try:

        # Remove accidental markdown fences
        content = raw_response.strip()

        if content.startswith("```json"):
            content = content[7:]

        elif content.startswith("```"):
            content = content[3:]

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        try:

            ai_result = json.loads(
                content
            )

        except json.JSONDecodeError:

            # Try extracting JSON object
            start_index = content.find("{")
            end_index = content.rfind("}")

            if (
                start_index == -1
                or end_index == -1
                or end_index <= start_index
            ):
                raise ValueError(
                    "AI did not return valid JSON."
                )

            json_text = content[
                start_index:end_index + 1
            ]

            ai_result = json.loads(
                json_text
            )

    except Exception as error:

        print(
            f"Shopping chat AI error: {error}"
        )

        return {
            "response": raw_response,
            "recommended_products": []
        }

    # --------------------------------------
    # Get AI recommendations
    # --------------------------------------

    ai_recommendations = ai_result.get(
        "recommended_products",
        []
    )

    if not isinstance(
        ai_recommendations,
        list
    ):
        ai_recommendations = []

    # --------------------------------------
    # Match AI recommendations with
    # actual MongoDB products
    # --------------------------------------

    recommended_products = []

    for recommendation in ai_recommendations:

        if not isinstance(
            recommendation,
            dict
        ):
            continue

        recommended_name = (
            recommendation.get(
                "name",
                ""
            )
            .strip()
            .lower()
        )

        reason = recommendation.get(
            "reason",
            ""
        )

        if not recommended_name:
            continue

        # Search actual catalog
        for product in products:

            product_name = (
                product.get(
                    "name",
                    ""
                )
                .strip()
                .lower()
            )

            if (
                product_name
                == recommended_name
            ):

                product_data = product.copy()

                # Add AI explanation
                product_data[
                    "ai_reason"
                ] = reason

                recommended_products.append(
                    product_data
                )

                break

        # Maximum 3 products
        if len(
            recommended_products
        ) >= 3:
            break

    # --------------------------------------
    # Return response + actual products
    # --------------------------------------

    return {
        "response": ai_result.get(
            "response",
            "Sorry, I couldn't generate a response."
        ),
        "recommended_products":
            recommended_products,
    }