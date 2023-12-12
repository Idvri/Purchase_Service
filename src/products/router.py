from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from auth.base_config import fastapi_users
from auth.models import User

from products.models import Product
from products.schemas import ProductGet, BasketGet, BasketLoad, BasketLoadArray

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
    """Эндпойнт для получения всех доступных товаров авторезированными пользователями."""
    query = select(Product).where(Product.is_active, Product.basket_id.is_(None))
    result = await session.execute(query)
    return result.scalars().all()


@basket_router.get('/', response_model=BasketGet)
async def get_basket(
        user: User = Depends(current_active_user),
):
    """Эндпойнт для отображения корзины текущего пользователя."""
    return user.basket


@basket_router.post('/add_product')
async def add_product(
        user: User = Depends(current_active_user),
        credentials: BasketLoad = Depends(),
        session: AsyncSession = Depends(get_async_session)
):
    """Эндпойнт для добавления товара в корзину текущего пользователя."""
    stmt = update(
        Product
    ).where(
        Product.name == credentials.product,
        Product.basket_id.is_(None)
    ).values(
        basket_id=user.basket.id
    )
    await session.execute(stmt)
    await session.commit()
    return {'detail': f'"{credentials.product}" was added in your basket!'}


@basket_router.post('/add_products')
async def add_products(
        user: User = Depends(current_active_user),
        credentials: BasketLoadArray = Depends(),
        session: AsyncSession = Depends(get_async_session)
):
    """Эндпойнт для добавления нескольких товаров в корзину текущего пользователя."""
    stmt = update(
        Product
    ).where(
        Product.name.in_(credentials.products),
        Product.basket_id.is_(None)
    ).values(
        basket_id=user.basket.id
    )
    await session.execute(stmt)
    await session.commit()
    return {'detail': f'"{", ".join(credentials.products)}" was added in your basket!'}


@basket_router.post('/delete_product')
async def delete_product(
        user: User = Depends(current_active_user),
        credentials: BasketLoad = Depends(),
        session: AsyncSession = Depends(get_async_session)
):
    """Эндпойнт для удаления товара из корзины текущего пользователя."""
    stmt = update(
        Product
    ).where(
        Product.name == credentials.product,
        Product.basket_id == user.basket.id
    ).values(
        basket_id=None
    )
    await session.execute(stmt)
    await session.commit()
    return {'detail': f'"{credentials.product}" was deleted in your basket!'}


@basket_router.post('/clean')
async def clean_basket(
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Эндпойнт для отчистки корзины текущего пользователя."""
    for product in user.basket.products:
        stmt = update(
            Product
        ).where(
            Product.name == product.name,
            Product.basket_id == user.basket.id
        ).values(
            basket_id=None
        )
        await session.execute(stmt)
        await session.commit()
    return {'detail': f'Your basket is cleaned!'}


@basket_router.get('/price')
async def get_basket_price(
        user: User = Depends(current_active_user),
):
    """Эндпойнт для получения общей стоимости корзины текущего пользователя."""
    return {'detail': f'{user.basket.get_price()} RUB'}
