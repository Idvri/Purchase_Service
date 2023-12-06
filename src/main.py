from fastapi import FastAPI

from auth.base_config import auth_backend, fastapi_users
from auth.router import get_costume_auth_router
from auth.schemas import UserRead, UserCreate

from products.router import router as products_router

app = FastAPI(
    title='Purchase Service'
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    get_costume_auth_router(
        auth_backend,
        fastapi_users.get_user_manager,
        fastapi_users.authenticator
    ),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    products_router
)
