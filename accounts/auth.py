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

# Generate token for forregister
@accounts_routers.post("/for_register_bot_api")
async def generate_token_forregister(
    data: TokenRequest, 
    session: AsyncSession = Depends(get_async_session)
):
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
    jwt_token_data = {
        "username": data.tg_id,
        "password": data.phone
            }
    token = generate_token_for_forregister(jwt_token_data)

    query = insert(forregister).values(
        tg_id=data.tg_id,
        phone=data.phone,
        token=token
    )

    await session.execute(query)
    await session.commit()

    return {"token": token}

# Create user with token
@accounts_routers.post("/create-user")
async def create_user(data: CreateUser, session: AsyncSession = Depends(get_async_session)):
    query = select(forregister).filter_by(token=data.token)
    result = await session.execute(query)
    data_forregister = result.fetchone()

    # Tokenni tekshirish
    if data_forregister is None:
        raise HTTPException(status_code=404, detail="Invalid token")

    try:
        payload = verify_jwt_token(data_forregister.token)
    except HTTPException as e:
        if e.detail == "Token has expired":
            # Token eskirgan bo'lsa, uni o'chirish
            delete_query = delete(forregister).where(forregister.c.token == data.token)
            await session.execute(delete_query)
            await session.commit()
            raise HTTPException(status_code=400, detail="Token has expired")
        else:
            raise e

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

    delete_query = delete(forregister).where(forregister.c.token == data.token)
    await session.execute(delete_query)
    await session.execute(query)
    await session.commit()

    return {"message": "User created!",}


# LOGIN SYSTEM

@accounts_routers.post("/login")
async def login(data: LoginUser, session: AsyncSession = Depends(get_async_session)):
    # Foydalanuvchi mavjudligini tekshirish
    query = select(users).where(users.c.username == data.username)
    result = await session.execute(query)
    user = result.fetchone()
    
    if user is None or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # Tokenni tekshirish
    try:
        payload = verify_jwt_token(user.token)
    except HTTPException as e:
        if e.detail == "Token has expired":
            # Token eskirgan bo'lsa, yangi token yaratish
            jwt_token_data = {
                "username": data.username,
                "password": user.password
            }
            new_token = generate_token_for_users(jwt_token_data)

            # Tokenni yangilash
            query = update(users).where(users.c.username == data.username).values(token=new_token)
            await session.execute(query)
            await session.commit()
        else:
            raise e

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

    return {"message": "parolni qayta tiklash kodi yuborildi"}


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
