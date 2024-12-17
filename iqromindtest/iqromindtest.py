from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from settings import IQROMINDTEST_ID
import telebot
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
    AddTestSerializer,
    SetTestSerializer,
    EditTestSerializer,
    GetTestSerializer,
    DeleteTestSerializer,
    GetTestKalitlarSerializer,
    GetTestEditTokenSerializer,
    SetTestEditTokenSerializer,
    GetTestTekshirishlarSerializer,
    SetEduNameSerializer,
    SetEduBotTokenSerializer,
    SetEduLogoSerializer,
    GetEduBotTokenSerializer,

)

from models.models import (
    users,
    products,
    reportsbalance,
    iqromindtest
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

    # Kundalik comda user mavjudmi?
    if qmtest_user is None:
        # mavjud emas, Qo'shadi
        await session.execute(
            insert(iqromindtest).values(
                user_id = user.id,
                end_use_date = now,
                device_id = data.device_id,
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
    # Test user mavjud bo'sa
    return [{"key": i, "name": qmtest_user.testlar[data.month_date][i]["name"]} for i in qmtest_user.testlar[data.month_date].keys()] if data.month_date in qmtest_user.testlar else []

# Testni o'qish
@iqromind_router.post("/get_test")
async def get_test_api(data: GetTestSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    res = await session.execute(select(iqromindtest).filter_by(user_id=user.id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    # Test user mavjud bo'sa
    return {
        "name": qmtest_user.testlar[data.month_date][data.test_key]["name"],
        "bio": qmtest_user.testlar[data.month_date][data.test_key]["bio"],
        "date": qmtest_user.testlar[data.month_date][data.test_key]["date"],
        "edit_token": qmtest_user.edit_token
    }

# Test qo'shish
@iqromind_router.post("/add_test")
async def add_test(data: AddTestSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    res = await session.execute(select(iqromindtest).filter_by(user_id=user.id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        raise HTTPException(status_code=401, detail="User mavjud emas!")
    
    # Test user mavjud bo'sa
    now = datetime.utcnow()
    month_date = now.strftime("%Y%m")
    if month_date not in qmtest_user.testlar:
        qmtest_user.testlar[month_date] = dict()
    
    # yangi test yaratib olish
    new_test = create_test(data.test_name, now)
    test_key = now.strftime("%d%H%M")
    if test_key in qmtest_user.testlar[month_date]:
        return {"how": False,"message":"Hoy-hoy shoshmang...\nTestni saqlab olishim uchun 1 min vaqt bering 🙂"}
    
    # Yangi testni qo'shish
    qmtest_user.testlar[month_date][test_key] = new_test
    edit_token = generate_token()
    await session.execute(update(iqromindtest).where(iqromindtest.c.id == qmtest_user.id).values(
        testlar = qmtest_user.testlar,
        edit_token = edit_token
    ))
    await session.commit()
    result_data = new_test.copy()
    result_data.pop("javoblar")
    result_data.pop("tekshirishlar")
    result_data["edit_token"] = edit_token
    return {"how": True,"message":"✅ Testni qo'shdim 😊", "test": result_data}


# Testni javoblarini taxrirlash
@iqromind_router.post("/set_test")
async def set_test(data: SetTestSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    res = await session.execute(select(iqromindtest).filter_by(user_id=user.id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        raise HTTPException(status_code=401, detail="User mavjud emas!")
    # Test user mavjud bo'sa
    try:
        if len(data.javoblar) != 410:
            return "Testni javoblarini to'liq kiriting 🙂"
        qmtest_user.testlar[data.month_date][data.test_key]["javoblar"] = data.javoblar
        await session.execute(update(iqromindtest).where(iqromindtest.c.id == qmtest_user.id).values(
            testlar = qmtest_user.testlar
        ))
        await session.commit()
        return "Testni javoblarini eslab qoldim 😊"
    except:
        raise HTTPException(status_code=402, detail="Test mavjud emas ekan 😕")

# Testni taxrirlash
@iqromind_router.post("/edit_test")
async def set_test(data: EditTestSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    res = await session.execute(select(iqromindtest).filter_by(user_id=user.id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        raise HTTPException(status_code=401, detail="User mavjud emas!")
    # Test user mavjud bo'sa
    try:
        qmtest_user.testlar[data.month_date][data.test_key]["name"] = data.test_name
        qmtest_user.testlar[data.month_date][data.test_key]["bio"] = data.bio
        await session.execute(update(iqromindtest).where(iqromindtest.c.id == qmtest_user.id).values(
            testlar = qmtest_user.testlar
        ))
        await session.commit()
        return "Testni nomi va izohini eslab qoldim 😊"
    except:
        raise HTTPException(status_code=402, detail="Test mavjud emas ekan 😕")
@iqromind_router.post("/delete_test")
async def delete_test(data: DeleteTestSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    res = await session.execute(select(iqromindtest).filter_by(user_id=user.id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        raise HTTPException(status_code=401, detail="User mavjud emas!")
    # Test user mavjud bo'sa
    try:
        del qmtest_user.testlar[data.month_date][data.test_key]
        await session.execute(update(iqromindtest).where(iqromindtest.c.id == qmtest_user.id).values(
            testlar = qmtest_user.testlar
        ))
        await session.commit()
        return "Testni o'chirdim 😊"
    except:
        raise HTTPException(status_code=402, detail="Test mavjud emas ekan 😕")

@iqromind_router.post("/get_test_kalitlar")
async def get_test_kalitlar(data: GetTestKalitlarSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    res = await session.execute(select(iqromindtest).filter_by(user_id=user.id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        raise HTTPException(status_code=401, detail="User mavjud emas!")
    try:
        if data.test_key not in qmtest_user.testlar[data.month_date]:
            raise HTTPException(status_code=402, detail="Test mavjud emas ekan 😕")
        return qmtest_user.testlar[data.month_date][data.test_key]["javoblar"]
    except:
        raise HTTPException(status_code=402, detail="Test mavjud emas ekan 😕")

@iqromind_router.post("/get_test_tekshirishlar")
async def get_test_tekshirishlar(data: GetTestTekshirishlarSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    res = await session.execute(select(iqromindtest).filter_by(user_id=user.id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        raise HTTPException(status_code=401, detail="User mavjud emas!")
    try:
        if data.test_key not in qmtest_user.testlar[data.month_date]:
            raise HTTPException(status_code=402, detail="Test mavjud emas ekan 😕")
        return qmtest_user.testlar[data.month_date][data.test_key]["tekshirishlar"]
    except:
        raise HTTPException(status_code=402, detail="Test mavjud emas ekan 😕")

# Testni kalitlarini edit token bilan olish
@iqromind_router.post("/get_test_edit_token")
async def get_test_edit_token(data: GetTestEditTokenSerializer, session: AsyncSession = Depends(get_async_session)):
    try:
        edit_token = data.edit_token[:4]+data.edit_token[:-4]
        f_id = int(data.edit_token[4:-4])
    except:
        return "Bu link eskirgan"
    
    res = await session.execute(select(iqromindtest).filter_by(user_id=data.user_id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        return "Bu link eskirgan"
    if edit_token != qmtest_user.edit_token:
        return "Bu link eskirgan"
    return qmtest_user.testlar[data.month_date][data.test_key]["javoblar"][30*f_id:30*(f_id+1)]

# Testni kalitlarini edit token bilan taxrirlash
@iqromind_router.post("/set_test_edit_token")
async def set_test_edit_token(data: SetTestEditTokenSerializer, session: AsyncSession = Depends(get_async_session)):
    try:
        edit_token = data.edit_token[:4]+data.edit_token[:-4]
        f_id = int(data.edit_token[4:-4])
    except:
        return "Bu link eskirgan"
    
    res = await session.execute(select(iqromindtest).filter_by(user_id=data.user_id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        return "Bu link eskirgan"
    if edit_token != qmtest_user.edit_token:
        return "Bu link eskirgan"
    if len(data.kalitlar) != 30:
        return "Testni javoblarini to'liq kiriting 🙂"
    qmtest_user.testlar[data.month_date][data.test_key]["javoblar"][30*f_id:30*(f_id+1)] = data.kalitlar
    await session.execute(update(iqromindtest).where(iqromindtest.c.id == qmtest_user.id).values(
        testlar = qmtest_user.testlar
    ))
    await session.commit()
    return "Testni javoblarini eslab qoldim 😊"

# User set edu name
@iqromind_router.post("/set_edu_name")
async def set_edu_name(data: SetEduNameSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    res = await session.execute(select(iqromindtest).filter_by(user_id=user.id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        raise HTTPException(status_code=401, detail="User mavjud emas!")
    await session.execute(update(iqromindtest).where(iqromindtest.c.id == qmtest_user.id).values(
        edu_name = data.edu_name
    ))
    await session.commit()
    return "Edu name muvaffaqiyatli kiritildi"

# User set edu bot token
@iqromind_router.post("/set_edu_bot_token")
async def set_edu_bot_token(data: SetEduBotTokenSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    res = await session.execute(select(iqromindtest).filter_by(user_id=user.id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        raise HTTPException(status_code=401, detail="User mavjud emas!")
    await session.execute(update(iqromindtest).where(iqromindtest.c.id == qmtest_user.id).values(
        edu_bot_token = data.edu_bot_token
    ))
    await session.commit()
    # Telegram bot nomini token orqali aniqlash
    try:
        bot = telebot.TeleBot(data.edu_bot_token)
        bot_name = bot.get_me().first_name
        return f"Botingiz nomi {bot_name} ekan\nEslab qoldim 😊"
    except:
        return "Bot mavjud emas ekan 😕"


# User get edu bot token
@iqromind_router.post("/get_edu_bot_token")
async def get_edu_bot_token(data: GetEduBotTokenSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    res = await session.execute(select(iqromindtest).filter_by(user_id=user.id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        raise HTTPException(status_code=401, detail="User mavjud emas!")
    return qmtest_user.edu_bot_token

# User set edu logo
@iqromind_router.post("/set_edu_logo")
async def set_edu_logo(data: SetEduLogoSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    res = await session.execute(select(iqromindtest).filter_by(user_id=user.id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        raise HTTPException(status_code=401, detail="User mavjud emas!")
    await session.execute(update(iqromindtest).where(iqromindtest.c.id == qmtest_user.id).values(
        edu_logo = data.edu_logo
    ))
    await session.commit()
    return "Edu logo muvaffaqiyatli kiritildi"

