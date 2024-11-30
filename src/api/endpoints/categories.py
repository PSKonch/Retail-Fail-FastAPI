from fastapi import APIRouter
from sqlalchemy import select, insert, delete

from src.db.postgres.database import database as db
from src.utils.dependencies import db_manager
from src.models.categories import CategoryModel
from src.schemas.categories import CategoryAdd

router = APIRouter(prefix='/categories', tags=['Категории'])

@router.get('/')
async def get_all_categories(db: db_manager):
    return await db.category.get_all()


@router.post('/')
async def create_category(db: db, data: CategoryAdd):
    stmt = insert(CategoryModel).values(**data.model_dump())
    await db.execute(stmt)
    await db.commit()
    return {
        'status': 'ok'
    }


@router.delete('/', description='Удаляет конкретную категорию и все товары с ней связанные, включая те, что в корзинах')
async def delete_category(db: db_manager, category_id: int):
    try:
        product_ids = await db.product.get_filtered(category_id=category_id)
        
        for product_id in product_ids:
            await db.cart.delete(product_id=product_id.id)

        await db.product.delete(category_id=category_id)
        await db.category.delete(id=category_id)
        await db.commit()
        return 'ok'
    except:
        return 'not ok'