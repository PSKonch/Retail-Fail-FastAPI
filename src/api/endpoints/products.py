from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache

from src.utils.dependencies import db_manager

from src.schemas.products import ProductAdd

router = APIRouter(prefix='/categories', tags=['Продукты'])

@router.get('/products')
@cache(expire=1800, namespace='products')
async def get_all_products(db: db_manager):
    return await db.product.get_all()

@router.get('/{category_id}/products')
@cache(expire=1800, namespace=lambda *args, **kwargs: f'products_by_category:{kwargs.get("category_id")}')
async def get_products_by_category(db: db_manager, category_id: int):
    return await db.product.get_filtered(category_id=category_id)

@router.post('/products/create')
async def create_product(db: db_manager, data: ProductAdd):
    try:
        await db.product.add(data)
        await db.commit()
        await FastAPICache.clear(namespace=f'products_by_category:{data.category_id}')
        await FastAPICache.clear(namespace='products')
        return {"status": "success", "message": "Product added successfully"}
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.delete('/products/delete/product_id')
async def delete_product(db: db_manager, product_id: int):
    try:
        await db.cart.delete(product_id=product_id)
        await db.product.delete(id=product_id)
        await db.commit()
        return {"status": "success", "message": "Product deleted successfully"}
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
