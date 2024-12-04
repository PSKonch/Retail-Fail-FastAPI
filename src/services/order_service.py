from src.services.email_service import notify_user_about_order

class OrderService:
    def __init__(self, db_manager):
        self.db = db_manager

    async def create_order_with_cart(self, user_id: int, user_email: str):
        new_order = await self.db.order.create_order_with_cart(user_id=user_id)
        await self.db.commit()
        await notify_user_about_order(user_email)
        return {
            "status": "ok",
            "order_id": new_order.id,
            "total_price": new_order.total_price,
        }