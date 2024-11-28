from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

class User(Document):
    name: str
    email: str

    class Settings:
        collection = "users"

async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.my_database, document_models=[User])

# Использование
async def create_user():
    user = User(name="Dimitriy", email="dimitriy@example.com")
    await user.insert()