from typing import Dict, List

from pydantic import BaseModel


class Product(BaseModel):
    id: str
    name: str
    brand: str
    category: str
    price: float
    rating: float
    store: str
    image: str
    description: str
    specifications: Dict[str, str]
    warranty: str
    reviews: List[str]