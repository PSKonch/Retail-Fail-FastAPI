from pydantic import BaseModel

class CartAdd(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int