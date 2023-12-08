import datetime

from typing import Optional, Annotated, List

from sqlalchemy import String, Integer, Boolean, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

intpk = Annotated[
    int,
    mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
]


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
        server_default=text('TIMEZONE("utc", now())')
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text('TIMEZONE("utc", now())'),
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

    products: Mapped[List['Product']] = relationship(back_populates="basket")

    @property
    def get_products_price(self):
        return self.products

