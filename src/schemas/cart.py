from pydantic import BaseModel

from src.schemas.products import Product  

class Cart(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    product: Product