from pydantic import BaseModel


class AlternativeRequest(BaseModel):
    product_id: int