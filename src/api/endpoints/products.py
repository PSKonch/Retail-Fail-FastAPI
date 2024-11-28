from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends
from slugify import slugify
from sqlalchemy import select, insert, delete, update

from src.db.postgres.database import database as db
from src.models.products import ProductModel
from src.models.users import UserModel
from src.models.cart import CartModel
from src.schemas.products import Product, ProductAdd
from src.api.endpoints.auth import auth_user, oauth2_scheme, decode_token

router = APIRouter(prefix='/categories', tags=['Продукты'])

@router.get('/products')
async def get_all_products(db: db):
    query = select(ProductModel)
    result = await db.execute(query)
    return result.scalars().all()

@router.post('/products/create')
async def create_product(db: db, data: ProductAdd):
    try:
        stmt = (
            insert(ProductModel)
            .values(**data.model_dump())
        )
        await db.execute(stmt)
        await db.commit()
        return 'ok'
    except:
        await db.rollback()
        return 'not ok'
    
@router.post('/products/{product_id}')
async def add_to_cart(db: db, product_id: int, token: Annotated[str, Depends(oauth2_scheme)], quantity: int):
        payload = await decode_token(token)
        user_id = payload.get('id')

        existing_item = await db.scalar(
            select(CartModel).where(
                CartModel.product_id == product_id,
                CartModel.user_id == user_id
            )
        )

        if existing_item:
            query = (
                update(CartModel)
                .where(CartModel.product_id == product_id, CartModel.user_id == user_id)
                .values(quantity=CartModel.quantity + quantity)
            )
        else:
            query = insert(CartModel).values(
                product_id=product_id,
                user_id=user_id,
                quantity=quantity
            )

        await db.execute(query)
        await db.commit()
        return 'Transaction Success'
