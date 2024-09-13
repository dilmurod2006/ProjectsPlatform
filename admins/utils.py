from datetime import datetime,timedelta
import random

import string

import hashlib

from fastapi import HTTPException
import jwt

from typing import Dict

import os

import binascii

from requests import post, get

import secrets

from settings import BOT_TOKEN, SECRET_KEY_FOR_ADMINS, ALGORITHM
import re


# send login code to admin via bot
def send_login_code(tg_id: int, code: int) -> str:
    """Foydalanuvchi login kodi yuborish."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": tg_id,
        "text": f"Sizning tasdiqlash kodingiz: {code}",
    }
    post(url, data)

    return f"code yuborildi!"


# reset password send code
def send_reset_password_code(tg_id: int, reset_code: int) -> str:
    """Foydalanuvchi login kodi yuborish."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": tg_id,
        "text": f"Your reset password code is: {reset_code}",
    }
    post(url, data)

    return f"parolni tiklovchi code yuborildi!"

# generate jwt token for admin
def generate_token_for_admin(data: Dict[str, str], expires_delta: timedelta = timedelta(days=731)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY_FOR_ADMINS, algorithm=ALGORITHM)

def verify_jwt_token(token: str) ->dict:
    try:
        # Tokenni dekodlash
        payload = jwt.decode(token, SECRET_KEY_FOR_ADMINS, algorithms=ALGORITHM)
        
        # Token muddati o'tganligini tekshirish
        exp = payload.get("exp")
        if exp is None:
            raise HTTPException(status_code=400, detail="Token does not contain expiration time")
        
        expiration_date = datetime.utcfromtimestamp(exp)
        if expiration_date < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Token has expired")
        
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")
    

# cheack premessinos in admin table
def has_permission(premessions: Dict, required_permissions: Dict) -> bool:
    """
    Check if the admin has the required permissions.
    """
    admin_perms = premessions.get('permessions', {})
    required_perms = required_permissions.get('permessions', {})

    # Check if all required permissions are present
    for category, required in required_perms.get('admin', {}).items():
        if admin_perms.get('admin', {}).get(category) != required:
            return False
    return True

# O'zbekiston raqamini tekshirish
def is_valid_phone_number(phone: str) -> bool:
    """Telefon raqamining O'zbekiston raqamiga mosligini tekshiradi.
       Masalan: O'zbekiston code:+998 dan boshlanadi
       agar boshqa davlatning raqami berilsa qabul qilmaydi.
    """
    return bool(re.match(r'^\+998[1-9][0-9]{8}$', phone))



# cheack user payment function start

# bank web sites control function
def bank_web_site_control():
    pass

# cheack payment
def check_payment():
    return True

# send about payment data
def send_payment_data(tg_id: int, username: str, tulov_summasi: int, payment_chek_img: bytes, bio: str) -> str:
    """Foydalanuvchiga to'lov o'tkazilganligi haqida ma'lumot yuborish"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        
        # Faylni yuborish uchun files parametrlardan foydalanamiz
        files = {
            "photo": payment_chek_img
        }
        
        data = {
            "chat_id": tg_id,
            "caption": (
                f"To'lov o'tkazildi:\n\n"
                f"Username: {username}\n"
                f"To'lov summasi: {tulov_summasi}\n"
                f"Bio: {bio}"
            )
        }
        
        response = post(url, data=data, files=files)
        
        if response.status_code == 200:
            return "To'lov haqidagi ma'lumotlar yuborildi foydalanuvchiga!"
        else:
            return f"Xato: {response.text}"
    except Exception as e:
        return f"Xato: {e}"


# check user payment function end

# get data serializer functions start
def serialize_forregister(row):
    return {
        "id": row.id,
        "tg_id": row.tg_id,
        "phone": row.phone,
        "token": row.token,
        "created_at": row.created_at
    }
def serialize_users(row):
    return {
        "full_name": row.full_name,
        "username": row.username,
        "email": row.email,
        "phone": row.phone,
        "sex": row.sex,
        "tg_id": row.tg_id,
        "balance": row.balance,
        "created_at": row.created_at,
        "updated_at": row.updated_at,
        "last_login": row.last_login,
        "code": row.code,
        "reset_code": row.reset_code,
        "how_online": row.how_online,
        "token": row.token
    }
def serialize_reports_balance(row):
    return {
        "id": row.id,
        "user_id": row.user_id,
        "balance": row.balance,
        "tulov_summasi": row.tulov_summasi,
        "bio": row.bio,
        "created_at": row.created_at
    }
def serialize_payment(row):
    return {
        "id": row.id,
        "admin_id": row.admin_id,
        "user_id": row.user_id,
        "tulov_summasi": row.tulov_summasi,
        "payment_chek_img": row.payment_chek_img,
        "bio": row.bio,
        "created_at": row.created_at
    }
def serialize_products(row):
    return {
        "id": row.id,
        "name": row.name,
        "bio": row.bio,
        "settings": row.settings,
        "created_at": row.created_at,
        "updated_at": row.updated_at
    }
def serialize_school_data(row):
    return {
        "id": row.id,
        "user_id": row.user_id,
        "viloyat": row.viloyat,
        "tuman": row.tuman,
        "school_number": row.school_number
    }
def serialize_pckundalikcom(row):
    return {
        "id": row.id,
        "user_id": row.user_id,
        "start_active_date": row.start_active_date,
        "end_active_date": row.end_active_date,
        "device_id": row.device_id,
        "end_use_date": row.end_use_date
    }
def serialize_mobilekundalikcom(row):
    return {
        "id": row.id,
        "user_id": row.user_id,
        "start_active_date": row.start_active_date,
        "end_active_date": row.end_active_date,
        "device_id": row.device_id,
        "end_use_date": row.end_use_date
    }
def serialize_majburiyobuna(row):
    return {
        "id": row.id,
        "device_id": row.device_id
    }
def serialize_admins(row):
    return {
        "id": row.id,
        'full_name': row.full_name,
        'phone': row.phone,
        'email': row.email,
        'username': row.username,
        'password': row.password,
        'sex': row.sex,
        'tg_id': row.tg_id,
        'active': row.active,
        'premessions': row.premessions,
        'created_at': row.created_at,
        'updated_at': row.updated_at
    }
def serialize_get_all_telegram_ids(row):
    return {
        "tg_id": row.tg_id
    }
def serialize_get_all_phone_numbers(row):
    return {
        "full_name": row.full_name,
        "phone": row.phone
    }
def serialize_get_projectsdata(row):
    return {
        'id': row.id,
        'name': row.name,
        'email': row.email,
        'domen': row.domen,
        'telegram_chaneel': row.telegram_chaneel,
        'youtube': row.youtube,
        'telegram_group': row.telegram_group,
        'telegram_bot': row.telegram_bot,
        'about': row.about,
        'balance': row.balance,
        'created_at': row.created_at,
        'updated_at': row.updated_atsssss

    }
# get data serializer functions end
