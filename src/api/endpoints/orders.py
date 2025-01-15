from typing import Annotated, List
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.db.postgres.manager import DBManager
from src.services.order_service import OrderService
from src.utils.dependencies import current_user_id, current_user_email
from src.db.postgres.database import async_session_maker

router = APIRouter(prefix='', tags=['Заказы'])

async def get_order_service():
    async with DBManager(async_session_maker) as db:
        yield OrderService(db)


@router.get('/orders')
@cache(expire=1800, namespace=lambda user_id: f"orders:{user_id}")
async def get_all_orders(
    user_id: current_user_id,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    return await order_service.get_all_orders(user_id)


@router.get('/order/{order_id}')
async def get_order_by_id(
    order_id: int,
    user_id: current_user_id,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    return await order_service.get_order_by_id(user_id, order_id)


@router.post('/cart/order', description="Создание заказа на основе корзины")
async def create_order(
    user_id: current_user_id,
    user_email: current_user_email,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    return await order_service.create_order(user_id, user_email)


@router.delete('/order/{order_id}/cancel', description="Отмена заказа")
async def cancel_order(
    order_id: int,
    user_id: current_user_id,
    user_email: current_user_email,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    return await order_service.cancel_order(user_id, user_email, order_id)


@router.post('/order/{order_id}/to_user/{user_id}', description="Выдача заказа пользователю")
async def give_an_order_to_user(
    order_id: int,
    user_id: int,
    employee_id: current_user_id,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    return await order_service.give_order_to_user(employee_id, user_id, order_id)


@router.post('/orders/delivery', description="Доставка заказов в постамат")
async def deliver_orders_to_post(
    order_ids: List[int],
    supplier_id: current_user_id,
    order_service: Annotated[OrderService, Depends(get_order_service)]
):
    return await order_service.deliver_orders_to_post(supplier_id, order_ids)