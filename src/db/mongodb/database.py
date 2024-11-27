from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "retail"

# Асинхронное подключение к MongoDB
client = AsyncIOMotorClient(MONGO_URI)

# Доступ к базе данных
db = client[DATABASE_NAME]

# Доступ к коллекции
collection = db["my_collection"]

# Асинхронная вставка документа
async def insert_document():
    document = {"name": "Alice", "age": 25, "city": "New York"}
    result = await collection.insert_one(document)
    print(f"Inserted document with ID: {result.inserted_id}")

# Асинхронный вызов
import asyncio
asyncio.run(insert_document())