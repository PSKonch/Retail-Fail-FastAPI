from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session


    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, *filters, **filter_by):
        query = select(self.model).filter(*filters).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().first()  # Возвращает первый объект или None
        return self.mapper.map_to_domain_entity(model) if model else None
    
    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)
    
    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)

    async def update(self, *filters, **values):
        query = (
            update(self.model)
            .filter(*filters)
            .values(**values)
        )
        await self.session.execute(query)

  
        
        
        