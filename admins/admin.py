# admin oanel apies
import os
import json
import random
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
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
    products,
    ProjectsData
)
from .schemes import (
    LoginAdmin,
    CheckLoginAdmin,
    ResetPasswordRequest,
    ResetPassword,
    CreateAdmin,
    DeleteAdmin,
    UpdateAdmin,
    AddProducts,
    UpdateProducts,
    DeleteProducts,
    AddPayment,
    CreateProjectsData,
    UpdateProjectsData,
)
from .utils import (
    send_login_code,
    send_reset_password_code,
    generate_token_for_admin,
    verify_jwt_token,
    has_permission,
    is_valid_phone_number,
    check_payment,
    serialize_forregister,
    serialize_users,
    serialize_reports_balance,
    serialize_products,
    serialize_school_data,
    serialize_pckundalikcom,
    serialize_mobilekundalikcom,
    serialize_majburiyobuna,
    serialize_admins,
    serialize_get_all_telegram_ids,
    serialize_get_all_phone_numbers,
    serialize_get_projectsdata
)
from datetime import datetime, timedelta

admin_router = APIRouter()

# login admin
@admin_router.post("/login")
async def login_admin(data: LoginAdmin, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.username == data.username)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None:
        raise HTTPException(status_code=401, detail="admin not found")
    if admin.password != data.password:
        raise HTTPException(status_code=401, detail="password is wrong")
    
    # Tokenni tekshirish
    try:
        payload = verify_jwt_token(admin.token)
    except HTTPException as e:
        if e.detail == "Token has expired":
            # Token eskirgan bo'lsa, yangi token yaratish
            jwt_token_data = {
                "username": data.username,
                "password": admin.password
            }
            new_token = generate_token_for_admin(jwt_token_data)

            # Tokenni yangilash
            query = update(admins).where(admin.c.username == data.username).values(token=new_token)
            await session.execute(query)
            await session.commit()
        else:
            raise e
    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'login_admin': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz admin login olmaysiz!")
    
     # Tasdiqlash kodi yaratish
    code = random.randint(100000, 999999)  # 6 xonali kod
    query = update(admins).where(admins.c.username == data.username).values(code=code)
    await session.execute(query)
    await session.commit()

    send_code = send_login_code(admin.tg_id, code)

    if not send_code:
        raise HTTPException(status_code=500, detail="code not sent")
    
    return {"message": "Tasdiqlash kodi yuborildi!"}
# cheack login admin
@admin_router.post("/check-login")
async def check_login_admin(data: CheckLoginAdmin, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.username == data.username)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None:
        raise HTTPException(status_code=401, detail="admin not found")

    if not verify_jwt_token(admin.token):
        raise HTTPException(status_code=401, detail="token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'check_login_admin': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz admin login olmaysiz!")

    if admin.code != data.code:
        raise HTTPException(status_code=401, detail="code is wrong")

    query = update(admins).where(admins.c.username == data.username).values(code=None)
    await session.execute(query)
    await session.commit()

    return {"message": "Admin login success", "token": admin.token}


# reset password admin
@admin_router.post("/reset-password-request")
async def reset_password_request_admin(data: ResetPasswordRequest, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.username == data.username)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None:
        raise HTTPException(status_code=401, detail="admin not found")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'reset_password_request_admin': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz admin parol tiklash uchun so'rov yubora olmaysiz!")

    code = random.randint(100000, 999999)  # 6 xonali kod
    query = update(admins).where(admins.c.username == data.username).values(reset_code=code)
    await session.execute(query)
    await session.commit()

    send_code = send_reset_password_code(admin.tg_id, code)

    if not send_code:
        raise HTTPException(status_code=500, detail="code not sent")

    return {"message": "Tasdiqlash kodi yuborildi!"}


