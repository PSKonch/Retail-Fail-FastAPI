from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
from sqlalchemy import select, insert, delete, update

from src.db.postgres.manager import db_manager
from src.db.postgres.database import database as db
from src.models.products import ProductModel
from src.models.users import UserModel
from src.models.cart import CartModel
from src.repositories.cart import CartRepository
from src.schemas.products import Product, ProductAdd
from src.api.endpoints.auth import auth_user, oauth2_scheme, decode_token

from src.repositories.products import ProductRepository

router = APIRouter(prefix='/categories', tags=['Продукты'])

@router.get('/products')
async def get_all_products(db: db_manager):
    return await db.product.get_all()

@router.post('/products/create')
async def create_product(db: db, data: ProductAdd):
        stmt = (
            insert(ProductModel)
            .values(**data.model_dump())
        )
        await db.execute(stmt)
        await db.commit()
        return 'ok'
