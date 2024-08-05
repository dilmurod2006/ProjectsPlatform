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
async def generate_token_forregister(data: TokenRequest, session: AsyncSession = Depends(get_async_session)):
    # tg_id va phone tekshirish
    tg_id_query = select(forregister).where(forregister.c.tg_id == data.tg_id)
    phone_query = select(forregister).where(forregister.c.phone == data.phone)
    
    tg_id_result = await session.execute(tg_id_query)
    phone_result = await session.execute(phone_query)
    
    if tg_id_result.fetchone():
        raise HTTPException(status_code=400, detail="Telegram ID already exists in the database")
    
    if phone_result.fetchone():
        raise HTTPException(status_code=400, detail="Phone number already exists in the database")
    
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