from typing import Annotated

from fastapi import Depends
from src.db.postgres.database import get_db, AsyncSession
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

def get_db_manager(db: Annotated[AsyncSession, Depends(get_db)]) -> DBManager:
    return DBManager(db)

db_manager = Annotated[DBManager, Depends(get_db_manager)]