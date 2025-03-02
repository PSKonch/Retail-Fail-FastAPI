from pydantic import BaseModel

class Payment(BaseModel):
    id: int
    order_id: int
    payment_intent_id: str
    amount: int
    currency: str  
    status: str 