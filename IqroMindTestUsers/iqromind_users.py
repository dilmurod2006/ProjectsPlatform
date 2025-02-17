from fastapi import APIRouter, HTTPException

from models.models import User, Test
from settings import IQROMIND_TEST_BOT_SECRET_KEY
from database import db1_collection
from .schemas import get_test_serializer

iqromind_users_router = APIRouter()


@iqromind_users_router.post("/register/{bot_secret_key}")
async def create_user(bot_secret_key: str, user: User):
    if bot_secret_key != IQROMIND_TEST_BOT_SECRET_KEY:
        raise HTTPException(status_code=400, detail="Xato secret key!")
    
    # Agar tg_id bazada mavjud bo'lsa, foydalanuvchi ro'yxatdan o'tmasligi kerak
    existing_user = await db1_collection.find_one({"tg_id": user.tg_id})
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Bunaqa foydalanuvchi mavjud!")
    
    await db1_collection.insert_one(user.dict())
    return {"message": "Foydalanuvchi qo'shildi", "user_id": str(user.tg_id)}




# add test
@iqromind_users_router.post("/addtest/{user_id}")
async def add_test(user_id: str, test: Test):
    # Foydalanuvchi mavjudligini tekshiramiz
    if await db1_collection.find_one({"user_id": user_id}):
        # test obyektini dictionary ga aylantiramiz va kerak bo'lsa user_id ni yangilaymiz:
        test.user_id = user_id  # agar kerak bo'lsa
        await db1_collection.insert_one(test.dict())
        return {"message": "Test qo'shildi"}
    else:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud emas!")


# get tests by user_id
@iqromind_users_router.get("/tests/{user_id}")
async def get_tests(user_id: str):
    cursor = db1_collection.find({"user_id": user_id})
    tests = []
    async for test in cursor:
        tests.append(get_test_serializer(test))
    return tests


