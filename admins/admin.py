# admin oanel apies
import os
import json
import random
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    insert,
    select,
    update,
    delete
)


from database import get_async_session
from models.models import (
    admins,
    users,
    majburiyobuna,
    loginsdata,
    reportsbalance,
    pckundalikcom,
    mobilekundalikcom,
    school_data,
    products,
    payment_admin
)

from sqlalchemy.sql import or_


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
    GetData,
    GetDataUser,
    FindData,
    DeleteUserData,
    KirishBallari
)

from .utils import (
    send_login_code,
    send_reset_password_code,
    generate_token_for_admin,
    verify_jwt_token,
    has_permission,
    is_valid_phone_number,
    send_payment_data,
    serialize_users,
    serialize_reports_balance,
    serialize_payment,
    serialize_products,
    serialize_school_data,
    serialize_pckundalikcom,
    serialize_mobilekundalikcom,
    serialize_majburiyobuna,
    serialize_admins,
    serialize_get_all_telegram_ids,
    serialize_get_all_phone_numbers
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
async def create_admin(token: str, data: CreateAdmin, session: AsyncSession = Depends(get_async_session)):
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
    
    if not is_valid_phone_number(data.phone):
        raise HTTPException(status_code=401, detail="Telefon raqam noto'g'ri kiritildi!")

    data_token = {
        "username": data.username,
        "password": data.password,
        "tg_id": data.tg_id
    }
    TOKEN = generate_token_for_admin(data_token)
    query = insert(admins).values(
        full_name = data.full_name,
        phone = data.phone,
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

    query = update(products).where(products.c.id == data.id).values(
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
@admin_router.post("/payment")
async def add_payment(
    admin_token: str = Form(...),
    tg_id: int = Form(...),
    tulov_summasi: int = Form(...),
    bio: str = Form(None),
    payment_chek_img: UploadFile = File(...),  # Tasvirni fayl shaklida qabul qilish
    session: AsyncSession = Depends(get_async_session)
):
    # Adminni tekshirish
    query = select(admins).where(admins.c.token == admin_token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(admin_token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # Adminning huquqlarini tekshirish
    required_permissions = {
        "permessions": {
            'admin': {
                'add_payment': 'True'
            }
        }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz payment qo'sha olmaysiz!")
    
    # Foydalanuvchini tekshirish
    user_query = select(users).where(users.c.tg_id == tg_id)
    user_result = await session.execute(user_query)
    user = user_result.fetchone()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Tasvir ma'lumotlarini o'qish
    image_data = await payment_chek_img.read()  # Faylni `bytes` ga o'qish

    # Payment qo'shish
    payment_query = insert(payment_admin).values(
        admin_id=admin.id,
        user_id=user.id,
        tulov_summasi=tulov_summasi,
        payment_chek_img=image_data,  # Tasvir ma'lumotlarini bazaga yozish
        bio=bio,
        created_at=datetime.utcnow()
    )

    # Foydalanuvchi balansini yangilash
    update_balance_query = update(users).where(users.c.id == user.id).values(balance=user.balance + tulov_summasi)
    await session.execute(update_balance_query)
    await session.execute(payment_query)

    send_about_payment_data = send_payment_data(
        tg_id=tg_id,
        username=user.username,
        tulov_summasi=tulov_summasi,
        payment_chek_img=image_data,
        bio=bio
    )

    await session.commit()
    return {"message": f"{user.username} foydalanuvchiga {tulov_summasi} so'm to'lov o'tkazildi. {send_about_payment_data}"}

# ADD PAYMENT FUNCTIONS END


# GET DATA FUNCTIONS FROM DATABASES START


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

# get user data
@admin_router.post("/get-user")
async def get_user(data:GetDataUser, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == data.admin_token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(data.admin_token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'get_user_data': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz user datalarni ololmaysiz!")

    # Userslarni olish
    query = select(users).where(users.c.id == data.user_id)
    result = await session.execute(query)
    data = result.fetchone()

    return {
        "id": data.id,
        "full_name": data.full_name,
        "username": data.username,
        "email": data.email,
        "phone": data.phone,
        "sex": data.sex,
        "tg_id": data.tg_id,
        "balance": data.balance,
        "created_at": data.created_at,
        "updated_at": data.updated_at,
        "last_login": data.last_login,
        "how_online": data.how_online,
    }





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

# get payment data
@admin_router.get("/get-payment-data")
async def get_payment(token: str, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    required_permissions = {
        "permessions": {
        'admin': {
            'get_payment_data': 'True'
        }
    }
    }

    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="siz payment datalarni ololmaysiz!")

    # Payment datalarni olish
    query = select(payment_admin)
    result = await session.execute(query)
    data = result.fetchall()

    # Ma'lumotlarni JSON formatiga aylantirish
    serialized_data = [serialize_payment(row) for row in data]

    return {"payment": serialized_data}

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


# GET DATA FUNCTIONS FROM DATABASES END

@admin_router.get("/about_admin")
async def about_admin(token: str, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")
    return {
        "full_name": admin.full_name,
        "phone": admin.phone,
        "tg_id": admin.tg_id,
        "username": admin.username,
        "premessions": admin.premessions
    }



@admin_router.post("/find_user")
async def find_user(data: FindData, session: AsyncSession = Depends(get_async_session)):
    # Check if admin exists and token is valid
    query = select(admins).where(admins.c.token == data.admin_token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(data.admin_token):
        raise HTTPException(status_code=401, detail="Admin not found or token expired")
    
    # Check permissions
    required_permissions = {
        "permessions": {
            'admin': {
                'find_user_data': 'True'
            }
        }
    }
    if not has_permission(admin.premessions, required_permissions):
        raise HTTPException(status_code=403, detail="Siz find_user datalarni ololmaysiz!")

    # Query users
    search_query = f"%{data.text}%"
    users_query = (
        select(users)
        .where(
            or_(
                users.c.full_name.like(search_query),
                users.c.username.like(search_query)
            )
        )
        .offset(0)
        .limit(10)
    )
    results = await session.execute(users_query)
    users_list = results.fetchall()


    return {"users": [{"id": user.id, "username": user.username, "full_name": user.full_name, "tg_id": user.tg_id, "email": user.email, "phone": user.phone, "balance": user.balance} for user in users_list]}
    # Datalarni qaytarish
# set kirish ballari
@admin_router.post("/set_kirish_ballari")
async def set_kirish_ballari(token: str, data: KirishBallari, session: AsyncSession = Depends(get_async_session)):
    query = select(admins).where(admins.c.token == token)
    result = await session.execute(query)
    admin = result.fetchone()

    if admin is None or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="admin not found or token expired")

    # cheack premessions in admin table
    # required_permissions = {
    #     "permessions": {
    #     'admin': {
    #         'set_kirish_ballari': 'True'
    #     }
    # }
    # }

    # if not has_permission(admin.premessions, required_permissions):
    #     raise HTTPException(status_code=403, detail="siz kirish ballarini o'zgartirish mumkin emas!")
    # Mavjudligini tekshirish
    query = select(kirish_ballari).where(kirish_ballari.c.viloyat == data.viloyat, kirish_ballari.c.otm == data.otm)
    result = await session.execute(query)
    kirish_ballari = result.fetchone()

    if kirish_ballari is None:
        await session.execute(
            insert(kirish_ballari).values(
                viloyat = data.viloyat,
                otm = data.otm,
                yil = data.yil,
                data = data.data
            )
        )
        await session.commit()
        return True
    # Mavjud bo'lsa yangilash
    await session.execute(
        update(kirish_ballari).where(kirish_ballari.c.viloyat == data.viloyat, kirish_ballari.c.otm == data.otm).values(
            yil = data.yil,
            data = data.data
        )
    )
    return True