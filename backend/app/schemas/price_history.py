from pydantic import BaseModel


class PriceHistory(BaseModel):
    date: str
    price: float