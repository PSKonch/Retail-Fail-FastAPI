from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.api.endpoints.auth import decode_token, oauth2_scheme
from src.db.postgres.database import database as db
from src.repositories.cart import CartRepository

router = APIRouter(prefix='', tags=['Корзина'])

@router.get('/cart')
async def get_all_in_cart(
    db: db,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    try:
        user_id = (await decode_token(token)).get('id')
        cart_repository = CartRepository(db)
        return await cart_repository.get_filtered(user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail={'message': 'Transaction Failed', 'error': str(e)})

@router.post('/products', description='Добавление продуктов в корзину')
async def add_to_cart(
    db: db, 
    product_id: int, 
    token: Annotated[str, Depends(oauth2_scheme)], 
    quantity: int
):
    try:
        user_id = (await decode_token(token)).get('id')
        cart_repository = CartRepository(db)
        await cart_repository.add_or_update_cart(user_id, product_id, quantity)
        await db.commit()
        return {'message': 'Transaction Success'}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail={'message': 'Transaction Failed', 'error': str(e)})
    
@router.delete('/cart')
async def remove_or_decrease_item(
    db: db, 
    product_id: int, 
    token: Annotated[str, Depends(oauth2_scheme)], 
    quantity: int = 1
):
    try:
        user_id = (await decode_token(token)).get('id')
        cart_repository = CartRepository(db)
        await cart_repository.remove_or_decrease_quantity(user_id, product_id, quantity)
        await db.commit()

        return {'message': f'Item with product_id {product_id} updated in cart'}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail={'message': f'Failed to update item {product_id} in cart', 'error': str(e)}
        )
    
@router.delete('/cart/clear')
async def clear_cart(
    db: db, 
    token: Annotated[str, Depends(oauth2_scheme)]
):
    try:
        user_id = (await decode_token(token)).get('id')
        cart_repository = CartRepository(db)
        await cart_repository.clear_cart(user_id)
        await db.commit()
        return {'message': 'Cart cleared successfully'}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail={'message': 'Failed to clear cart', 'error': str(e)})