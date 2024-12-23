from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from settings import IQROMINDTEST_ID
from telebot import TeleBot
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
    GetEduNameSerializer,
    SetEduBotTokenSerializer,
    SetEduLogoSerializer,
    GetEduBotTokenSerializer,
    AddNatijaSerializer,
    GetNatijaSerializer,
    GetAllNatijalarSerializer
)
from io import BytesIO

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
        now = datetime.now()
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
    now = datetime.now()

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
    # Eng yuqori bal eng past bal va o'rtacha balni hisoblash
    num=0
    umumiy_ball = 0
    max = 1890
    min = 0
    for i in qmtest_user.testlar[data.month_date][data.test_key]["tekshirishlar"].keys():
        test_data = qmtest_user.testlar[data.month_date][data.test_key]["tekshirishlar"][i]
        n = test_data.split("|")[0]
        bal = int(n.split(".")[0])*11
        bal += int(n.split(".")[1])*21
        bal += int(n.split(".")[2])*31
        if max<bal:
            max = bal
        if min>bal:
            min = bal
        umumiy_ball += bal
        num+=1
    


    # Test user mavjud bo'sa
    return {
        "name": qmtest_user.testlar[data.month_date][data.test_key]["name"],
        "bio": qmtest_user.testlar[data.month_date][data.test_key]["bio"],
        "date": qmtest_user.testlar[data.month_date][data.test_key]["date"],
        "edit_token": qmtest_user.edit_token,
        "max": max/10,
        "mid": umumiy_ball/(num*10),
        "min": min/10
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
    now = datetime.now()
    month_date = now.strftime("%Y%m")
    if month_date not in qmtest_user.testlar:
        qmtest_user.testlar[month_date] = dict()
    
    # yangi uchun key yaratiib olish
    test_key = now.strftime("%d%H%M")
    if test_key in qmtest_user.testlar[month_date]:
        return {"how": False,"message":"Hoy-hoy shoshmang...\nTestni saqlab olishim uchun 1 min vaqt bering 🙂"}
    if qmtest_user.end_premium_date < now:
        n = 0
        for i in qmtest_user.testlar.keys():
            n += len(qmtest_user.testlar[i])
        if n >= 5:
            return {"how": False,"message":"Afsus 😔 sizda faqat 5 ta test boshqarish imkoni bor \nyoki, Premiumga obuna olib xohlaganingizcha testlarni saqlab boring mumkin 🙂"}
    
    # yangi test yaratib olish
    new_test = create_test(data.test_name, now)
    
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
        if len(data.javoblar) != 420:
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
        edu_name = data.edu_name,
        edu_slogan = data.edu_slogan
    ))
    await session.commit()
    return "Edu name muvaffaqiyatli kiritildi"

# User get edu name
@iqromind_router.post("/get_edu_name/{user_id}")
async def get_edu_name(user_id: int, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(iqromindtest).filter_by(user_id=user_id))
    qmtest_user = res.fetchone()
    if qmtest_user is None:
        return {"name": "Iqro Mind Test", "slogan": "powered by Projects Platform"}
    if qmtest_user.end_premium_date < datetime.now():
        return {"name": "Iqro Mind Test", "slogan": "powered by Projects Platform"}
    if qmtest_user.edu_name == None or qmtest_user.edu_slogan == None:
        return {"name": "Iqro Mind Test", "slogan": "powered by Projects Platform"}
    return {"name": qmtest_user.edu_name, "slogan": qmtest_user.edu_slogan}


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
        bot = TeleBot(data.edu_bot_token)
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


