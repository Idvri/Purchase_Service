from typing import List

from pydantic import BaseModel


class ProductGet(BaseModel):
    name: str
    price: int


class BasketGet(BaseModel):
    products: List[ProductGet]
