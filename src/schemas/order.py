from typing import List
from pydantic import BaseModel

from src.schemas.order_items import OrderItem

class Order(BaseModel):
    id: int
    user_id: int
    price: float
    status: str
    items: List[OrderItem]