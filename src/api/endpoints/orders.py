from fastapi import APIRouter

from src.utils.dependencies import db_manager, current_user_id

router = APIRouter(prefix='/cart', tags=['Заказ'])

@router.post("/order")
async def create_order(
    db: db_manager,
    current_user: current_user_id,
):
    try:
        new_order = await db.order.create_order_with_cart(user_id=current_user)
        await db.commit()
        return {
            "status": "ok",
            "order_id": new_order.id,
            "total_price": new_order.total_price,
        }
    except ValueError as e:
        await db.rollback()
        return {"status": "error", "message": str(e)}