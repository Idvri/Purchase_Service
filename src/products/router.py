from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from auth.base_config import fastapi_users
from auth.models import User

from products.models import Product
from products.schemas import ProductGet

router = APIRouter(
    prefix='/products',
    tags=['Product']
)

current_active_user = fastapi_users.current_user(active=True)


@router.get('/', response_model=List[ProductGet])
async def get_products(
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(Product).where(Product.is_active)
    result = await session.execute(query)
    return result.scalars().all()
