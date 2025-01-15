from fastapi import HTTPException
from fastapi_cache import FastAPICache

from src.db.postgres.manager import DBManager


class CartService:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager
        self.cart_repo = db_manager.cart

    async def get_all_items_in_cart(self, user_id: int):
        try:
            return await self.cart_repo.get_filtered(user_id=user_id)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={'message': 'Transaction Failed', 'error': str(e)}
            )

    async def add_to_cart(self, user_id: int, product_id: int, quantity: int):
        try:
            await self.cart_repo.add_or_update_cart(user_id, product_id, quantity)
            await self.db_manager.commit()
            return {'message': 'Transaction Success'}
        except Exception as e:
            await self.db_manager.rollback()
            raise HTTPException(
                status_code=500,
                detail={'message': 'Transaction Failed', 'error': str(e)}
            )

    async def remove_or_decrease_item(self, user_id: int, product_id: int, quantity: int):
        try:
            await self.cart_repo.remove_or_decrease_quantity(user_id, product_id, quantity)
            await self.db_manager.commit()
            await FastAPICache.clear(namespace=f'cart:{user_id}')
            return {'message': f'Item with product_id {product_id} updated in cart'}
        except ValueError as e:
            raise HTTPException(
                status_code=404,
                detail=str(e)
            )
        except Exception as e:
            await self.db_manager.rollback()
            raise HTTPException(
                status_code=500,
                detail={
                    'message': f'Failed to update item {product_id} in cart',
                    'error': str(e)
                }
            )

    async def clear_cart(self, user_id: int):
        try:
            await self.cart_repo.clear_cart(user_id)
            await self.db_manager.commit()
            await FastAPICache.clear(namespace=f'cart:{user_id}')
            return {'message': 'Cart cleared successfully'}
        except Exception as e:
            await self.db_manager.rollback()
            raise HTTPException(
                status_code=500,
                detail={'message': 'Failed to clear cart', 'error': str(e)}
            )
