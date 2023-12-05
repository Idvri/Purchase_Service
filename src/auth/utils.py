from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.models import UP, ID

from database import get_async_session

from auth.models import User


class AlterSQLAlchemyUserDatabase(SQLAlchemyUserDatabase[UP, ID]):

    async def get_by_number(self, number: str) -> Optional[UP]:
        statement = select(self.user_table).where(
            func.lower(self.user_table.number) == func.lower(number)
        )
        return await self._get_user(statement)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield AlterSQLAlchemyUserDatabase(session, User)
