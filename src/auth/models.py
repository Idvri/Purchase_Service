from fastapi_users.db import SQLAlchemyBaseUserTable

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    last_name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    surname: Mapped[str] = mapped_column(
        String, nullable=False
    )
    number: Mapped[str] = mapped_column(
        String, unique=True, primary_key=True
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, primary_key=True
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
