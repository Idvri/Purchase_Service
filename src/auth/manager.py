import re

from typing import Optional

from fastapi import Depends, Request

from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, models, exceptions

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from config import SECRET
from database import get_async_session

from auth.models import User
from auth.schemas import UserAuth
from auth.utils import get_user_db

from products.models import Basket


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_email = await self.user_db.get_by_email(user_create.email)
        existing_number = await self.user_db.get_by_number(user_create.number)
        if existing_email is not None or existing_number is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, session=self.user_db.session)

        return created_user

    async def on_after_register(
            self,
            user: models.UP,
            session: AsyncSession = Depends(get_async_session),
    ) -> None:
        stmt = insert(Basket).values(
            {'user_id': user.id},
        )
        await session.execute(stmt)
        await session.commit()

    async def authenticate(
            self, credentials: UserAuth
    ) -> Optional[models.UP]:
        re_for_number: re.Pattern[str] = re.compile(r'^\+7[0-9]{10}$')

        if re_for_number.match(credentials.email_or_number):
            user = await self.user_db.get_by_number(credentials.email_or_number)
        else:
            user = await self.user_db.get_by_email(credentials.email_or_number)

        if user is None:
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None

        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