# reset password admin
@admin_router.post("/reset-password")
async def reset_password_admin(data: ResetPassword, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.username == data.username)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None:
        raise HTTPException(status_code=401, detail="admin not found")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'reset_password_admin': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz admin parolini o'zgartira olmaysiz!")

    # cheack reset code
    if admin.reset_code != data.reset_code:
        raise HTTPException(status_code=401, detail="code not found")   
    
    query = update(admins).where(admins.c.username == data.username).values(
        password=data.password,
        reset_code=None
    )
    await session.execute(query)
    await session.commit()

    return {"message": "Parol yangilandi!"}

# create admin
@admin_router.post("/add-admin")
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
    
    # cheack username in admin table
    if data.username==admin.username:
        raise HTTPException(status_code=401, detail="Bu username allaqachon bor!")
    
    # cheack email in admin table
    if data.email==admin.email:
        raise HTTPException(status_code=401, detail="Bu email allaqachon bor!")
    
    phone_number = is_valid_phone_number(data.phone)

    data_token = {
        "username": data.username,
        "password": data.password,
        "tg_id": data.tg_id
    }
    TOKEN = generate_token_for_admin(data_token)
    query = insert(admins).values(
        full_name = data.full_name,
        phone = phone_number,
        email = data.email,
        username = data.username,
        password = data.password,
        tg_id = data.tg_id,
        premessions = data.premessions,
        token = TOKEN
    )
    await session.execute(query)
    await session.commit()
    return {"message": "Admin created successfully"}

# update admin
@admin_router.put("/update-admin")
async def update_admin(token: str, data: UpdateAdmin, session: AsyncSession = Depends(get_async_session)):
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
    
    # cheack username in admin tabless
    if data.username==admin.username:
        raise HTTPException(status_code=401, detail="Bu username allaqachon bor!")
    
    # cheack email in admin table
    if data.email==admin.email:
        raise HTTPException(status_code=401, detail="Bu email allaqachon bor!")
    
    phone_number = is_valid_phone_number(data.phone)
    
    query = update(admins).where(admins.c.username == admin.username).values(
        full_name = data.full_name,
        phone = phone_number,
        email = data.email,
        username=data.username,
        password=data.password,
        tg_id=data.tg_id,
        premessions=data.premessions,
        active=data.active,
        updated_at=datetime.utcnow()
    )
    result = await session.execute(query)
    await session.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"message": "Admin updated successfully"}

# delete admin
@admin_router.delete("/delete-admin")
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

    # settings_dict = json.loads(data.settings)
    query = insert(products).values(
        name=data.name,
        bio=data.bio,
        settings=data.settings
    )
    await session.execute(query)
    await session.commit()
    return {"message": "Product added successfully"}

