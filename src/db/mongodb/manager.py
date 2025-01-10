from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.models.order_history import OrderHistory
from src.core.setting import settings


class MongoDBManager:
    def __init__(self, url: str):
        self.url = url
        self.client = None
        self.db = None

    async def connect(self):
        self.client = AsyncIOMotorClient(self.url)
        self.db = self.client.get_database()
        await init_beanie(database=self.db, document_models=[OrderHistory])

    async def close(self):
        if self.client:
            self.client.close()

mongodb_manager = MongoDBManager(url=settings.MONGO_URL)