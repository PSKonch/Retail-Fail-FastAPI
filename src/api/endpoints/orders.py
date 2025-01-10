from fastapi import APIRouter

from src.utils.dependencies import db_manager, current_user_id, current_user_email
from src.services.email_service import notify_user_about_orders_status, update_order_status

router = APIRouter(prefix='', tags=['Заказ'])

@router.get("/orders")
async def get_all_orders(
    db: db_manager,
    user_id: current_user_id,   
):
    return await db.order.get_filtered(user_id=user_id)

@router.get('/order/{order_id}')
async def get_order_by_order_id(
    db: db_manager,
    user_id: current_user_id,
    order_id: int
):
    return await db.order.get_filtered(user_id=user_id, order_id=order_id)

@router.post("/cart/order")
async def create_order(
    db: db_manager,
    current_user: current_user_id,
    current_user_email: current_user_email
):
    try:
        new_order = await db.order.create_order_with_cart(user_id=current_user)
        await db.commit()

        # Обновление статуса в БД + отправка уведомлений
        update_order_status.apply_async(args=[new_order.id, "pending"], countdown=1)
        notify_user_about_orders_status.apply_async(args=[current_user_email, "pending"], countdown=1)

        update_order_status.apply_async(args=[new_order.id, "arrived"], countdown=15)
        notify_user_about_orders_status.apply_async(args=[current_user_email, "arrived"], countdown=15)

        update_order_status.apply_async(args=[new_order.id, "got"], countdown=30)
        notify_user_about_orders_status.apply_async(args=[current_user_email, "got"], countdown=30)

        return {"status": "ok", "order_id": new_order.id, "total_price": new_order.total_price}
    
    except ValueError as e:
        await db.rollback()
        return {"status": "error", "message": str(e)}