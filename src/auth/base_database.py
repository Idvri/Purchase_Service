from typing import Optional

from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.models import UP, ID


class CostumeSQLAlchemyUserDatabase(SQLAlchemyUserDatabase[UP, ID]):

    async def get_by_number(self, number: str) -> Optional[UP]:
        statement = select(self.user_table).where(
            func.lower(self.user_table.number) == func.lower(number)
        )
        return await self._get_user(statement)
