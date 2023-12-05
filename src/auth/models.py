from sqlalchemy import MetaData, Integer, String, Table, Column, BigInteger, Boolean

metadata = MetaData()

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('last_name', String, nullable=False),
    Column('first_name', String, nullable=False),
    Column('surname', String, nullable=False),
    Column('number', BigInteger, unique=True),
    Column('email', String, unique=True),
    Column('hashed_password', String, nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),
)
