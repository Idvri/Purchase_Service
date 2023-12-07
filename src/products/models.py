from datetime import datetime

from sqlalchemy import MetaData, Table, Column, String, Integer, TIMESTAMP, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String
    )
    price: Mapped[int] = mapped_column(
        Integer
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean
    )

# basket = Table(
#     'basket',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('product.id', Integer, ForeignKey('basket.id')),
# )
