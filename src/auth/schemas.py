import re

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
    last_name: str
    first_name: str
    surname: str
    number: str = Field(pattern=r'\+7[0-9]{10}')
    email: str
    password: str = Field(min_length=8)

    @field_validator('password')
    @classmethod
    def regex_match(cls, password: str) -> str:
        re_for_pw: re.Pattern[str] = re.compile(r'^(?=.*[A-Z])(?=.*[$%&!:])[a-zA-Z$%&!:].{7,}$')
        if not re_for_pw.match(password):
            raise ValueError("invalid password")
        return password
