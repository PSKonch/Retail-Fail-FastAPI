from fastapi import APIRouter

from src.utils.decorators import exception_handler
from src.utils.dependencies import order_service, current_user_id, current_user_email

router = APIRouter(prefix='/order', tags=['Заказ'])

@router.post('', summary='Создать заказ')
@exception_handler
async def create_order(
    current_user: current_user_id,
    current_user_email: current_user_email,
    service: order_service
):
    return await service.create_order_with_cart(user_id=current_user, user_email=current_user_email)