from typing import Optional

from fastapi_users import schemas
from fastapi_users.schemas import PYDANTIC_V2

from pydantic import ConfigDict


class UserRead(schemas.BaseUser[int]):
    id: int
    last_name: str
    first_name: str
    surname: str
    number: int
    email: str

    if PYDANTIC_V2:
        model_config = ConfigDict(from_attributes=True)
    else:

        class Config:
            orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    last_name: str
    first_name: str
    surname: str
    number: int
    email: str
    password: str
