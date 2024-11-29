from typing import Annotated

from fastapi import Depends

from src.db.postgres.database import async_session_maker
from src.repositories.products import ProductRepository
from src.repositories.cart import CartRepository

class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.product = ProductRepository(self.session)
        self.cart = CartRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
