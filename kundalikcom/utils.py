
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import(
    select,
    delete
)
from fastapi import Depends, HTTPException
from typing import Dict
from models.models import loginsdata
from settings import SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta
import jwt
def months_size_price(months_count: int, month_price: int, month_chegirma: int) -> int:
    if months_count < 3:
        return month_price*months_count
    return month_chegirma*months_count

async def get_user_logins(user_id: int, session: AsyncSession) -> Dict[str, str]:
    # Ma'lumotlarni olish
    result = await session.execute(select(loginsdata).filter_by(user_id=user_id))
    # Malumotlar olingandan keyin uchirib tashlash
    await session.execute(delete(loginsdata).filter_by(user_id=user_id))
    rows = result.fetchall()

    # Loginlar va parollarni dict ga saqlash
    login_password_dict = {row.login: row.password for row in rows}

    return login_password_dict


def verify_jwt_token(token: str) ->dict:
    try:
        # Tokenni dekodlash
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
        # Token muddati o'tganligini tekshirish
        exp = payload.get("exp")
        if exp is None:
            raise HTTPException(status_code=400, detail="Token does not contain expiration time")
        
        expiration_date = datetime.utcfromtimestamp(exp)
        if expiration_date < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Token has expired")
        
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")
