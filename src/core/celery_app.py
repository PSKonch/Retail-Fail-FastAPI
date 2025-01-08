from celery import Celery
from src.core.setting import settings  

# Запуск воркера на Windows
# celery -A src.core.celery_app worker --loglevel=info --pool=solo

celery_app = Celery(
    "my_app", 
    broker=settings.RABBITMQ_URL,  
    backend=settings.REDIS_URL, 
    include=["src.services.email_service"] 
)

celery_app.conf.update(
    task_serializer="json",  
    accept_content=["json"],  
    result_serializer="json",  
    timezone="UTC",
    enable_utc=True, 
    broker_connection_retry_on_startup=True
)

import src.services.email_service