# update products
@admin_router.put("/update-products")
async def update_products(token: str, data: UpdateProducts, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")
    
    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'update_products': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz productlarni o'zgartira olmaysiz!")

    query = update(products).where(products.c.name == data.name).values(
        name=data.name,
        bio=data.bio,
        settings=data.settings
    )
    await session.execute(query)
    await session.commit()
    return {"message": "Product updated successfully"}

# delete products
@admin_router.delete("/delete-products")
async def delete_products(token: str, data: DeleteProducts, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'delete_products': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz productlarni o'chira olmaysiz!")
    
    query = delete(products).where(products.c.name == data.name)
    await session.execute(query)
    await session.commit()
    return {"message": "Product deleted successfully"}


# ADD PAYYMENT FUNCTIONS START
@admin_router.post("/add-payment")
async def add_payment(token: str, data: AddPayment, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'add_payment': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz payment qo'sha olmaysiz!")
    
    # cheack user token
    user_query = select(users).where(users.c.token == data.token)
    result = await session.execute(user_query)
    user = result.fetchone()

    reportsbalance_query = select(reportsbalance).where(reportsbalance.c.payment_number == data.payment_number)
    result = await session.execute(reportsbalance_query)
    reportsbalance_data = result.fetchone()

    if user is None:
        raise HTTPException(status_code=400, detail="User not found")

    # cheack payment 
    if check_payment() is False:
        raise HTTPException(status_code=400, detail="Bunaqa to'lov hali amalga oshmadi qaytadan urinib ko'ring!")

    # add balance in users table
    balance_query = update(users).where(users.c.token == data.token).values(
        balance = user.balance + data.tulov_summasi
    )

    query = insert(reportsbalance).values(
        payment_number = data.payment_number,
        user_id=user.id,
        balance= data.tulov_summasi,
        tulov_summasi=data.tulov_summasi,
        bio=data.bio
    )
    await session.execute(balance_query)
    await session.execute(query)

    await session.commit()
    return {"message": "Payment added successfully"}


# ADD PAYMENT FUNCTIONS END

# CREATE, UPDATE PROJECTSDATA FUNCTIONS START

# Create ProjectsData
@admin_router.post("/create-projectsdata")
async def create_projectsdata(token: str, data: CreateProjectsData, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'create_projectsdata': 'True'
        }
        }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz projectsdata qo'sha olmaysiz!")

    query = insert(ProjectsData).values(
        name = data.name,
        email = data.email,
        domen = data.domen,
        telegram_channel = data.telegram_channel,
        youtube_channel = data.youtube_channel,
        telegram_group = data.telegram_group,
        telegram_bot = data.telegram_bot,
        about = data.about
    )

    await session.execute(query)
    await session.commit()
    return {"message": "ProjectsData created successfully"}

# Update ProjectsData
@admin_router.put("/update-projectsdata")
async def update_projectsdata(token: str, data: UpdateProjectsData, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'update_projectsdata': 'True'
        }
        }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz projectsdata o'zgartira olmaysiz!")

    query = update(ProjectsData).where(ProjectsData.c.id == data.id).values(
        name = data.name,
        email = data.email,
        domen = data.domen,
        telegram_channel = data.telegram_channel,
        youtube_channel = data.youtube_channel,
        telegram_group = data.telegram_group,
        telegram_bot = data.telegram_bot,
        about = data.about
    )

    await session.execute(query)
    await session.commit()
    return {"message": "ProjectsData updated successfully"}


# CREATE, UPDATE PROJECTSDATA FUNCTIONS END

# GET DATA FUNCTIONS FROM DATABASES START

# get forregister data
@admin_router.get("/get-forregister")
async def get_forregister(token: str, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'get_forregister_data': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz forregister datalarni ololmaysiz!")

    # Forregisterlarni olish
    query = select(forregister)
    result = await session.execute(query)
    data = result.fetchall()
    
    # Ma'lumotlarni JSON formatiga aylantirish
    serialized_data = [serialize_forregister(row) for row in data]

    return {"forregister": serialized_data}


# get users data
@admin_router.get("/get-users")
async def get_users(token: str, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'get_users_data': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz users datalarni ololmaysiz!")

    # Userslarni olish
    query = select(users)
    result = await session.execute(query)
    data = result.fetchall()

    # Ma'lumotlarni JSON formatiga aylantirish
    serialized_data = [serialize_users(row) for row in data]

    return {"users": serialized_data}

# get reportsbalance data
@admin_router.get("/get-reportsbalance")
async def get_reportsbalance(token: str, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'get_reportsbalance_data': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz reportsbalance datalarni ololmaysiz!")

    # Reportsbalance datalarni olish
    query = select(reportsbalance)
    result = await session.execute(query)
    data = result.fetchall()

    # Ma'lumotlarni JSON formatiga aylantirish
    serialized_data = [serialize_reports_balance(row) for row in data]

    return {"reportsbalance": serialized_data}

# get products data
@admin_router.get("/get-products")
async def get_products(token: str, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'get_products_data': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz product datalarni ololmaysiz!")

    # Mahsulotlarni olish
    query = select(products)
    result = await session.execute(query)
    data = result.fetchall()

    # Ma'lumotlarni JSON formatiga aylantirish
    serialized_data = [serialize_products(row) for row in data]
    
    return {"products": serialized_data}
# get school data
@admin_router.get("/get-schooldata")
async def get_schooldata(token: str, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'get_school_data': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz school datalarni ololmaysiz!")

    query = select(school_data)
    result = await session.execute(query)
    data = result.fetchall()

    # Ma'lumotlarni JSON formatiga aylantirish
    serialized_data = [serialize_school_data(row) for row in data]

    return {"school": serialized_data}

# get pckundalikcom data
@admin_router.get("/get-pckundalikcom")
async def get_pckundalikcom(token: str, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)   
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'get_pckundalikcom_data': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz pckundalikcom datalarni ololmaysiz!")

    query = select(pckundalikcom)
    result = await session.execute(query)
    data = result.fetchall()

    # Ma'lumotlarni JSON formatiga aylantirish
    serialized_data = [serialize_pckundalikcom(row) for row in data]

    return {"pckundalikcom": serialized_data}

# get mobilekundalikcom data
@admin_router.get("/get-mobilekundalikcom")
async def get_mobilekundalikcom(token: str, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'get_mobilekundalikcom_data': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz mobilekundalikcom datalarni ololmaysiz!")

    query = select(mobilekundalikcom)
    result = await session.execute(query)
    data = result.fetchall()

    # Ma'lumotlarni JSON formatiga aylantirish
    serialized_data = [serialize_mobilekundalikcom(row) for row in data]

    return {"mobilekundalikcom": serialized_data}

# get majburiyobuna data
@admin_router.get("/get-majburiyobuna")
async def get_majburiyobuna(token: str, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'get_majburiyobuna_data': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz majburiyobuna datalarni ololmaysiz!")

    query = select(majburiyobuna)
    result = await session.execute(query)
    data = result.fetchall()

    # Ma'lumotlarni JSON formatiga aylantirish
    serialized_data = [serialize_majburiyobuna(row) for row in data]

    return {"majburiyobuna": serialized_data}

# get admins data
@admin_router.get("/get-admins")
async def get_admins(token: str, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'get_admins_data': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz admins datalarni ololmaysiz!")

    query = select(admins)
    result = await session.execute(query)
    data = result.fetchall()

    # Ma'lumotlarni JSON formatiga aylantirish
    serialized_data = [serialize_admins(row) for row in data]

    return {"admins": serialized_data}


# get all Telegram IDs from users table
@admin_router.get("/get_all_telegram_ids")
async def get_all_telegram_ids(token: str, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'get_all_telegram_ids_data': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz all_telegram_ids datalarni ololmaysiz!")

    query = select(users.c.tg_id)
    result = await session.execute(query)
    data = result.fetchall()

    # Ma'lumotlarni JSON formatiga aylantirish
    serialized_data = [serialize_get_all_telegram_ids(row) for row in data]

    return {"all_telegram_ids": serialized_data}



# Get all phone numbers and full names from users table
@admin_router.get("/get_all_phone_numbers")
async def get_all_phone_numbers(token: str, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'get_all_phone_numbers_data': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz all_phone_numbers datalarni ololmaysiz!")

    query = select(users.c.phone, users.c.full_name)
    result = await session.execute(query)
    data = result.fetchall()

    # Ma'lumotlarni JSON formatiga aylantirish
    serialized_data = [serialize_get_all_phone_numbers(row) for row in data]

    return {"all_phone_numbers": serialized_data}

# get ProjectsData
@admin_router.get("/get-projectsdata")
async def get_projectsdata(token: str, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):    
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'get_projectsdata': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz projectsdata datalarni ololmaysiz!")

    query = select(ProjectsData)
    result = await session.execute(query)
    data = result.fetchall()

    # Ma'lumotlarni JSON formatiga aylantirish
    serialized_data = [serialize_get_projectsdata(row) for row in data]

    return {"projectsdata": serialized_data}

# GET DATA FUNCTIONS FROM DATABASES END