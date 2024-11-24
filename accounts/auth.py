import os
import random
from datetime import datetime, timedelta

from .schemes import (
    CreateUser,
    LoginUser,
    CheckLogin,
    ChangePassword,
    ResetPassword,
    ResetPasswordRequest,
    AboutAccount,
    ActivationAccount,
    GetUserReports
)
from database import get_async_session
from models.models import users, reportsbalance, payment_admin
from settings import (
    API_ACTIVATION_ACCOUNT_SECRET_KEY,
    CHEACK_USER_FOR_BOT,
    CREATE_USER_SECRET_KEY
    )

from sqlalchemy import select, insert, update, delete, desc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, HTTPException
from passlib.context import CryptContext

from .utils import (
    hash_password,
    verify_password,
    generate_token_for_activation_account,
    generate_token_for_users,
    send_login_code,
    verify_jwt_token,
    send_reset_password_code,
    validate_username,
    validate_email
)

accounts_routers = APIRouter()
# Create User
@accounts_routers.post("/create_user")
async def create_user(data: CreateUser, session: AsyncSession = Depends(get_async_session)):
    try:
        # cheack secret key
        if data.secret_key != CREATE_USER_SECRET_KEY:
            raise HTTPException(status_code=400, detail="Secret key xato! Buzishga urunma!")

        # username validation
        validate_username(data.username)

        # email validation
        validate_email(data.email)

        # cheack email and username
        user = await session.execute(select(users).where(users.c.username == data.username))
        if user.scalars().first():
            raise HTTPException(status_code=400, detail="Foydalanuvchi nomi mavjud!")
        user = await session.execute(select(users).where(users.c.email == data.email))
        if user.scalars().first():
            raise HTTPException(status_code=400, detail="Email mavjud!")

        # password hashing
        password = hash_password(data.password)

        # genarate token for activation
        activation_token = generate_token_for_activation_account(data.username)

        # generate token for users
        jwt_data = {
            "username": data.username,
            "password": data.password
        }
        token = generate_token_for_users(jwt_data)

        # create user
        query = insert(users).values(
            full_name=data.full_name,
            email=data.email,
            username=data.username,
            password=password,
            activation_token=activation_token,
            token=token,
            ref_id=data.ref,
        )
        await session.execute(query)
        await session.commit()

        return {
            "message": "Account muvaffaqiyatli qo'shildi!\nTelegram orqali activation qiling.",
            "activation_link": f"https://t.me/projectsplatformbot?start={activation_token}",
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Activation account
@accounts_routers.post("/activation_account")
async def activation_account(data: ActivationAccount, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(users).filter_by(activation_token=data.token)
        result = await session.execute(query)
        data_acctivation = result.fetchone()
         
        # Tokenni tekshirish
        if data_acctivation is None:
            raise HTTPException(status_code=400, detail="Activation token xato! Buzishga urunma!")
        # cheack secret key
        if data.secret_key != API_ACTIVATION_ACCOUNT_SECRET_KEY:
            raise HTTPException(status_code=400, detail="Secret key xato! Buzishga urunma!")

        # update user
        query = update(users).where(users.c.activation_token == data.token).values(
            tg_id=data.tg_id,
            phone=data.phone,
            activation_token=None,
            is_active=True
        )
        await session.execute(query)
        await session.commit()

        return {"message": "Account muvaffaqiyatli activation qilindi!"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Login
@accounts_routers.post("/login")
async def login(data: LoginUser, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(users).where(users.c.username == data.username)
        result = await session.execute(query)
        user = result.fetchone()

        
        if user is None or not verify_password(data.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid username or password")
        
        # cheack is_active
        if user.is_active == False:
            return {
                "is_active": False,
                "url": f"https://t.me/projectsplatformbot?start={user.activation_token}"
            }
        
        # Tokenni tekshirish
        try:
            payload = verify_jwt_token(user.token)
        except HTTPException as e:
            if e.detail == "Token has expired":
                # Token eskirgan bo'lsa, yangi token yaratish
                jwt_token_data = {
                    "username": data.username,
                    "password": user.password
                }
                new_token = generate_token_for_users(jwt_token_data)

                # Tokenni yangilash
                query = update(users).where(users.c.username == data.username).values(token=new_token)
                await session.execute(query)
                await session.commit()
            else:
                raise e

        # Tasdiqlash kodi yaratish
        code = random.randint(100000, 999999)  # 6 xonali kod
        query = update(users).where(users.c.username == data.username).values(code=code)
        await session.execute(query)
        await session.commit()

        send_code = send_login_code(user.tg_id, code)

        return {
            "is_active": True,
            "message": send_code
            }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# cheack code for login
@accounts_routers.post("/check-login-code")
async def check_code(data: CheckLogin, session: AsyncSession = Depends(get_async_session)):
    query = select(users).where(users.c.username == data.username)
    result = await session.execute(query)
    user = result.fetchone()

    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    if user.code != data.code:
        raise HTTPException(status_code=400, detail="Invalid code")

    query = update(users).where(users.c.username == data.username).values(code=None)
    await session.execute(query)
    await session.commit()

    # return users.token    
    return {"message": "Code is valid and user logged in", "token": user.token}


# reset password request
@accounts_routers.post("/change-password-request")
async def reset_password_request(token: str, data: ChangePassword, session: AsyncSession = Depends(get_async_session)):
    payload = verify_jwt_token(token)
    
    # Token orqali foydalanuvchi ma'lumotlarini olish
    query = select(users).where(users.c.username == payload["username"])
    result = await session.execute(query)
    user = result.fetchone()

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid token")

    if not verify_password(data.last_password, user.password):
        raise HTTPException(status_code=400, detail="eski parolingiz xato")

    hashed_password = hash_password(data.new_password)

    query = update(users).where(users.c.username == payload["username"]).values(password=hashed_password)
    await session.execute(query)
    await session.commit()

    return {"message": "Password changed successfully"}

# reset password request
@accounts_routers.post("/reset-password-request")
async def reset_password_request(data: ResetPasswordRequest, session: AsyncSession = Depends(get_async_session)):
    query = select(users).where(users.c.username == data.username)
    result = await session.execute(query)
    user = result.fetchone()

    if user is None:
        raise HTTPException(status_code=400, detail="User not found")

    code = random.randint(100000, 999999)  # 6 xonali kod
    query = update(users).where(users.c.username == data.username).values(reset_code=code)
    await session.execute(query)
    await session.commit()

    send_code = send_reset_password_code(user.tg_id, code)

    return {"message": "parolni qayta tiklash kodi yuborildi"}


# reset password
@accounts_routers.post("/reset-password")
async def reset_password(data: ResetPassword, session: AsyncSession = Depends(get_async_session)):
    query = select(users).where(users.c.username == data.username)
    result = await session.execute(query)
    user = result.fetchone()

    if user is None:
        raise HTTPException(status_code=400, detail="User not found")

    if user.reset_code != data.reset_code:
        raise HTTPException(status_code=400, detail="Invalid reset code")

    hashed_password = hash_password(data.password)

    query = update(users).where(users.c.username == data.username).values(password=hashed_password, reset_code=None)
    await session.execute(query)
    await session.commit()

    return {"message": "Parol muvaffaqiyatli o'zgartirildi"}


# GET AboutAccount
@accounts_routers.post("/about_account")
async def get_about_account(data: AboutAccount, session: AsyncSession = Depends(get_async_session)):
    query = select(users).where(users.c.token == data.token)
    result = await session.execute(query)
    user = result.fetchone()


    # cheack token
    if user is None or not verify_jwt_token(data.token):
        raise HTTPException(status_code=401, detail="user not found or token expired")
    
    # Ma'lumotlarni JSON formatiga aylantirish
    # serialized_data = [serialize_user(row) for row in user]

    return {
        "id": user.id,
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "sex": user.sex,
        "tg_id": user.tg_id,
        "balance": user.balance,
    }

# cheack user for bot
@accounts_routers.get("/check_user")
async def check_user(KeySecret: str, tg_id: int, session: AsyncSession = Depends(get_async_session)):
    # KeySecret ni tekshirish
    if KeySecret != CHEACK_USER_FOR_BOT:
        raise HTTPException(status_code=400, detail="Invalid KeySecret")

    # Foydalanuvchini topish uchun query
    query = select(users).where(users.c.tg_id == tg_id)
    result = await session.execute(query)
    user = result.fetchone()

    # Agar foydalanuvchi topilmasa
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    # result.fetchone() natijasi tuple bo'lishi mumkin
    user_data = user._mapping  # Bu usul natijani dict formatiga o'giradi

    return {
        "full_name": user_data['full_name'],
        "balance": user_data['balance'],
        "username": user_data['username']
    }



# Get Reports
@accounts_routers.post("/get_reports")
async def get_reports(data: GetUserReports, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(users).where(users.c.token == data.token)
        result = await session.execute(query)
        user = result.fetchone()

        
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        
        # cheack is_active
        if user.is_active == False:
            return {
                "is_active": False,
                "url": f"https://t.me/projectsplatformbot?start={user.activation_token}"
            }
        
        
        # 1-jadvaldan `created_at` bo'yicha ma'lumotlarni olish
        res1 = await session.execute(select(payment_admin).filter_by(user_id=user.id).order_by(desc(payment_admin.c.created_at)))
        table1_items = res1.fetchall()

        # 2-jadvaldan `created_at` bo'yicha ma'lumotlarni olish
        res2 = await session.execute(select(reportsbalance).filter_by(user_id=user.id).order_by(desc(reportsbalance.c.created_at)))
        table2_items = res2.fetchall()

        # Ikkala jadvaldan olingan yozuvlarni birlashtirish
        combined_items = table1_items + table2_items

        # `created_at` bo'yicha saralash
        combined_items_sorted = sorted(combined_items, key=lambda x: x.created_at, reverse=True)

        # JSON formatida qaytarish
        return [{"tulov_summasi": item.tulov_summasi, "bio": item.bio, "created_at": item.created_at} for item in combined_items_sorted]    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
