from fastapi_users.db import SQLAlchemyBaseUserTable

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
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
        String, unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    basket: Mapped['Basket'] = relationship(back_populates='user')

