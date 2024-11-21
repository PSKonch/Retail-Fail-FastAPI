from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.core.setting import settings

engine = create_async_engine(url=settings.POSTGRES_URL)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
    async with async_session_maker() as db:
        yield db

database = Annotated[AsyncSession, Depends(get_db)]

class Base(DeclarativeBase):
    pass