from celery import Celery
from celery.schedules import crontab
from src.core.setting import settings  

# Запуск воркера на Windows
# python -m celery -A src.core.celery_app worker --loglevel=info --pool=solo
# Запуск расписания
# python -m celery -A src.core.celery_app beat --loglevel=info
# Запуск мониторинга
# python -m celery -A src.core.celery_app flower

celery_app = Celery(
    "my_app", 
    broker=settings.RABBITMQ_URL,  
    backend=settings.REDIS_URL, 
    include=[
        "src.tasks.notifications",
        "src.tasks.orders"] 
)

celery_app.conf.update(
    task_serializer="json",  
    accept_content=["json"],  
    result_serializer="json",  
    timezone="UTC",
    enable_utc=True, 
    broker_connection_retry_on_startup=True
)


celery_app.conf.beat_schedule = {
    "migrate-orders-every-15-minutes": {
        "task": "src.tasks.orders.migrate_old_orders",
        "schedule": crontab(minute="*/15"),  # Запуск каждую минуту
    }
}

import src.services.email_service