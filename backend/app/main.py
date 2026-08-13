from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.compare import router as compare_router

from app.api.routes.search import router as search_router
from app.api.routes.ai_compare import router as ai_compare_router
from app.api.routes.product import router as product_router
from app.api.routes.review_summary import router as review_router
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



@app.get("/")
def home():
    return {
        "message": "Welcome to NexCart AI 🚀"
    }