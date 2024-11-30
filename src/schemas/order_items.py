from typing import List
from pydantic import BaseModel

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price_per_item: float