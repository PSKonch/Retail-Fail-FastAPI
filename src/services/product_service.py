from fastapi_cache import FastAPICache

class ProductService:
    def __init__(self, db_manager):
        self.db = db_manager

    async def get_all_products(self):
        return await self.db.product.get_all()

    async def get_products_by_category(self, category_id: int):
        return await self.db.product.get_filtered(category_id=category_id)

    async def create_product(self, data):
        await self.db.product.add(data)
        await self.db.commit()
        await FastAPICache.clear(namespace=f'products_by_category:{data.category_id}')
        await FastAPICache.clear(namespace='products')
        return {"status": "success", "message": "Product added successfully"}

    async def delete_product(self, product_id: int):
        await self.db.cart.delete(product_id=product_id) 
        await self.db.product.delete(id=product_id)      
        await self.db.commit()
        return {"status": "success", "message": "Product deleted successfully"}
