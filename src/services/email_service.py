import asyncio
import smtplib
import aiosmtplib
from email.parser import Parser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery.schedules import crontab

from src.core.celery_app import celery_app

from src.core.setting import settings
from src.utils.constants import ORDER_STATUSES_TO_EMAIL

async def send_email_async(to_email: str, subject: str, message: str):
    email_message = MIMEMultipart()
    email_message['From'] = settings.SMTP_USERNAME
    email_message['To'] = to_email
    email_message['Subject'] = subject
    email_message.attach(MIMEText(message, _subtype="plain", _charset="utf-8"))

    try:
        await aiosmtplib.send(
            email_message,
            hostname="localhost",
            port=1025,
        )
        print(f'Сообщение доставлено по адресу {to_email}')

        encoded_message = email_message.as_string()  # Получаем всё сообщение как строку
        decoded_body = decode_email_body(encoded_message)
        print(f"Расшифрованное содержимое сообщения:\n{decoded_body}")

    except Exception as e:
        print(f'Произошла ошибка {e}')

def send_email_sync(to_email: str, subject: str, message: str):
    email_message = MIMEMultipart()
    email_message["From"] = settings.SMTP_USERNAME
    email_message["To"] = to_email
    email_message["Subject"] = subject
    email_message.attach(MIMEText(message, _subtype="plain", _charset="utf-8"))

    try:
        with smtplib.SMTP("localhost", 1025) as server:
            server.sendmail(
                settings.SMTP_USERNAME, to_email, email_message.as_string()
            )
        print(f"Сообщение доставлено по адресу {to_email}")

    except Exception as e:
        print(f"Ошибка отправки: {e}")


def decode_email_body(encoded_message: str) -> str: 
    try:
        # Используем Parser для парсинга MIME-структуры
        parsed_message = Parser().parsestr(encoded_message)

        # Извлекаем содержимое тела (первую часть)
        for part in parsed_message.walk():
            if part.get_content_type() == "text/plain":
                charset = part.get_content_charset() or "utf-8"  
                decoded_body = part.get_payload(decode=True).decode(charset)
                return decoded_body

        return "Не удалось найти текстовую часть письма."
    except Exception as e:
        return f"Ошибка расшифровки: {e}"


async def notify_user_about_order(user_email: str):
    subject = "Ваш заказ подтверждён"
    message = "Спасибо за ваш заказ! Мы обработаем его в ближайшее время."
    await send_email_async(to_email=user_email, subject=subject, message=message)


@celery_app.task
def notify_user_about_orders_status(user_email: str, order_status: str):
    """Отправляет email-уведомление пользователю в зависимости от статуса заказа"""
    subject = "Обновление статуса заказа"
    
    # Получаем сообщение на основе статуса заказа
    message = ORDER_STATUSES_TO_EMAIL.get(order_status, "Обновление статуса заказа")
    
    # Отправка email
    send_email_sync(to_email=user_email, subject=subject, message=message)