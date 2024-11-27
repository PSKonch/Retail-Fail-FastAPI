from datetime import datetime
from fastapi import APIRouter
from slugify import slugify
from sqlalchemy import select, insert, delete

from src.db.postgres.database import database as db
from src.models.products import ProductModel
from src.schemas.products import Product, ProductAdd

router = APIRouter(prefix='/categories', tags=['Продукты'])

@router.get('/products')
async def get_all_products(db: db):
    query = select(ProductModel)
    result = await db.execute(query)
    return result.scalars().all()

@router.post('/products')
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
        return 'not ok'