from typing import List, Annotated

from fastapi import Form, Query
from pydantic import BaseModel


class ProductGet(BaseModel):
    name: str
    price: int


class BasketGet(BaseModel):
    products: List[ProductGet]


class BasketLoad:

    def __init__(self, *, product: Annotated[str, Form()]):
        self.product = product


class BasketLoadArray:

    def __init__(self, *, products: List[str] = Form()):
        self.products = products[0].split(',') if products else []
