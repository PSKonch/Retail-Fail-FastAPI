from src.repositories.order import OrderRepository
from src.repositories.order_item import OrderItemRepository
from src.repositories.products import ProductRepository
from src.repositories.cart import CartRepository
from src.repositories.categories import CategoryRepository
from src.repositories.users import UserRepository

class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.product = ProductRepository(self.session)
        self.cart = CartRepository(self.session)
        self.category = CategoryRepository(self.session)
        self.order = OrderRepository(self.session)
        self.order_item = OrderItemRepository(self.session)
        self.user = UserRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
