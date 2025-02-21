from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update,insert
from models.models import abuturen_users
from settings import IQROMIND_TEST_BOT_SECRET_KEY
from database import get_async_session
from .schemas import AbuturentUsers,TestSchema
from .yordamchi import generate_id

iqromind_users_router = APIRouter()


@iqromind_users_router.post("/register/{bot_secret_key}")
async def create_user(
    bot_secret_key: str, 
    user: AbuturentUsers, 
    session: AsyncSession = Depends(get_async_session)
):
    """
    Yangi foydalanuvchini ro'yxatdan o'tkazish API endpointi.
    
    Ushbu funksiya quyidagi vazifalarni bajaradi:
      1. Kiritilgan bot secret key'ni tekshiradi; agar noto'g'ri bo'lsa, 403 xatolik qaytaradi.
      2. Kiritilgan tg_id asosida foydalanuvchi mavjudligini tekshiradi.
         Agar mavjud bo'lsa, 400 xatolik bilan foydalanuvchi allaqachon ro'yxatdan o'tganligini bildiradi.
      3. Unikal identifikator (abuturent_id) yaratadi va yangi foydalanuvchini bazaga qo'shadi.
      4. Bazaga qo'shilgandan so'ng, o'zgarishlarni commit qiladi va foydalanuvchi yaratilgani haqida tasdiq xabari qaytaradi.
      
    Parametrlar:
      - bot_secret_key (str): Bot secret key, API ga ruxsat berish uchun ishlatiladi.
      - user (AbuturentUsers): Ro'yxatdan o'tkazilayotgan foydalanuvchining ma'lumotlarini o'z ichiga oladi.
      - session (AsyncSession): Asinxron SQLAlchemy sessiyasi (dependency orqali olinadi).
    
    Qaytariladigan qiymat:
      - dict: Foydalanuvchi muvaffaqiyatli yaratilganligini bildiruvchi xabar va yaratilgan foydalanuvchining unikal ID'si.
    
    Izoh:
      - tg_id ustuniga UNIQUE va INDEX qo'shilgani sababli, 
        "select(...).filter_by(tg_id=user.tg_id)" qidiruvi PostgreSQL tomonidan B-Tree indeks orqali optimal bajariladi.
    """
    
    # Bot secret key ni tekshirish
    if bot_secret_key != IQROMIND_TEST_BOT_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Bot secret key not valid")
    
    # tg_id bo'yicha mavjud foydalanuvchini tekshiramiz (indeks orqali tez qidiruv amalga oshiriladi)
    result = await session.execute(select(abuturen_users).filter_by(tg_id=user.tg_id))
    existing_user = result.scalar()
    if existing_user:
        raise HTTPException(status_code=400, detail="Bunaqa foydalanuvchi mavjud!")
    
    # Unikal identifikator yaratish (MongoDB _id ga o'xshash tarzda)
    unical_id = generate_id()
    
    # Yangi foydalanuvchini bazaga qo'shamiz
    await session.execute(
        insert(abuturen_users).values(
            abuturent_id=unical_id,
            first_name=user.first_name,
            tg_id=user.tg_id,
        )
    )
    
    # O'zgarishlarni bazaga commit qilamiz
    await session.commit()
    
    # Foydalanuvchi yaratildi degan xabar va yaratilgan foydalanuvchining unikal ID'sini qaytaramiz
    return {"message": "Foydalanuvchi qo'shildi", "user_id": unical_id}

# check user api
@iqromind_users_router.get("/check-user/{tg_id}")
async def check_user_by_tg_id(tg_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Berilgan tg_id asosida foydalanuvchini tekshiruvchi endpoint.
    
    1. Abuturent_users jadvalidan tg_id bo‘yicha foydalanuvchi qidiriladi.
    2. Agar foydalanuvchi topilsa, foydalanuvchi ma'lumotlari va "exists": True qaytariladi.
    3. Agar topilmasa, "exists": False va mos xabar qaytariladi.
    """
    # tg_id bo‘yicha foydalanuvchini qidirish
    result = await session.execute(select(abuturen_users).filter_by(tg_id=tg_id))
    user = result.fetchone()
    
    if user:
        return {"mes": True,"abuturent_id": user.abuturent_id,}
    else:
        return {"mes": False, "message": "Foydalanuvchi topilmadi"}
  

# add test
@iqromind_users_router.patch("/users/{user_id}/tests")
async def add_test_to_user(
    user_id: str,
    new_test: TestSchema,
    session: AsyncSession = Depends(get_async_session)
):
    # Foydalanuvchini qidirish (abuturent_id orqali)
    result = await session.execute(select(abuturen_users).filter_by(abuturent_id=user_id))
    user = result.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    
    # Hozirgi testlar ro'yxatini olish
    current_tests = user.testlar.get("testlar")
    
    # Yangi test obyektini qo'shish
    # Agar siz butun obyektni qo'shmoqchi bo'lsangiz, new_test.dict() dan foydalaning:
    current_tests.append(new_test.dict())
    
    # Bazani yangilash
    await session.execute(
        update(abuturen_users)
        .where(abuturen_users.c.abuturent_id == user_id)
        .values(testlar={"testlar": current_tests})
    )
    await session.commit()
    
    return {"message": "Yangi test qo'shildi", "tests": current_tests}

# get tests by user_id
@iqromind_users_router.get("/get_tests/{user_id}/tests")
async def get_tests_by_user_id(
    user_id: str, 
    session: AsyncSession = Depends(get_async_session)
):
    """
    Berilgan user_id bo‘yicha foydalanuvchining testlar ro‘yxatini qaytaruvchi endpoint.
    
    1. Avval, abuturent_users jadvalidan user_id (abuturent_id) bo‘yicha foydalanuvchi qidiriladi.
    2. Agar foydalanuvchi topilmasa, 404 xato qaytariladi.
    3. Agar topilsa, testlar JSONB maydonidagi "testlar" ro‘yxati olinadi.
    4. Testlar ro‘yxati client-ga qaytariladi.
    """
    # Foydalanuvchini abuturent_id bo‘yicha qidirish
    result = await session.execute(
        select(abuturen_users).filter_by(abuturent_id=user_id)
    )
    user = result.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    
    # Testlar maydonidagi "testlar" ro'yxatini olish (default bo'lsa bo'sh ro'yxat qaytariladi)
    tests = user.testlar.get("testlar")
    
    return tests

