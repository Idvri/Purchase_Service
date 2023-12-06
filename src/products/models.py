from datetime import datetime

from sqlalchemy import MetaData, Table, Column, String, Integer, TIMESTAMP, Boolean

metadata = MetaData()

product = Table(
    'product',
    metadata,
    Column('name', String, nullable=False),
    Column('price', Integer, nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
    Column('updated_at', TIMESTAMP),
    Column('is_active', Boolean, nullable=False),
)
