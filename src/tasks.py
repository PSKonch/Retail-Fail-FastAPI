import asyncio
from src.core.celery_app import celery_app
from src.db.postgres.manager import DBManager
from src.utils.dependencies import db_manager
from src.models.orders import OrderModel
from src.services.email_service import send_email_sync
from src.utils.constants import ORDER_STATUSES_TO_EMAIL

@celery_app.task
def update_order_status_and_notify(user_id: int, user_email: str, new_status: str):
    """Обновляет статус заказа и отправляет email-уведомление пользователю."""
    from src.database.db_manager import DBManager  # type: ignore # Импортируем здесь, чтобы не было циклического импорта

    async def async_update():
        async with DBManager() as db:  # Открываем сессию внутри таски
            order = await db.order.get_filtered(OrderModel.user_id == user_id).first()

            if not order:
                return {"error": "No active orders found"}

            # Обновляем статус заказа
            await db.order.update(
                OrderModel.id == order.id,
                values={"status": new_status}
            )
            await db.commit()

    # Запускаем асинхронную часть в синхронной Celery-таске
    import asyncio
    asyncio.run(async_update())

    # Отправляем email (синхронная функция)
    subject = "Статус вашего заказа изменен"
    message = ORDER_STATUSES_TO_EMAIL[new_status]
    send_email_sync(to_email=user_email, subject=subject, message=message)

    return {"status": f"Order updated to '{new_status}' and email sent"}