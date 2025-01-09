from enum import Enum

ORDER_STATUSES = {
    "pending",
    "processing",
    "shipped",
    "arrived",
    "got",
    "canceled",
    "returned",
}

ORDER_STATUSES_TO_EMAIL = {
    "pending": "Заказ принят в обработку",
    "processing": "Ваш заказ обрабатывается",
    "shipped": "Ваш заказ отправлен, ожидайте прибытия",
    "arrived": "Заказ прибыл в пункт самовывоза",
    "got": "Вы получили свой заказ. Спасибо за покупку!",
    "canceled": "Ваш заказ был отменен",
    "returned": "Заказ возвращен продавцу",
}