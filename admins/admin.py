# admin oanel apies

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    insert,
    select,
    update,
    delete,
)
from database import get_async_session
from models.models import (
    admins,
    forregister,
    users,
    majburiyobuna,
    loginsdata,
    reportsbalance,
    pckundalikcom,
    mobilekundalikcom,
    school_data,
    products
)
from .schemes import (
    CreateAdmin,
    DeleteAdmin,
    UpdateAdmin,
    AddProducts
)
from .utils import (
    generate_token_for_admin,
    verify_jwt_token,
    has_permission
)
from datetime import datetime, timedelta

admin_router = APIRouter()


# create admin
@admin_router.post("/create-admin")
async def create_admin(token:str,data: CreateAdmin, session: AsyncSession = Depends(get_async_session)):
    # cheack admin token in admin table
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")
    
    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'add_admin': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz admin qo'sha olmaysiz!")

    data_token = {
        "username": data.username,
        "password": data.password,
        "tg_id": data.tg_id
    }
    TOKEN = generate_token_for_admin(data_token)
    query = insert(admins).values(
        username=data.username,
        password=data.password,
        tg_id=data.tg_id,
        token=TOKEN,
        premessions=data.premessions
    )
    await session.execute(query)
    await session.commit()
    return {"message": "Admin created successfully"}

# update admin
@admin_router.put("/update")
async def update_admin(token: str, admin: UpdateAdmin, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")
    
    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'update_admin': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz admin ma'lumotlarini o'zgartira olmaysiz!")
    
    query = update(admins).where(admins.c.username == admin.username).values(
        username=admin.username,
        password=admin.password,
        tg_id=admin.tg_id,
        premessions=admin.premessions,  # JSONB formatidagi qiymat
        updated_at=datetime.utcnow()  # Yangilanish vaqtini qo'shish
    )
    result = await session.execute(query)
    await session.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"message": "Admin updated successfully"}

# delete admin
@admin_router.delete("/delete")
async def delete_admin(token: str, data: DeleteAdmin, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'delete_admin': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz admini o'chira olmaysiz!")

    query = delete(admins).where(admins.c.username == data.username)
    await session.execute(query)
    await session.commit()
    return {"message": "Admin deleted successfully"}


# Add products
@admin_router.post("/add-products")
async def add_products(token: str, data: AddProducts, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")
    
    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'add_products': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz product qo'sha olmaysiz!")

    query = insert(products).values(
        name=data.name,
        bio=data.bio,
        settings=data.settings
    )
    await session.execute(query)
    await session.commit()
    return {"message": "Product added successfully"}


# GET DATA FUNCTIONS FROM DATABASES START


# About users get data
@admin_router.post("/about-account")
async def about_account(token: str, session: AsyncSession = Depends(get_async_session)):
    """
    Foydalanuvchi haqida ma'lumot olish va token muddati tekshiruvi.

    Args:
        token (str): JWT token.

    Raises:
        HTTPException: Agar token noto'g'ri yoki muddati o'tgan bo'lsa.

    Returns:
        dict: Foydalanuvchi ma'lumotlarini o'z ichiga olgan lug'at.
    """
    # Tokenni tekshirish
    payload = verify_jwt_token(token)
    
    # Token orqali foydalanuvchi ma'lumotlarini olish
    query = select(users).where(users.c.username == payload["username"])
    result = await session.execute(query)
    user = result.fetchone()

    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Token muddati o'tmagan bo'lsa, foydalanuvchi ma'lumotlarini qaytarish
    return {
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "sex": user.sex,
        "tg_id": user.tg_id,
        "balance": user.balance
    }

# Get all Telegram IDs from users table
@admin_router.get("/get_all_telegram_ids")
async def get_all_telegram_ids(session: AsyncSession = Depends(get_async_session)):
    """Bu funksiya foydalanuvchilarimizni telegram IDlarini qaytaradi.
       Bu funksiyani qilishdan maqsad foydalanuvchilarga kerakli vaqtda xabar va reklama yuborish uchun olinadi!
       Va foydalanuvchilarni doimiy statiskasini ko'rish uchun yani botdan nechta foydalanuvchi borligi va ular botni blocklamagnini tekshirish uchun olinadi.
       
       
       Funksiydan foydalanish uchun:
        /get_all_telegram_ids GET so'rovini yuborish kifoya
        
        
        respone sifatida: dict qaytadi: {"tg_ids": list} shaklida beradi bemalol olish mumkun
    """
    query = select(users.c.tg_id)
    result = await session.execute(query)
    data = result.scalars().all()  # Use scalars().all() to get a list of values
    return {"tg_ids": data}

# Get all phone numbers and full names from users table
@admin_router.get("/get_all_phone_numbers")
async def get_all_phone_numbers(session: AsyncSession = Depends(get_async_session)):
    """Bu funksiya foydalanuvchilarimizni hamma telefon raqamlarini va ism-familiyani qaytaradi.
       Bu funksiyani qilishdan maqsad foydalanuvchilarga kerakli vaqtda sms yuborish uchun olinadi!
       Yani sms da foydalanuvchi ism familiyasi bilan murojat qilishi uchun qilindi.
    """
    query = select(users.c.phone, users.c.full_name)
    result = await session.execute(query)
    data = result.fetchall()
    
    phone_numbers = [row[0] for row in data]
    full_names = [row[1] for row in data]
    
    return {"phone_numbers": phone_numbers, "full_names": full_names}


# GET DATA FUNCTIONS FROM DATABASES END

# get all users
@admin_router.get("/get-all-users")
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    query = select(users)
    result = await session.execute(query)
    user = result.all()
    return user

# get all admins
@admin_router.get("/get-all-admins")
async def get_all_admins(session: AsyncSession = Depends(get_async_session)):
    query = select(admins)
    result = await session.execute(query)
    data = result.all()
    return data

# get all forregister
@admin_router.get("/get-all-forregister")
async def get_all_forregister(session: AsyncSession = Depends(get_async_session)):
    query = select(forregister)
    result = await session.execute(query)
    data = result.all()
    return data

# get all majburiyobuna
@admin_router.get("/get-all-majburiyobuna")
async def get_all_majburiyobuna(session: AsyncSession = Depends(get_async_session)):
    query = select(majburiyobuna)
    result = await session.execute(query)
    data = result.all()
    return data

# get all products
@admin_router.get("/get-all-products")
async def get_all_products(session: AsyncSession = Depends(get_async_session)):
    query = select(products)
    result = await session.execute(query)
    data = result.all()
    return data