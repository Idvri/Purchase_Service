from sqlalchemy import MetaData, Integer, String, Table, Column, BigInteger, Boolean

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('last_name', String, nullable=False),
    Column('first_name', String, nullable=False),
    Column('surname', String, nullable=False),
    Column('number', BigInteger, primary_key=True, nullable=False),
    Column('email', String, primary_key=True, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),
)
