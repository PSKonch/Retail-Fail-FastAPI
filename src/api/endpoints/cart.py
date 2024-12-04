from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.utils.dependencies import current_user_id, cart_service
from src.utils.decorators import exception_handler

router = APIRouter(prefix='', tags=['Корзина'])

@router.get('/cart')
@cache(expire=1800, namespace=lambda *args, **kwargs: f"cart:{kwargs.get('user_id')}")
@exception_handler
async def get_all_in_cart(
    user_id: current_user_id,
    service: cart_service
):
    return await service.get_cart_items(user_id)

@router.post('/products', description='Добавление продуктов в корзину')
@exception_handler
async def add_to_cart(
    product_id: int,
    quantity: int,
    user_id: current_user_id,
    service: cart_service
):
    return await service.add_to_cart(user_id, product_id, quantity)

@router.delete('/cart')
@exception_handler
async def remove_or_decrease_item(
    product_id: int,
    quantity: int,
    user_id: current_user_id,
    service: cart_service
):
    return await service.remove_or_decrease_item(user_id, product_id, quantity)

@router.delete('/cart/clear')
@exception_handler
async def clear_cart(
    user_id: current_user_id,
    service: cart_service
):
    return await service.clear_cart(user_id)