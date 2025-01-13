from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.db.postgres.manager import DBManager
from src.services.cart_service import CartService
from src.utils.dependencies import current_user_id
from src.db.postgres.database import async_session_maker 

router = APIRouter(prefix='', tags=['Корзина'])

async def get_cart_service():
    async with DBManager(async_session_maker) as db:
        yield CartService(db)

@router.get('/cart')
@cache(expire=1800, namespace=lambda user_id: f"cart:{user_id}")
async def get_all_in_cart(
    user_id: current_user_id,
    cart_service: Annotated[CartService, Depends(get_cart_service)]
):
    return await cart_service.get_all_items_in_cart(user_id)


@router.post('/products', description='Добавление продуктов в корзину')
async def add_to_cart(
    cart_service: Annotated[CartService, Depends(get_cart_service)], 
    product_id: int, 
    user_id: current_user_id, 
    quantity: int
):
    return await cart_service.add_to_cart(user_id, product_id, quantity)


@router.delete('/cart')
async def remove_or_decrease_item(
    cart_service: Annotated[CartService, Depends(get_cart_service)], 
    product_id: int, 
    user_id: current_user_id, 
    quantity: int = 1
):
    return await cart_service.remove_or_decrease_item(user_id, product_id, quantity)


@router.delete('/cart/clear')
async def clear_cart(
    cart_service: Annotated[CartService, Depends(get_cart_service)], 
    user_id: current_user_id
):
    return await cart_service.clear_cart(user_id)