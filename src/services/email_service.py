import aiosmtplib
from email.parser import Parser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.core.setting import settings

async def send_email(to_email: str, subject: str, message: str):
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
    await send_email(to_email=user_email, subject=subject, message=message)