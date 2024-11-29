from pydantic import BaseModel

class Cart(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int