from sqlalchemy import insert
from src.models.users import UserModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper


class UserRepository(BaseRepository):
    model = UserModel
    mapper = UserDataMapper

    async def get_by_username(self, username: str):
        return await self.get_one_or_none(username=username)

    async def get_by_id(self, user_id: int):
        return await self.get_one_or_none(id=user_id)
    
    async def add(self, data: UserModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit() 
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)