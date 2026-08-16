from pydantic import BaseModel


class BuyAdviceRequest(BaseModel):
    product_id: int