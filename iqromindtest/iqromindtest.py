from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from settings import IQROMINDTEST_ID

from sqlalchemy import(
    select,
    update,
    delete,
    insert
)

from .schemes import (
    BuySerializer,
    PriceSerializer,
    CheckPcSerializer,
    GetHaveTestMonthsSerializer,
    GetTestDatasInMonthSerializer,
)

from models.models import (
    users,
    products,
    reportsbalance,
    iqromindtest,
    iqrominddevices
)

from .utils import *

from database import get_async_session

iqromind_router = APIRouter()





######  D E S K T O P  ######

@iqromind_router.post("/buy")
async def buy_api(data: BuySerializer,session: AsyncSession = Depends(get_async_session)):
    # Userni qidirish
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()

    # User mavjud bulmasa
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    
    # Product narxalarini olish
    res = await session.execute(select(products).filter_by(id = int(IQROMINDTEST_ID)))
    prices = res.fetchone().settings
    
    # Barcha narxlar olindi
    all_months_price = months_size_price(month=prices["month"], year=prices["year"], months_count=int(data.months_count))

    if user.balance >= all_months_price > 0:
        now = datetime.utcnow()
        res = await session.execute(
            select(iqromindtest).filter_by(user_id = user.id)
        )
        user_check = res.fetchone()
        if user_check is None:
            await session.execute(
                insert(iqromindtest).values(
                    user_id = user.id,
                    end_use_date = now,
                    end_premium_date = now + timedelta(days=30*data.months_count)
                )
            )
        else:
            await session.execute(
                update(iqromindtest).filter_by(id=user_check.id).values(
                    user_id = user.id,
                    end_use_date = now,
                    end_premium_date = max(user_check.end_premium_date, now) + timedelta(days=30*data.months_count)
                )
            )
        await session.execute(update(users).where(users.c.token == data.token).values(balance = user.balance-all_months_price))
        await session.execute(insert(reportsbalance).values(
            user_id=user.id,
            balance=user.balance-all_months_price,
            tulov_summasi=-all_months_price,
            bio="For product: Kundalikcom"
        ))
        await session.commit()
        return {
            "how": True,
            "message": "To‘lov muvaffaqiyatli amalga oshirildi"
        }
    elif all_months_price <= 0:
        return {
            "how": False,
            "message": "Noto'g'ri qiymat kiritildi"
        }
    else:
        return {
            "how": False,
            "message": "Mablag‘ yetarli emas!"
        }

@iqromind_router.post("/price_months")
async def price_months_api(data: PriceSerializer, session: AsyncSession = Depends(get_async_session)):
    """Oy soniga mos keluvchi narxni qaytaruvchi api
    masalan: 1 oy -> 30 000 `so'm`"""

    # narxlarni databasedan olish
    res = await session.execute(select(products).filter_by(id = int(IQROMINDTEST_ID)))
    prices = res.fetchone().settings

    # jami summani hisoblab qaytarish
    all_months_price = months_size_price(month=prices["month"], year=prices["year"], months_count=int(data.months_count))
    return all_months_price



# Qurilmani va premiumni tekshirib natija qaytarish
@iqromind_router.post("/check_pc")
async def check_pc_api(data: CheckPcSerializer,session: AsyncSession = Depends(get_async_session)):
    # token orqali userni qidirish
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")

    # hozirgi vaqtni aniqlash
    now = datetime.utcnow()

    # kundalikcomdan userni qidirish
    res = await session.execute(select(iqromindtest).filter_by(user_id=user.id))
    qmtest_user = res.fetchone()

    # Kundalik komda user mavjudmi?
    if qmtest_user is None:
        # mavjud emas, Qo'shadi
        await session.execute(
            insert(iqromindtest).values(
                user_id = user.id,
                end_use_date = now,
                device_id=data.device_id,
                end_premium_date = now
            )
        )
        await session.commit()
        return {
            "how": True,
            "end_premium_date": now,
            "size": timedelta(days=0),
        }

    elif qmtest_user.device_id == data.device_id:
        await session.execute(update(iqromindtest).filter_by(id = qmtest_user.id).values(end_use_date = now))
        await session.commit()
        return {
            "how": True,
            "end_premium_date": qmtest_user.end_premium_date,
            "size": qmtest_user.end_premium_date-now
        }
    elif (now - qmtest_user.end_use_date).days >= 2 or qmtest_user.device_id == None:
        await session.execute(update(iqromindtest).filter_by(id = qmtest_user.id).values(end_use_date = now, device_id=data.device_id))
        await session.commit()
        return {
            "how": True,
            "end_premium_date": qmtest_user.end_premium_date,
            "size": qmtest_user.end_premium_date-now
        }
    delta = timedelta(days=2)-(now - qmtest_user.end_use_date)
    total_hours = delta.days * 24 + delta.seconds // 3600
    return {
        "how": False,
        "message": f"Boshqa qurilmadan kirilgan.\nBoshqa qurulmangizdan {total_hours} soat mobaynida foydalanmang. Keyin bu qurulmaga login qilib foydalanishingiz mumkin"
    }

# userning testlari mavjud oylarni qaytaradi
@iqromind_router.post("/get_have_test_months")
async def get_tests_api(data: GetHaveTestMonthsSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    res = await session.execute(select(iqromindtest).filter_by(user_id=user.id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    
    return list(qmtest_user.testlar.keys())

# 1 oylik testlarni qaytaradi
@iqromind_router.post("/get_test_datas_in_month")
async def get_test_data_api(data: GetTestDatasInMonthSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    res = await session.execute(select(iqromindtest).filter_by(user_id=user.id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    return qmtest_user.testlar[data.month_date] if data.month_date in qmtest_user.testlar else {}



