import datetime

from typing import Optional, Annotated, List

from fastapi_users.db import SQLAlchemyBaseUserTable

from sqlalchemy import String, Integer, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()

intpk = Annotated[
    int,
    mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
]


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
    basket: Mapped['Basket'] = relationship(back_populates='user', lazy=False)


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(
        String
    )
    price: Mapped[int] = mapped_column(
        Integer
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=datetime.datetime.utcnow,
        nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean
    )
    basket_id: Mapped[Optional[int]] = mapped_column(ForeignKey("basket.id"))
    basket: Mapped[Optional['Basket']] = relationship(back_populates="products")


class Basket(Base):
    __tablename__ = 'basket'

    id: Mapped[intpk]

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    user: Mapped['User'] = relationship(back_populates='basket')

    products: Mapped[List['Product']] = relationship(
        back_populates="basket",
        lazy=False
    )

    def get_price(self):
        """Getter для получения стоимости корзины"""
        common_price: int = 0
        for product in self.products:
            common_price += product.price
        return common_price
