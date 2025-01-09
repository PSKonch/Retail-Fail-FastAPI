from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import configure_mappers

from src.core.setting import settings

engine = create_async_engine(url=settings.POSTGRES_URL)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
    async with async_session_maker() as db:
        yield db

database = Annotated[AsyncSession, Depends(get_db)]

SYNC_DATABASE_URL = settings.POSTGRES_URL.replace("asyncpg", "psycopg2")
sync_engine = create_engine(SYNC_DATABASE_URL)
SessionLocal = sessionmaker(bind=sync_engine)

configure_mappers()

class Base(DeclarativeBase):
    pass