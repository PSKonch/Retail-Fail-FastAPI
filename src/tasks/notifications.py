from src.core.celery_app import celery_app
from src.services.email_service import send_email_sync
from src.utils.constants import ORDER_STATUSES_TO_EMAIL

@celery_app.task
def notify_user_about_orders_status(user_email: str, order_status: str, order_id: int):
    """Отправляет email-уведомление пользователю в зависимости от статуса заказа"""
    subject = "Обновление статуса заказа"
    
    # Берём сообщение из словаря, если статус есть, иначе используем дефолтное
    base_message = ORDER_STATUSES_TO_EMAIL.get(order_status, f"Статус вашего заказа изменился на {order_status}")

    # Добавляем номер заказа в любое сообщение
    message = f"Заказ №{order_id}: {base_message}"
    
    # Отправка email
    send_email_sync(to_email=user_email, subject=subject, message=message)