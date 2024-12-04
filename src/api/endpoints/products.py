from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.utils.decorators import exception_handler
from src.utils.dependencies import product_service
from src.schemas.products import ProductAdd

router = APIRouter(prefix='/categories', tags=['Продукты'])

@router.get('/products')
@cache(expire=1800, namespace='products')
@exception_handler
async def get_all_products(service: product_service):
    return await service.get_all_products()

@router.get('/{category_id}/products')
@cache(expire=1800, namespace=lambda *args, **kwargs: f'products_by_category:{kwargs.get("category_id")}')
@exception_handler
async def get_products_by_category(category_id: int, service: product_service):
    return await service.get_products_by_category(category_id)

@router.post('/products/create')
@exception_handler
async def create_product(data: ProductAdd, service: product_service):
    return await service.create_product(data)

@router.delete('/products/delete/{product_id}')
@exception_handler
async def delete_product(product_id: int, service: product_service):
    return await service.delete_product(product_id)