from typing import List
from pydantic import BaseModel

from src.schemas.order_items import OrderItem

# статусы указаны в src.utils.constants

class Order(BaseModel):
    id: int
    user_id: int
    price: float
    status: str
    items: List[OrderItem]