from fastapi import APIRouter

from app.schemas.review import ReviewSummaryRequest
from app.services.review_summary_service import summarize_reviews

router = APIRouter()


@router.post("/summarize-reviews")
def summarize(request: ReviewSummaryRequest):
    return summarize_reviews(request.product_id)