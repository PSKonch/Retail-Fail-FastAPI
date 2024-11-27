from fastapi import APIRouter
from sqlalchemy import select, insert, delete

from src.db.postgres.database import database as db
from src.models.categories import CategoryModel
from src.schemas.categories import CategoryAdd

router = APIRouter(prefix='/categories', tags=['Категории'])

@router.get('/')
async def get_all_categories(db: db):
    query = select(CategoryModel)
    result = await db.execute(query)
    return result.scalars().all()


@router.post('/')
async def create_category(db: db, data: CategoryAdd):
    stmt = insert(CategoryModel).values(**data.model_dump())
    await db.execute(stmt)
    await db.commit()
    return {
        'status': 'ok'
    }


@router.delete('/')
async def delete_category(db: db, category_id: int):
    stmt = delete(CategoryModel).filter_by(id=category_id)
    await db.execute(stmt)
    await db.commit()
    return {
        'status': 'ok'
    }