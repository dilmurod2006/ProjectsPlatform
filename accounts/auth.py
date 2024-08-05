import os
import secrets
import jwt
from datetime import datetime, timedelta

from .schemes import TokenRequest, CreateUser
from database import get_async_session
from models.models import users, forregister

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, HTTPException
from passlib.context import CryptContext

from .utils import generate_token_for_forregister, generate_token_for_users

accounts_routers = APIRouter()

# Generate token for forregister
@accounts_routers.post("/for_register_bot_api")
async def generate_token_forregister(
    data: TokenRequest, 
    session: AsyncSession = Depends(get_async_session)
):
    """
    Foydalanuvchi uchun token yaratish va saqlash.

    Bu funksiya Telegram ID va telefon raqamini tekshiradi, agar ular mavjud bo'lmasa,
    yangi token yaratadi va `forregister` jadvaliga saqlaydi.

    Args:
        data (TokenRequest): Token yaratish uchun Telegram ID va telefon raqami.

    Raises:
        HTTPException: Agar Telegram ID yoki telefon raqami mavjud bo'lsa yoki 
        agar Telegram ID allaqachon `users` jadvalida mavjud bo'lsa.

    Returns:
        dict: Yangi yaratilgan tokenni o'z ichiga olgan lug'at.
    """
    # Telegram ID va telefon raqamlarini tekshirish
    forregister_tg_id_query = select(forregister).where(forregister.c.tg_id == data.tg_id)
    forregister_phone_query = select(forregister).where(forregister.c.phone == data.phone)
    users_tg_id_query = select(users).where(users.c.tg_id == data.tg_id)

    tg_id_result = await session.execute(forregister_tg_id_query)
    phone_result = await session.execute(forregister_phone_query)
    users_tg_id_result = await session.execute(users_tg_id_query)

    # Foydalanuvchi Telegram ID'si mavjudligini tekshirish
    if users_tg_id_result.fetchone():
        raise HTTPException(
            status_code=400, 
            detail="Bu Telegram ID orqali ro'yxatdan o'tilgan. Boshqa Telegram akkaunt orqali ro'yxatdan o'ting."
        )
    
    # Telegram ID yoki telefon raqami mavjudligini tekshirish
    if tg_id_result.fetchone():
        raise HTTPException(
            status_code=400, 
            detail="Telegram ID allaqachon mavjud."
        )
    
    if phone_result.fetchone():
        raise HTTPException(
            status_code=400, 
            detail="Telefon raqam allaqachon mavjud."
        )
    
    # Token yaratish va saqlash
    token = generate_token_for_forregister()
    expires_at = datetime.utcnow() + timedelta(minutes=15)  # 15 daqiqa

    query = insert(forregister).values(
        tg_id=data.tg_id,
        phone=data.phone,
        token=token,
        expires_at=expires_at
    )

    await session.execute(query)
    await session.commit()

    return {"token": token}

# Create user with token
@accounts_routers.post("/create-user/{token}")
async def create_user(token: str, data: CreateUser, session: AsyncSession = Depends(get_async_session)):
    query = select(forregister).filter_by(token=token)
    result = await session.execute(query)
    data_forregister = result.fetchone()
    # foregister_data = {
    #     "tg_id": user[1],
    #     "phone": user[2],
    # }

    if data_forregister is None:
        raise HTTPException(status_code=404, detail="Invalid token")

    if data_forregister.expires_at < datetime.utcnow():
        delete_query = delete(forregister).where(forregister.c.token == token)
        await session.execute(delete_query)
        await session.commit()
        raise HTTPException(status_code=400, detail="Token expired and deleted!")

    # cheack username and email
    username_query = select(users).where(users.c.username == data.username)
    email_query = select(users).where(users.c.email == data.email)

    username_result = await session.execute(username_query)
    email_result = await session.execute(email_query)

    if username_result.fetchone():
        raise HTTPException(status_code=400, detail="Username already exists in the database")

    if email_result.fetchone():
        raise HTTPException(status_code=400, detail="Email already exists in the database")

    TOKEN = generate_token_for_users()

    query = insert(users).values(
        full_name=data.full_name,
        sex=data.sex,
        email=data.email,
        phone=data_forregister.phone,
        username=data.username,
        password=data.password,
        tg_id=data_forregister.tg_id,
        token=TOKEN
    )
    delete_query = delete(forregister).where(forregister.c.token == token)
    await session.execute(delete_query)
    await session.execute(query)
    await session.commit()

    return {"message": "User created!"}


# GET DATA FUNCTIONS FROM DATABASES START

# Get all Telegram IDs from users table
@accounts_routers.get("/get_all_telegram_ids")
async def get_all_telegram_ids(session: AsyncSession = Depends(get_async_session)):
    """Bu funksiya foydalanuvchilarimizni telegram IDlarini qaytaradi.
       Bu funksiyani qilishdan maqsad foydalanuvchilarga kerakli vaqtda xabar va reklama yuborish uchun olinadi!
       Va foydalanuvchilarni doimiy statiskasini ko'rish uchun yani botdan nechta foydalanuvchi borligi va ular botni blocklamagnini tekshirish uchun olinadi.
       
       
       Funksiydan foydalanish uchun:
        /get_all_telegram_ids GET so'rovini yuborish kifoya
        
        
        respone sifatida: dict qaytadi: {"tg_ids": list} shaklida beradi bemalol olish mumkun
    """
    query = select(users.c.tg_id)
    result = await session.execute(query)
    data = result.scalars().all()  # Use scalars().all() to get a list of values
    return {"tg_ids": data}

# Get all phone numbers and full names from users table
@accounts_routers.get("/get_all_phone_numbers")
async def get_all_phone_numbers(session: AsyncSession = Depends(get_async_session)):
    """Bu funksiya foydalanuvchilarimizni hamma telefon raqamlarini va ism-familiyani qaytaradi.
       Bu funksiyani qilishdan maqsad foydalanuvchilarga kerakli vaqtda sms yuborish uchun olinadi!
       Yani sms da foydalanuvchi ism familiyasi bilan murojat qilishi uchun qilindi.
    """
    query = select(users.c.phone, users.c.full_name)
    result = await session.execute(query)
    data = result.fetchall()
    
    phone_numbers = [row[0] for row in data]
    full_names = [row[1] for row in data]
    
    return {"phone_numbers": phone_numbers, "full_names": full_names}


# GET DATA FUNCTIONS FROM DATABASES END