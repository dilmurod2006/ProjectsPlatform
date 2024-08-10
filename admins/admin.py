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
    UpdateAdmin
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
        raise HTTPException(status_code=403, detail="siz admin qo'sha olmaysiz!")
    
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


# GET DATAES FUNCTIONS FROM DATABASES START

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