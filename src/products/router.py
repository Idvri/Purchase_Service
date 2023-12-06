from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from products.models import product
from products.schemas import Product

router = APIRouter(
    prefix='/products',
    tags=['Product']
)


@router.get('/', response_model=List[Product])
async def get_products(session: AsyncSession = Depends(get_async_session)):
    query = select(product).where(product.c.is_active)
    result = await session.execute(query)
    return result.mappings().all()
