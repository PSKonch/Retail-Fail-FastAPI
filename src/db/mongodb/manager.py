from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pymongo import MongoClient
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
        print("MongoDB (async) connection is successful!")

    async def close(self):
        if self.client:
            self.client.close()
            print("MongoDB (async) connection closed.")

    def connect_sync(self):
        self.sync_client = MongoClient(self.url)
        self.sync_db = self.sync_client.get_database()
        print("MongoDB (sync) connection is successful!")

    def close_sync(self):
        if self.sync_client:
            self.sync_client.close()
            print("MongoDB (sync) connection closed.")

mongodb_manager = MongoDBManager(url=settings.MONGO_URL)