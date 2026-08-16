from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.compare import router as compare_router

from app.api.routes.search import router as search_router
from app.api.routes.ai_compare import router as ai_compare_router
from app.api.routes.product import router as product_router
from app.api.routes.review_summary import router as review_router
from app.api.routes.buy_advice import router as buy_advice_router
from app.api.routes.alternative import router as alternative_router
from app.api.routes.recommendation import router as recommendation_router
from app.api.routes.price import router as price_router
from app.api.routes.auth import router as auth_router
from app.security.jwt_handler import create_access_token
from app.api.routes.profile import router as profile_router
from app.api.routes.wishlist import router as wishlist_router
from app.api.routes.ai import router as ai_router

app = FastAPI(
    title="NexCart AI",
    description="Agentic Shopping Intelligence Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router)
app.include_router(compare_router)
app.include_router(ai_compare_router)
app.include_router(product_router)
app.include_router(review_router)
app.include_router(buy_advice_router)
app.include_router(alternative_router)
app.include_router(recommendation_router)
app.include_router(price_router)
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)
app.include_router(profile_router)
app.include_router(wishlist_router)
app.include_router(ai_router)



@app.get("/")
def home():
    return {
        "message": "Welcome to NexCart AI 🚀"
    }