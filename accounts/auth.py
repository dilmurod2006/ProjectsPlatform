import os
import secrets
import jwt
from datetime import datetime, timedelta

from .schemes import TokenRequest, CreateUser
from database import get_async_session
from models.models import users, forregister

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

from .utils import generate_token_for_orregister



accounts_rotures = APIRouter()


# generate token for forregister
@accounts_rotures.post("/generate-token")
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

