from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.db.mongodb.manager import mongodb_manager
from src.db.redis.manager import redis_manager

from src.api.endpoints.categories import router as categories_router
from src.api.endpoints.products import router as products_router
from src.api.endpoints.auth import router as auth_router
from src.api.endpoints.cart import router as cart_router
from src.api.endpoints.orders import router as order_router
from src.api.endpoints.payments import router as payment_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongodb_manager.connect()
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi_cache")
    
    try:
        await redis_manager.redis.ping()
        print("Redis connection is successful!")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")

    yield
    await mongodb_manager.close()
    await redis_manager.close()

app = FastAPI(lifespan=lifespan, title='Retail Fail API', version='0.5.1')

app.include_router(categories_router)
app.include_router(products_router)
app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(payment_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)