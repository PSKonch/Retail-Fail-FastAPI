from fastapi import FastAPI

from src.api.endpoints.categories import router as categories_router
from src.api.endpoints.products import router as products_router
from src.api.endpoints.auth import router as auth_router

app = FastAPI()

app.include_router(categories_router)
app.include_router(products_router)
app.include_router(auth_router)