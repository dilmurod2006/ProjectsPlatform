import os
import random
from datetime import datetime, timedelta


from .schemes import (
    TokenRequest,
    CreateUser,
    LoginUser,
    CheckLogin,
    ChangePassword,
    ResetPassword,
    ResetPasswordRequest
)

from database import get_async_session
from models.models import users, forregister

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, HTTPException
from passlib.context import CryptContext


from .utils import (
    hash_password,
    verify_password,
    generate_token_for_forregister,
    generate_token_for_users,
    send_login_code,
    verify_jwt_token,
    send_reset_password_code
)




accounts_routers = APIRouter()


# generate token for forregister
@accounts_routers.post("/for_register_bot_api")
async def generate_token_forregister(data: TokenRequest, session: AsyncSession = Depends(get_async_session)):
    
    token = generate_token_for_forregister()
    # expires_at modeliga 15 daqiqa qoshiladi
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

    hashed_password = hash_password(data.password)

     # JWT token yaratish
    jwt_token_data = {
        "username": data.username,
        "password": hashed_password
    }
    jwt_token = generate_token_for_users(jwt_token_data)

    query = insert(users).values(
        full_name=data.full_name,
        sex=data.sex,
        email=data.email,
        phone=data_forregister.phone,
        username=data.username,
        password=hashed_password,
        tg_id=data_forregister.tg_id,
        token=jwt_token
    )

    delete_query = delete(forregister).where(forregister.c.token == token)
    await session.execute(delete_query)
    await session.execute(query)
    await session.commit()

    return {"message": "User created!",}


# LOGIN SYSTEM

@accounts_routers.post("/login")
async def login(data: LoginUser, session: AsyncSession = Depends(get_async_session)):
    """
    Foydalanuvchini login qilish va tasdiqlash kodi yaratish.

    Args:
        data (LoginUser): Login uchun username va password.

    Raises:
        HTTPException: Agar username yoki password noto'g'ri bo'lsa.

    Returns:
        dict: Yaratilgan kodni o'z ichiga olgan lug'at.
    """
    # Foydalanuvchi mavjudligini tekshirish
    query = select(users).where(users.c.username == data.username)
    result = await session.execute(query)
    user = result.fetchone()
    
    if user is None or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # Tasdiqlash kodi yaratish
    code = random.randint(100000, 999999)  # 6 xonali kod
    query = update(users).where(users.c.username == data.username).values(code=code)
    await session.execute(query)
    await session.commit()

    send_code = send_login_code(user.tg_id, code)

    return {"message": send_code}


# cheack code for login
@accounts_routers.post("/check-login-code")
async def check_code(data: CheckLogin, session: AsyncSession = Depends(get_async_session)):
    query = select(users).where(users.c.username == data.username)
    result = await session.execute(query)
    user = result.fetchone()

    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    if user.code != data.code:
        raise HTTPException(status_code=400, detail="Invalid code")

    query = update(users).where(users.c.username == data.username).values(code=None)
    await session.execute(query)
    await session.commit()

    # return users.token    
    return {"message": "Code is valid and user logged in", "token": user.token}


# reset password request
@accounts_routers.post("/change-password-request")
async def reset_password_request(token: str, data: ChangePassword, session: AsyncSession = Depends(get_async_session)):
    payload = verify_jwt_token(token)
    
    # Token orqali foydalanuvchi ma'lumotlarini olish
    query = select(users).where(users.c.username == payload["username"])
    result = await session.execute(query)
    user = result.fetchone()

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid token")

    if not verify_password(data.last_password, user.password):
        raise HTTPException(status_code=400, detail="eski parolingiz xato")

    hashed_password = hash_password(data.new_password)

    query = update(users).where(users.c.username == payload["username"]).values(password=hashed_password)
    await session.execute(query)
    await session.commit()

    return {"message": "Password changed successfully"}

# reset password request
@accounts_routers.post("/reset-password-request")
async def reset_password_request(data: ResetPasswordRequest, session: AsyncSession = Depends(get_async_session)):
    query = select(users).where(users.c.username == data.username)
    result = await session.execute(query)
    user = result.fetchone()

    if user is None:
        raise HTTPException(status_code=400, detail="User not found")

    code = random.randint(100000, 999999)  # 6 xonali kod
    query = update(users).where(users.c.username == data.username).values(reset_code=code)
    await session.execute(query)
    await session.commit()

    send_code = send_reset_password_code(user.tg_id, code)

    return {"message": send_code}


# reset password
@accounts_routers.post("/reset-password")
async def reset_password(data: ResetPassword, session: AsyncSession = Depends(get_async_session)):
    query = select(users).where(users.c.username == data.username)
    result = await session.execute(query)
    user = result.fetchone()

    if user is None:
        raise HTTPException(status_code=400, detail="User not found")

    if user.reset_code != data.reset_code:
        raise HTTPException(status_code=400, detail="Invalid reset code")

    hashed_password = hash_password(data.password)

    query = update(users).where(users.c.username == data.username).values(password=hashed_password, reset_code=None)
    await session.execute(query)
    await session.commit()

    return {"message": "Parol muvaffaqiyatli o'zgartirildi"}

# GET DATA FUNCTIONS FROM DATABASES START


# About users get data
@accounts_routers.post("/about-account")
async def about_account(token: str, session: AsyncSession = Depends(get_async_session)):
    """
    Foydalanuvchi haqida ma'lumot olish va token muddati tekshiruvi.

    Args:
        token (str): JWT token.

    Raises:
        HTTPException: Agar token noto'g'ri yoki muddati o'tgan bo'lsa.

    Returns:
        dict: Foydalanuvchi ma'lumotlarini o'z ichiga olgan lug'at.
    """
    # Tokenni tekshirish
    payload = verify_jwt_token(token)
    
    # Token orqali foydalanuvchi ma'lumotlarini olish
    query = select(users).where(users.c.username == payload["username"])
    result = await session.execute(query)
    user = result.fetchone()

    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Token muddati o'tmagan bo'lsa, foydalanuvchi ma'lumotlarini qaytarish
    return {
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "sex": user.sex,
        "tg_id": user.tg_id,
        "balance": user.balance
    }



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

