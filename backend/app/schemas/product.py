from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    brand: str
    category: str
    price: float
    rating: float
    store: str
    image: str