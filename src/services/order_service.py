from typing import List
from fastapi import HTTPException

from src.db.postgres.manager import DBManager
from src.tasks.notifications import notify_user_about_orders_status

class OrderService:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager
        self.order_repo = db_manager.order
        self.user_repo = db_manager.user
        self.cart_repo = db_manager.cart

    async def get_all_orders(self, user_id: int):
        try:
            return await self.order_repo.get_orders_by_user(user_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail={'message': 'Failed to fetch orders', 'error': str(e)})

    async def get_order_by_id(self, user_id: int, order_id: int):
        try:
            return await self.order_repo.get_one_or_none(user_id=user_id, id=order_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail={'message': 'Failed to fetch order', 'error': str(e)})

    async def create_order(self, user_id: int, user_email: str):
        try:
            new_order = await self.order_repo.create_order_with_cart(user_id=user_id)
            await self.db_manager.commit()
            notify_user_about_orders_status.apply_async(args=[user_email, "pending", new_order.id])
            return {"status": "ok", "order_id": new_order.id, "total_price": new_order.total_price}
        except ValueError as e:
            await self.db_manager.rollback()
            raise HTTPException(status_code=400, detail={'message': str(e)})
        except Exception as e:
            await self.db_manager.rollback()
            raise HTTPException(status_code=500, detail={'message': 'Failed to create order', 'error': str(e)})

    async def cancel_order(self, user_id: int, user_email: str, order_id: int):
        try:
            order = await self.order_repo.get_one_or_none(user_id=user_id, id=order_id)
            if not order:
                raise HTTPException(status_code=404, detail="Order not found.")
            if order.status == "got":
                raise HTTPException(status_code=400, detail="Order already received and cannot be canceled.")

            await self.order_repo.update(
                filters={"id": order_id, "user_id": user_id},
                values={"status": "canceled"}
            )
            await self.db_manager.commit()
            notify_user_about_orders_status.apply_async(args=[user_email, "canceled", order.id])
            return {"status": "ok"}
        except HTTPException:
            raise
        except Exception as e:
            await self.db_manager.rollback()
            raise HTTPException(status_code=500, detail={'message': 'Failed to cancel order', 'error': str(e)})

    async def give_order_to_user(self, employee_id: int, user_id: int, order_id: int):
        try:
            employee = await self.user_repo.get_one_or_none(id=employee_id)
            if not employee or employee.role not in ["super_user", "supplier"]:
                raise HTTPException(status_code=403, detail="Access denied.")

            user = await self.user_repo.get_one_or_none(id=user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found.")

            order = await self.order_repo.get_one_or_none(user_id=user_id, id=order_id)
            if not order or order.status != "arrived":
                raise HTTPException(status_code=400, detail="Order not found or not ready for pickup.")

            await self.order_repo.update(
                filters={"user_id": user_id, "id": order_id},
                values={"status": "got"}
            )
            await self.db_manager.commit()
            notify_user_about_orders_status.apply_async(args=[user.email, "got", order.id])
            return {"status": "ok"}
        except HTTPException:
            raise
        except Exception as e:
            await self.db_manager.rollback()
            raise HTTPException(status_code=500, detail={'message': 'Failed to give order to user', 'error': str(e)})

    async def deliver_orders_to_post(self, supplier_id: int, order_ids: List[int]):
        try:
            supplier = await self.user_repo.get_one_or_none(id=supplier_id)
            if not supplier or supplier.role not in ["super_user", "supplier"]:
                raise HTTPException(status_code=403, detail="Access denied.")

            arrived_orders = []

            for order_id in order_ids:
                order = await self.order_repo.get_one_or_none(id=order_id)
                if not order:
                    raise HTTPException(status_code=404, detail=f"Order {order_id} not found.")
                await self.order_repo.update(
                    filters={"id": order_id},
                    values={"status": "arrived"}
                )
                arrived_orders.append(order)

            await self.db_manager.commit()

            for order in arrived_orders:
                user = await self.user_repo.get_one_or_none(id=order.user_id)
                if user:
                    notify_user_about_orders_status.apply_async(args=[user.email, "arrived", order.id])

            return {"status": "ok"}
        except HTTPException:
            raise
        except Exception as e:
            await self.db_manager.rollback()
            raise HTTPException(status_code=500, detail={'message': 'Failed to deliver orders', 'error': str(e)})
        
    async def get_last_order(self, user_id: int):
        order = await self.order_repo.get_orders_by_user(user_id=user_id)
        return order[-1]
    
    async def reorder_last_order(self, user_id: int, user_email: str):
        try:
            new_order = await self.order_repo.reorder_last_order(user_id)
            await self.db_manager.commit()
            notify_user_about_orders_status.apply_async(args=[user_email, "pending", new_order.id])
            return {"status": "ok"}
        except Exception as e:
            await self.db_manager.rollback()
            raise HTTPException(status_code=500, detail={'message': 'Reorder attempt failed', 'error': str(e)})