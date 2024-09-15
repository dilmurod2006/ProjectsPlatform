
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import(
    select,
    delete
)
from fastapi import Depends, HTTPException
from typing import Dict
from models.models import loginsdata
def months_size_price(months_count: int, month_price: int, month_chegirma: int) -> int:
    months_count = months_count - (months_count//12)*3
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
