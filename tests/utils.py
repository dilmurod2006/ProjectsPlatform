import sys
sys.path.append('c:/Users/dilmu/ProjectsPlatform') 
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from main import app  # Bu yerda sizning ilova asosiy faylingiz (misol uchun, main.py)
from database import get_async_session
from models.models import forregister



# Test maqsadida yangi test ma'lumotlar bazasini yaratamiz
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

@pytest.fixture(scope="module")
def override_get_async_session():
    async def _override_get_async_session():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_async_session] = _override_get_async_session

@pytest.fixture(autouse=True, scope="module")
async def create_tables(override_get_async_session):
    async with engine.begin() as conn:
        await conn.run_sync(forregister.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(forregister.metadata.drop_all)
