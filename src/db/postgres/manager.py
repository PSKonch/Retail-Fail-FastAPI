from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.db.postgres.database import get_db, AsyncSession, async_session_maker
from src.repositories.products import ProductRepository

class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.product = ProductRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

db_manager = Annotated[DBManager, Depends(get_db)]
