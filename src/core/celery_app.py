from celery import Celery
from src.core.setting import settings  

celery_app = Celery(
    "my_app", 
    broker=settings.CELERY_BROKER_URL,  
    backend=settings.CELERY_RESULT_BACKEND, 
)

celery_app.conf.update(
    task_serializer="json",  
    accept_content=["json"],  
    result_serializer="json",  
    timezone="UTC",
    enable_utc=True, 
)