# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# import sys
# sys.path.append('c:/Users/dilmu/ProjectsPlatform') 
# from main import app  # Bu yerda sizning ilova asosiy faylingiz (misol uchun, main.py)
# from database import get_async_session
# from models.models import forregister
# from settings import DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_PASSWORD

# # Testing uchun TestClient'ni yaratamiz
# client = TestClient(app)

# # Test maqsadida yangi test ma'lumotlar bazasini yaratamiz
# DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# engine = create_async_engine(DATABASE_URL, echo=True)
# TestingSessionLocal = sessionmaker(
#     autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
# )

# @pytest.fixture(scope="module")
# def override_get_async_session():
#     async def _override_get_async_session():
#         async with TestingSessionLocal() as session:
#             yield session

#     app.dependency_overrides[get_async_session] = _override_get_async_session

# @pytest.fixture(autouse=True, scope="module")
# async def create_tables(override_get_async_session):
#     # Ma'lumotlar bazasidagi jadvallarni yaratish
#     async with engine.begin() as conn:
#         await conn.run_sync(forregister.metadata.create_all)

#     yield

#     # Testlardan keyin barcha jadvallarni o'chirish
#     async with engine.begin() as conn:
#         await conn.run_sync(forregister.metadata.drop_all)

# # TEST FORREGISTER START

# # test generate token forregister
# def test_generate_token_forregister(override_get_async_session):
#     # Yangi foydalanuvchi ma'lumotlarini sinab ko'ramiz
#     response = client.post(
#         "accounts/for_register_bot_api",
#         json={"tg_id": 6565635535, "phone": "+998901234567"}
#     )

#     assert response.status_code == 200
#     assert "token" in response.json()


# # TEST FORREGISTER ENDs

