from fastapi import APIRouter, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from src.utils.dependencies import db_manager, current_user_id

router = APIRouter(prefix='', tags=['Корзина'])

@router.get('/cart')
@cache(expire=1800, namespace=lambda *args, **kwargs: f"cart:{kwargs.get('user_id')}")
async def get_all_in_cart(
    db: db_manager,
    user_id: current_user_id
):
    try:
        return await db.cart.get_filtered(user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail={'message': 'Transaction Failed', 'error': str(e)}
        )


@router.post('/products', description='Добавление продуктов в корзину')
async def add_to_cart(
    db: db_manager, 
    product_id: int, 
    user_id: current_user_id, 
    quantity: int
):
    try:
        await db.cart.add_or_update_cart(user_id, product_id, quantity)
        await db.commit()
        await FastAPICache.clear(namespace=f'cart:{user_id}')
        return {'message': 'Transaction Success'}
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, 
            detail={'message': 'Transaction Failed', 'error': str(e)}
        )


@router.delete('/cart')
async def remove_or_decrease_item(
    db: db_manager, 
    product_id: int, 
    user_id: current_user_id, 
    quantity: int = 1
):
    try:
        await db.cart.remove_or_decrease_quantity(user_id, product_id, quantity)
        await db.commit()
        await FastAPICache.clear(namespace=f'cart:{user_id}')
        return {'message': f'Item with product_id {product_id} updated in cart'}
    except ValueError as e:
        raise HTTPException(
            status_code=404, 
            detail=str(e)
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                'message': f'Failed to update item {product_id} in cart', 
                'error': str(e)
            }
        )
    
@router.delete('/cart/clear')
async def clear_cart(
    db: db_manager, 
    user_id: current_user_id
):
    try:
        await db.cart.clear_cart(user_id)
        await db.commit()
        await FastAPICache.clear(namespace=f'cart:{user_id}')
        return {'message': 'Cart cleared successfully'}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail={'message': 'Failed to clear cart', 'error': str(e)})