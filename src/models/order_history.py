from typing import List

from beanie import Document

from src.schemas.order_items import OrderItem


class OrderHistory(Document):
    order_id: int  # ID заказа из PostgreSQL
    user_id: int

    items: List[OrderItem]
    total_price: float
    status: str