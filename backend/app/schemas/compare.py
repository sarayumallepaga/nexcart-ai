from typing import List

from pydantic import BaseModel

from app.schemas.product import Product


class CompareRequest(BaseModel):
    product_ids: List[int]


class ComparisonResponse(BaseModel):
    products: List[Product]
    cheaper_product: str
    higher_rated_product: str