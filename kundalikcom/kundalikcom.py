from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
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
    BuySerializer,
    PriceSerializer,
    CheckPcSerializer,
    RegisterLoginsSerializer,
    SetSchoolSerializer,
    GetSchoolSerializer
)

from models.models import (
    users,
    products,
    pckundalikcom,
    mobilekundalikcom,
    reportsbalance,
    school_data
)

from .utils import *

from database import get_async_session

kundalik_router = APIRouter()





######  D E S K T O P  ######

@kundalik_router.post("/buy")
async def buy_api(data: BuySerializer,session: AsyncSession = Depends(get_async_session)):
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
        if user_check is None:
            await session.execute(
                insert(pckundalikcom).values(
                    user_id = user.id,
                    start_active_date = now,
                    end_use_date = now,
                    end_active_date = now + timedelta(days=30*data.months_count)
                )
            )
        else:
            await session.execute(
                update(pckundalikcom).filter_by(id=user_check.id).values(
                    user_id = user.id,
                    start_active_date = now,
                    end_use_date = now,
                    end_active_date = now + timedelta(days=30*data.months_count)
                )
            )
        await session.execute(update(users).where(users.c.token == data.token).values(balance = user.balance-all_months_price))
        await session.execute(insert(reportsbalance).values(
            user_id=user.id,
            balance=user.balance-all_months_price,
            size=all_months_price,
            bio="For product: Kundalikcom"
        ))
        await session.commit()
        return {
            "how": True,
            "message": "To‘lov muvaffaqiyatli amalga oshirildi"
        }
    else:
        return {
            "how": False,
            "message": "Mablag‘ yetarli emas!"
        }

@kundalik_router.post("/price_months")
async def price_months_api(data: PriceSerializer, session: AsyncSession = Depends(get_async_session)):
    """Oy soniga mos keluvchi narxni qaytaruvchi api
    masalan: 1 oy -> 250 000 `so'm`"""

    # narxlarni databasedan olish
    res = await session.execute(select(products).filter_by(id = int(PRODUCT_ID)))
    prices = res.fetchone().settings

    # jami summani hisoblab qaytarish
    all_months_price = months_size_price(month_chegirma=prices["pc_chegirma_price"], month_price=prices["price_pc"], months_count=int(data.months_count))
    return all_months_price




@kundalik_router.post("/check_pc")
async def check_pc_api(data: CheckPcSerializer,session: AsyncSession = Depends(get_async_session)):
    # token orqali userni qidirish
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        return HTTPException("Bunday user mavjud emas!")

    # hozirgi vaqtni aniqlash
    now = datetime.utcnow()

    # kundalikcomdan userni qidirish
    res = await session.execute(select(pckundalikcom).filter_by(user_id=user.id))
    kundalik_user = res.fetchone()

    # Kundalik komda user mavjudmi?
    if kundalik_user is None:
        # mavjud emas, Qo'shadi hamda 7 kunga active qilib beradi
        await session.execute(
            insert(pckundalikcom).values(
                user_id = user.id,
                start_active_date = now,
                end_use_date = now,
                device_id=data.device_id,
                end_active_date = now + timedelta(days=7)
            )
        )
        await session.commit()
        return {
            "how": True,
            "end_active_date": now + timedelta(days=7),
            "size": timedelta(days=7),
        }

    elif kundalik_user.device_id == data.device_id:
        await session.execute(update(pckundalikcom).filter_by(id = kundalik_user.id).values(end_use_date = now))
        all_logins = await get_user_logins(kundalik_user.user_id, session)
        await session.commit()
        return {
            "how": True,
            "end_active_date": kundalik_user.end_active_date,
            "size": kundalik_user.end_active_date-now,
            "all_logins": all_logins
        }
    elif (now - kundalik_user.end_use_date).days >= 2 or kundalik_user.device_id == None:
        await session.execute(update(pckundalikcom).filter_by(id = kundalik_user.id).values(end_use_date = now, device_id=data.device_id))
        all_logins = await get_user_logins(kundalik_user.user_id, session)
        await session.commit()
        return {
            "how": True,
            "end_active_date": kundalik_user.end_active_date,
            "size": kundalik_user.end_active_date-now,
            "all_logins": all_logins
        }
    delta = timedelta(days=2)-(now - kundalik_user.end_use_date)
    total_hours = delta.days * 24 + delta.seconds // 3600
    return {
        "how": False,
        "message": f"Boshqa qurilmadan kirilgan.\nBoshqa qurulmangizdan {total_hours} soat mobaynida foydalanmang. Keyin bu qurulmaga login qilib foydalanishingiz mumkin"
    }





