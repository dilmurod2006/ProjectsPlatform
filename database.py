# conect Databases 
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient

from settings import (
    DB_NAME,
    DB_PORT,
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    )

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# MONGODB setting database
# client = AsyncIOMotorClient(MONGO_DB_HOST)
MONGO_URL = "mongodb://localhost:27017/abuturent"
client = AsyncIOMotorClient(MONGO_URL)
database = client["abuturent"]

users_collection = database["users"]


