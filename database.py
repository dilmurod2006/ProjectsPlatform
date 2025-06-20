# conect Databases 
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from settings import (
    DB_NAME,
    DB_PORT,
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    MONGODB_1_USERNAME,
    MONGODB_1_PASSWORD
    )

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session



# MONGODB setting ONLINE database1 


uri = F"mongodb+srv://dilmurodamonov006:C2VJzXPDsvwn33Ef@iqromindtestbot.1kspd.mongodb.net/?retryWrites=true&w=majority&appName=IqroMindTestBot"

# client = AsyncIOMotorClient(uri)
# Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

#database = client["IqroMindTestBot"]
# db1_collection = database["abuturent"]
























# MONGODB setting database
# client = AsyncIOMotorClient(MONGO_DB_HOST)
# MONGO_URL = "mongodb://localhost:27017/abuturent"
# client = AsyncIOMotorClient(MONGO_URL)
# database = client["abuturent"]

# users_collection = database["users"]