@kundalik_router.post("/register_logins/{user_id}")
async def register_logins(user_id: int, data: RegisterLoginsSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(pckundalikcom).filter_by(user_id=user_id))
    kundalik_user = res.fetchone()
    if kundalik_user is not None:
        await session.execute(insert(loginsdata).values(
            user_id=user_id,
            login=data.login,
            password=data.password
        ))
        await session.commit()
        return True
    return False


@kundalik_router.post("/set_school")
async def set_school_api(data: SetSchoolSerializer,session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).filter_by(token=data.token))
    user = res.fetchone()
    if user is None:
        return HTTPException("User mavjud emas!")
    res = await session.execute(select(pckundalikcom).filter_by(user_id=user.id))
    kundalik_user = res.fetchone()
    if kundalik_user is None:
        return HTTPException("User mavjud emas!")

    res = await session.execute(select(school_data).filter_by(user_id=user.id))
    maktab = res.fetchone()
    if maktab is None:
        await session.execute(insert(school_data).values(
            user_id=kundalik_user.user_id,
            viloyat=data.viloyat,
            tuman=data.tuman,
            school_number=data.school_number
        ))
    await session.execute(update(school_data).filter_by(user_id=user.id).values(
        viloyat=data.viloyat,
        tuman=data.tuman,
        school_number=data.school_number
    ))
    await session.commit()
    return "Maktab ma'lumotlari muvaffaqiyatli kiritildi"
@kundalik_router.post("/get_school")
async def get_school_api(data: GetSchoolSerializer,session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).filter_by(token=data.token))
    user = res.fetchone()
    if user is None:
        return HTTPException("User mavjud emas!")
    res = await session.execute(select(pckundalikcom).filter_by(user_id=user.id))
    kundalik_user = res.fetchone()
    if kundalik_user is None:
        return HTTPException("User mavjud emas!")

    res = await session.execute(select(school_data).filter_by(user_id=user.id))
    maktab = res.fetchone()
    if maktab is None:
        return {
            "how": False,
            "message": "Maktab haqida ma'lumotlar hali kiritilmagan"
        }
    return {
        "viloyat": maktab.viloyat,
        "tuman": maktab.tuman,
        "school_number": maktab.school_number
    }




######  M O B I L E  ######

