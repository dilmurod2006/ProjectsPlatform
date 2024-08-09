from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from settings import PRODUCT_ID
from sqlalchemy import(
    select,
    update,
    delete,
    insert
)

from .schemes import (
    BuySerializer
)

from models.models import (
    users,
    products,
    pckundalikcom,
    mobilekundalikcom,
    reportsbalance
)

from .utils import *

from database import get_async_session

kundalik_router = APIRouter()

@kundalik_router.post("/buy")
async def buy_api(
        data: BuySerializer,
        session: AsyncSession = Depends(get_async_session)
    ):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    res = await session.execute(select(products).filter_by(id = int(PRODUCT_ID)))
    prices = res.fetchone().settings
    all_months_price = months_size_price(month_chegirma=prices["pc_chegirma_price"], month_price=prices["price_pc"], months_count=int(data.months_count))
    if user.balance >= all_months_price:
        now = datetime.utcnow()
        res = await session.execute(
            select(pckundalikcom).filter_by(user_id = user.id)
        )
        user_check = res.fetchone()
        print(user_check)
        if user_check is None:
            await session.execute(
                insert(pckundalikcom).values(
                    user_id = user.id,
                    start_active_date = now,
                    end_use_date = now,
                    end_active_date = now + timedelta(days=30)
                )
            )
        else:
            await session.execute(
                insert(pckundalikcom).values(
                    user_id = user.id,
                    start_active_date = now,
                    end_active_date = user_check.end_active_date + timedelta(days=30*data.months_count)
                )
            )
        await session.execute(update(users).where(users.c.token == data.token).values(balance = user.balance-all_months_price))
        await session.execute(insert(reportsbalance).values(
            user_id=user.id,
            balance=user.balance-all_months_price,
            size=all_months_price
        ))
        await session.commit()
        return {
            "how": True,
            "message": "To‘muvaffaqiyatli amalga oshirildi"
        }
    else:
        return {
            "how": False,
            "message": "Mablag‘ yetarli emas!"
        }

    