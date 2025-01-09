from fastapi import APIRouter

from src.utils.dependencies import db_manager, current_user_id, current_user_email
from src.services.email_service import notify_user_about_orders_status

router = APIRouter(prefix='', tags=['Заказ'])

@router.post("/cart/order")
async def create_order(
    db: db_manager,
    current_user: current_user_id,
    current_user_email: current_user_email
):
    """
    Создает заказ, очищает корзину пользователя и отправляет email-уведомления 
    о разных этапах заказа с помощью Celery.
    """
    try:
        new_order = await db.order.create_order_with_cart(user_id=current_user)
        await db.commit()
        
        # Немедленная отправка уведомления о принятии заказа
        notify_user_about_orders_status.apply_async(
            args=[current_user_email, "pending"],
            countdown=1
        )

        # Отправка уведомления о прибытии заказа через 5 секунд
        notify_user_about_orders_status.apply_async(
            args=[current_user_email, "arrived"],
            countdown=5
        )

        # Отправка уведомления о получении заказа через 10 секунд
        notify_user_about_orders_status.apply_async(
            args=[current_user_email, "got"],
            countdown=10
        )

        return {
            "status": "ok",
            "order_id": new_order.id,
            "total_price": new_order.total_price,
        }
    
    except ValueError as e:
        await db.rollback()
        return {"status": "error", "message": str(e)}