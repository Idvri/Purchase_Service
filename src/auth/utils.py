from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from database import get_async_session
from models import User

from auth.base_database import CostumeSQLAlchemyUserDatabase


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield CostumeSQLAlchemyUserDatabase(session, User)
