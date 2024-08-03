import os
import secrets
import jwt
from datetime import datetime, timedelta

from .schemes import TokenRequest, CreateUser, CheckUser
from database import get_async_session
from models.models import users, forregister

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

from .utils import generate_token_for_orregister



accounts_routers = APIRouter()


# generate token for forregister
@accounts_routers.post("/for_register_bot_api")
async def generate_token_forregister(data: TokenRequest, session: AsyncSession = Depends(get_async_session)):
    
    token = generate_token_for_orregister()
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

# check token
@accounts_routers.post("/cheack_token_api")
async def generate_token_forregister(data: CheckUser, session: AsyncSession = Depends(get_async_session)):
    query = select(forregister).filter_by(token=data.token)
    res = await session.execute(query)
    print(res)
    if res != None:
        return True
    return False
