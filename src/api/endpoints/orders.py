from fastapi import APIRouter

from src.tasks import update_order_status_and_notify
from src.utils.dependencies import db_manager, current_user_id, current_user_email
from src.services.email_service import notify_user_about_order, notify_user_about_orders_arrival

router = APIRouter(prefix='', tags=['Заказ'])

@router.post("/cart/order")
async def create_order(
    db: db_manager,
    current_user: current_user_id,
    current_user_email: current_user_email
):
    """
    Функция создает запись заказа в обработке в бд
    Очищает корзину пользователя в бд
    Немедленно отправляет сообщение на почту пользователя о том, что заказ оформлен
    Через минуту срабатывает celery_task на отправку уведомления о прибытии заказа
    """
    try:
        new_order = await db.order.create_order_with_cart(user_id=current_user)
        await db.commit()
        await notify_user_about_order(current_user_email)
        update_order_status_and_notify.apply_async(
            args=[current_user, current_user_email, "arrived"],
            countdown=30
        )
        update_order_status_and_notify.apply_async(
            args=[current_user, current_user_email, "arrived"],  # ✅ Только user_id, email, status
            countdown=5
        )
        update_order_status_and_notify.apply_async(
            kwargs={"user_id": current_user, "user_email": current_user_email, "new_status": "got"},
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