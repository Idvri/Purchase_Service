from pydantic import BaseModel


class ProductGet(BaseModel):
    name: str
    price: int
