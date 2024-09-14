# conect Databases 
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import aioredis

from settings import (
    DB_NAME,
    DB_PORT,
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    REDIS_HOST,
    REDIS_PORT
    )

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_redis():
    redis = await aioredis.create_redis_pool((REDIS_HOST, REDIS_PORT), minsize=10, maxsize=20)
    return redis
