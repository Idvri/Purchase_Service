from typing import List, Annotated

from fastapi import Form
from pydantic import BaseModel


class ProductGet(BaseModel):
    name: str
    price: int


class BasketGet(BaseModel):
    products: List[ProductGet]


class BasketLoad:

    def __init__(self, *,  product: Annotated[str, Form()]):
        self.product = product