# User get edu logo
@iqromind_router.get("/get_edu_logo/{user_id}")
async def get_edu_logo(user_id: int, session: AsyncSession = Depends(get_async_session)):
    # User ID bo'yicha qidirish
    res = await session.execute(select(iqromindtest).filter_by(user_id=user_id))
    qmtest_user = res.fetchone()

    # Default fayl yo'li
    default_logo_path = "iqromindtest/logo.svg"

    # Agar foydalanuvchi topilmasa, default logoni yuborish
    if qmtest_user is None:
        return FileResponse(default_logo_path, media_type="image/svg+xml")
    now = datetime.now()
    # Agar user premium bo'lmasa edu logoni o'rnga IqroMind logoni qaytarish
    if qmtest_user.end_premium_date < now:
        return FileResponse(default_logo_path, media_type="image/svg+xml")
    try:
        # Botdan fayl yuklab olish
        bot = TeleBot(qmtest_user.edu_bot_token)
        file_id = qmtest_user.edu_logo
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        file = bot.download_file(file_path)

        
        return StreamingResponse(BytesIO(file), media_type="image/png")

    except Exception as e:
        # Xatolik yuz berganda default logoni yuborish
        print(f"Xatolik: {e}")
        return FileResponse(default_logo_path, media_type="image/svg+xml")

# Natija qo'shish
@iqromind_router.post("/add_natija")
async def add_natija(data: AddNatijaSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(users).where(users.c.token == data.token))
    user = res.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User mavjud emas!")
    res = await session.execute(select(iqromindtest).filter_by(user_id=user.id))
    qmtest_user = res.fetchone()
    # Mavjud yoki yo'qligini tekshirsh
    if qmtest_user is None:
        raise HTTPException(status_code=401, detail="User mavjud emas!")
    # Mavjud bo'lsa
    qmtest_user.testlar[data.month_date][data.test_key]["tekshirishlar"][data.id_raqam] = f"{data.maj}.{data.b1}.{data.b2}|{data.file_id}"
    await session.execute(update(iqromindtest).where(iqromindtest.c.id == qmtest_user.id).values(
        testlar = qmtest_user.testlar
    ))
    await session.commit()
    return "Natija muvaffaqiyatli kiritildi"

# Natijani id_raqam bo'yicha olish
@iqromind_router.post("/get_natija")
async def get_natija(data: GetNatijaSerializer, session: AsyncSession = Depends(get_async_session)):

    res = await session.execute(select(iqromindtest).filter_by(user_id=data.user_id))
    qmtest_user = res.fetchone()
    # Mavjud yoki yo'qligini tekshirsh
    if qmtest_user is None:
        raise HTTPException(status_code=401, detail="User mavjud emas!")
    # Mavjud bo'lsa
    try:
        natija = qmtest_user.testlar[data.month_date][data.test_key]["tekshirishlar"][str(data.id_raqam)]
        return {
            "maj": natija.split("|")[0].split(".")[0],
            "b1": natija.split("|")[0].split(".")[1],
            "b2": natija.split("|")[0].split(".")[2],
            "file_url": f"https://api.projectsplatform.uz/iqromindtest/get_natija_file/{user.id}/{natija.split('|')[1]}"
        }
    except:
        raise HTTPException(status_code=408, detail="Natijalar topilmadi")
# Barcha natijalarni ulashish
@iqromind_router.post("/get_all_natijalar")
async def get_all_natijalar(data: GetAllNatijalarSerializer, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(iqromindtest).filter_by(user_id=data.user_id))
    qmtest_user = res.fetchone()
    # Mavjud yoki yo'qligini tekshirsh
    if qmtest_user is None:
        raise HTTPException(status_code=401, detail="User mavjud emas!")
    # Mavjud bo'lsa
    result = qmtest_user.testlar[data.month_date][data.test_key]["tekshirishlar"]
    return sort_dict(result)


# Natijani id_raqam bo'yicha olish
@iqromind_router.get("/get_natija_file/{user_id}/{file_id}")
async def get_natija_file(user_id: int, file_id: str, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(iqromindtest).filter_by(user_id=user_id))
    qmtest_user = res.fetchone()
    # Mavjud yoki yo'qligini tekshirsh
    default_logo_path = "iqromindtest/not-found.png"
    if qmtest_user is None:
        return FileResponse(default_logo_path, media_type="image/png")
    # Mavjud bo'lsa
    try:
        bot = TeleBot(qmtest_user.edu_bot_token)
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        file = bot.download_file(file_path)
        return StreamingResponse(BytesIO(file), media_type="image/png")
    except:
        return FileResponse(default_logo_path, media_type="image/png")

