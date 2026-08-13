from pydantic import BaseModel


class ReviewSummaryRequest(BaseModel):
    product_id: int