@kundalik_router.post("/buy_api_mobile")
async def buy_api_mobile_api(data: BuySerializer,session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    res = await session.execute(select(products).filter_by(id = int(PRODUCT_ID)))
    prices = res.fetchone().settings
    all_months_price = months_size_price(month_chegirma=prices["mobile_chegirma_price"], month_price=prices["price_mobile"], months_count=int(data.months_count))
    if user.balance >= all_months_price:
        now = datetime.utcnow()
        res = await session.execute(
            select(mobilekundalikcom).filter_by(user_id = user.id)
        )
        user_check = res.fetchone()
        if user_check is None:
            await session.execute(
                insert(mobilekundalikcom).values(
                    user_id = user.id,
                    start_active_date = now,
                    end_use_date = now,
                    end_active_date = now + timedelta(days=30*data.months_count)
                )
            )
        else:
            await session.execute(
                update(mobilekundalikcom).filter_by(id=user_check.id).values(
                    user_id = user.id,
                    start_active_date = now,
                    end_use_date = now,
                    end_active_date = now + timedelta(days=30*data.months_count)
                )
            )
        await session.execute(update(users).where(users.c.token == data.token).values(balance = user.balance-all_months_price))
        await session.execute(insert(reportsbalance).values(
            user_id=user.id,
            balance=user.balance-all_months_price,
            size=all_months_price,
            bio="For product: Kundalikcom Mobile"
        ))
        await session.commit()
        return {
            "how": True,
            "message": "To‘lov muvaffaqiyatli amalga oshirildi"
        }
    else:
        return {
            "how": False,
            "message": "Mablag‘ yetarli emas!"
        }

@kundalik_router.post("/price_months_mobile")
async def price_months_mobile_api(data: PriceSerializer, session: AsyncSession = Depends(get_async_session)):
    """Oy soniga mos keluvchi narxni qaytaruvchi api
    masalan: 1 oy -> 250 000 `so'm`"""

    # narxlarni databasedan olish
    res = await session.execute(select(products).filter_by(id = int(PRODUCT_ID)))
    prices = res.fetchone().settings

    # jami summani hisoblab qaytarish
    all_months_price = months_size_price(month_chegirma=prices["mobile_chegirma_price"], month_price=prices["price_mobile"], months_count=int(data.months_count))
    return all_months_price

@kundalik_router.post("/check_mobile")
async def check_mobile_api(data: CheckPcSerializer,session: AsyncSession = Depends(get_async_session)):
    # token orqali userni qidirish
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        return HTTPException("Bunday user mavjud emas!")

    # hozirgi vaqtni aniqlash
    now = datetime.utcnow()

    # kundalikcomdan userni qidirish
    res = await session.execute(select(mobilekundalikcom).filter_by(user_id=user.id))
    kundalik_user = res.fetchone()

    # Kundalik komda user mavjudmi?
    if kundalik_user is None:
        # mavjud emas, Qo'shadi hamda 7 kunga active qilib beradi
        await session.execute(
            insert(mobilekundalikcom).values(
                user_id = user.id,
                start_active_date = now,
                end_use_date = now,
                device_id=data.device_id,
                end_active_date = now + timedelta(days=7)
            )
        )
        await session.commit()
        return {
            "how": True,
            "end_active_date": now + timedelta(days=7),
            "size": timedelta(days=7),
        }

    elif kundalik_user.device_id == data.device_id:
        await session.execute(update(mobilekundalikcom).filter_by(id = kundalik_user.id).values(end_use_date = now))
        await session.commit()
        return {
            "how": True,
            "end_active_date": kundalik_user.end_active_date,
            "size": kundalik_user.end_active_date-now
        }
    elif (now - kundalik_user.end_use_date).days >= 2 or kundalik_user.device_id == None:
        await session.execute(update(mobilekundalikcom).filter_by(id = kundalik_user.id).values(end_use_date = now, device_id=data.device_id))
        await session.commit()
        return {
            "how": True,
            "end_active_date": kundalik_user.end_active_date,
            "size": kundalik_user.end_active_date-now
        }
    delta = timedelta(days=2)-(now - kundalik_user.end_use_date)
    total_hours = delta.days * 24 + delta.seconds // 3600
    return {
        "how": False,
        "message": f"Boshqa qurilmadan kirilgan.\nBoshqa qurulmangizdan {total_hours} soat mobaynida foydalanmang. Keyin bu qurulmaga login qilib foydalanishingiz mumkin"
    }


### EXE AND APK DOWNLOADING START ###

# Exe downloading
@kundalik_router.get("/download_exe_kundalikcom")
async def download_exe_kundalikcom_api():
    pass

# Apk downloading
@kundalik_router.get("/download_apk_kundalikcom")
async def download_apk_kundalikcom_api():
    pass

### EXE AND APK DOWNLOADING END ###