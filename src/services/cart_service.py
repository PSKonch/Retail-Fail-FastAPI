from fastapi_cache import FastAPICache

class CartService:
    def __init__(self, db_manager):
        self.db = db_manager

    async def get_cart_items(self, user_id: int):
        return await self.db.cart.get_filtered(user_id=user_id)

    async def add_to_cart(self, user_id: int, product_id: int, quantity: int):
        await self.db.cart.add_or_update_cart(user_id, product_id, quantity)
        await self.db.commit()
        await FastAPICache.clear(namespace=f'cart:{user_id}')
        return {'message': 'Transaction Success'}

    async def remove_or_decrease_item(self, user_id: int, product_id: int, quantity: int):
        await self.db.cart.remove_or_decrease_quantity(user_id, product_id, quantity)
        await self.db.commit()
        await FastAPICache.clear(namespace=f'cart:{user_id}')
        return {'message': f'Item with product_id {product_id} updated in cart'}

    async def clear_cart(self, user_id: int):
        await self.db.cart.clear_cart(user_id)
        await self.db.commit()
        await FastAPICache.clear(namespace=f'cart:{user_id}')
        return {'message': 'Cart cleared successfully'}