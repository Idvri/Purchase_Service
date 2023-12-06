import re

from typing_extensions import Annotated

from fastapi.param_functions import Form

from fastapi_users import schemas
from fastapi_users.schemas import PYDANTIC_V2

from pydantic import ConfigDict, Field, field_validator


class UserRead(schemas.BaseUser[int]):
    id: int
    last_name: str
    first_name: str
    surname: str
    number: str
    email: str

    if PYDANTIC_V2:
        model_config = ConfigDict(from_attributes=True)
    else:

        class Config:
            orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    last_name: str = Field(pattern=r'[A-ZА-ЯЁ]{1}[a-zа-яё]+')
    first_name: str = Field(pattern=r'[A-ZА-ЯЁ]{1}[a-zа-яё]+')
    surname: str = Field(pattern=r'[A-ZА-ЯЁ]{1}[a-zа-яё]+')
    number: str = Field(pattern=r'^\+7[0-9]{10}$')
    email: str = Field(pattern=r'^[a-z0-9_\-]+[a-z0-9_\-\.]+[a-z0-9_\-]+@[a-z]+\.[a-z]+$')
    password: str = Field(min_length=8)

    @field_validator('password')
    @classmethod
    def password_validation(cls, password: str) -> str:
        re_for_pw: re.Pattern[str] = re.compile(r'^(?=.*[A-Z])(?=.*[$%&!:])[a-zA-Z$%&!:].{7,}$')
        if not re_for_pw.match(password):
            raise ValueError("invalid password")
        return password


class UserAuth:

    def __init__(self, *,  email_or_number: Annotated[str, Form()], password: Annotated[str, Form()]):
        self.email_or_number = email_or_number
        self.password = password
