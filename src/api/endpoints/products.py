from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, delete, update

from src.utils.dependencies import db_manager
from src.db.postgres.database import database as db
from src.models.products import ProductModel
from src.schemas.products import Product, ProductAdd
from src.repositories.products import ProductRepository

router = APIRouter(prefix='/categories', tags=['Продукты'])

@router.get('/products')
async def get_all_products(db: db_manager):
    return await db.product.get_all()

@router.post('/products/create')
async def create_product(db: db_manager, data: ProductAdd):
        await db.product.add(data)
        await db.commit()
        return 'ok'
