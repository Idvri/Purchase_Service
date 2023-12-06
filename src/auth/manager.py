import re

from typing import Optional

from fastapi import Depends, Request

from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, models, exceptions

from config import SECRET

from auth.models import User
from auth.schemas import UserAuth
from auth.utils import get_user_db


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

        return created_user

    async def authenticate(
        self, credentials: UserAuth
    ) -> Optional[models.UP]:
        re_for_number: re.Pattern[str] = re.compile(r'^\+7[0-9]{10}$')

        if re_for_number.match(credentials.email_or_number):
            try:
                user = await self.user_db.get_by_number(credentials.email_or_number)
            except exceptions.UserNotExists:
                self.password_helper.hash(credentials.password)
                return None
        else:
            try:
                user = await self.user_db.get_by_email(credentials.email_or_number)
            except exceptions.UserNotExists:
                self.password_helper.hash(credentials.password)
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
