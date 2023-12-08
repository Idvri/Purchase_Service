from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy import select, func, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database import get_async_session

from auth.base_config import fastapi_users
from auth.models import User

from products.models import Product, Basket
from products.schemas import ProductGet, BasketGet, BasketLoad

products_router = APIRouter(
    prefix='/products',
    tags=['Product']
)

basket_router = APIRouter(
    prefix='/basket',
    tags=['Basket']
)

current_active_user = fastapi_users.current_user(active=True)


@products_router.get('/', response_model=List[ProductGet])
async def get_products(
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(Product).where(Product.is_active)
    result = await session.execute(query)
    return result.scalars().all()


@basket_router.get('/', response_model=BasketGet)
async def get_basket(
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(Basket).where(Basket.user_id == user.id).options(joinedload(Basket.products))
    result = await session.execute(query)
    return result.unique().scalars().first()


# @basket_router.post('/add_product')
# async def post_basket(
#         user: User = Depends(current_active_user),
#         credentials: BasketLoad = Depends(),
#         session: AsyncSession = Depends(get_async_session)
# ):
#     stmt = insert(Basket.products).values(credentials.product)
#     await session.execute(stmt)
#     await session.commit()
#     return {'detail': f'"{credentials.product}" was added in your basket!'}


@basket_router.get('/price')
async def get_basket_price(
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(
        func.sum(
            Product.price
        )
    ).where(
        Product.basket_id.in_(
            select(
                Basket.id
            ).where(
                Basket.user_id == user.id
            )
        )
    )
    result = await session.execute(query)
    return {'detail': f'{result.unique().scalars().first()} RUB'}
