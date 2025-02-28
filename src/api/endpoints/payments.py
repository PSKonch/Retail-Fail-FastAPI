import stripe
import asyncio

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.core.setting import settings
from src.utils.dependencies import db_manager, current_user_id, current_user_id

stripe.api_key = settings.SECRET_STRIPE_KEY

router = APIRouter(prefix="/payments", tags=["Платежи"])

@router.post("/create/intent")
async def create_intent(amount: int, currency: str = "usd"):
    try:
        intent = await asyncio.to_thread(
            stripe.PaymentIntent.create,
            amount=amount,
            currency=currency,
            payment_method_types=["card"]
        )
        
        return {"intent": intent}
    
    except stripe.error.StripeError as e:
            return {"error": str(e)}
    
