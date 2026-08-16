from fastapi import APIRouter

from app.services.ai_service import (
    get_buy_advice,
    summarize_reviews,
    predict_price,
    compare_products,
    recommend_alternatives,
    shopping_chat,
)

from app.repositories.product_repository import (
    get_product_by_id,
    get_products_by_category,
)

from app.schemas.chat_schema import ChatRequest

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)

@router.get("/buy-advice/{product_id}")
def buy_advice(product_id: str):

    product = get_product_by_id(product_id)

    if not product:
        return {
            "error": "Product not found"
        }

    advice = get_buy_advice(product)

    return {
        "product": product["name"],
        "advice": advice,
    }


@router.get("/review-summary/{product_id}")
def review_summary(product_id: str):

    product = get_product_by_id(product_id)

    if not product:
        return {
            "error": "Product not found"
        }

    summary = summarize_reviews(product)

    return {
        "product": product["name"],
        "summary": summary,
    }


@router.get("/price-prediction/{product_id}")
def price_prediction(product_id: str):

    product = get_product_by_id(product_id)

    if not product:
        return {
            "error": "Product not found"
        }

    prediction = predict_price(product)

    return {
        "product": product["name"],
        "prediction": prediction,
    }    
    
    
@router.get("/compare/{product1_id}/{product2_id}")
def compare(product1_id: str, product2_id: str):

    product1 = get_product_by_id(product1_id)
    product2 = get_product_by_id(product2_id)

    if not product1 or not product2:
        return {
            "error": "One or both products not found"
        }

    result = compare_products(product1, product2)

    return {
        "product_1": product1["name"],
        "product_2": product2["name"],
        "comparison": result,
    }    
    
    
@router.get("/alternatives/{product_id}")
def alternatives(product_id: str):

    product = get_product_by_id(product_id)

    if not product:
        return {
            "error": "Product not found"
        }

    similar_products = get_products_by_category(
        product["category"]
    )

    similar_products = [
        p for p in similar_products
        if p["_id"] != product["_id"]
    ]

    result = recommend_alternatives(
        product,
        similar_products,
    )

    return {
        "product": product["name"],
        "alternatives": result,
    }    
    
@router.post("/chat")
def chat(request: ChatRequest):

    return shopping_chat(
        request.message
    )    