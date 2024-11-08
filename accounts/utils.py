from datetime import datetime,timedelta

import hashlib

from fastapi import HTTPException
import jwt

from typing import Dict

import os

import binascii

from requests import post, get

from settings import BOT_TOKEN, SECRET_KEY, ALGORITHM
import re


# password hashing
def hash_password(password: str) -> str:
    """Parolni hash qilish."""
    salt = binascii.hexlify(os.urandom(16)).decode()
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return salt + '$' + binascii.hexlify(pwdhash).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Hashlangan parolni tekshirish."""
    salt, stored_password = hashed_password.split('$')
    pwdhash = hashlib.pbkdf2_hmac('sha256', plain_password.encode(), salt.encode(), 100000)
    return binascii.hexlify(pwdhash).decode() == stored_password

# generate token for forregister
def generate_token_for_forregister(data: Dict[str, str], expires_delta: timedelta = timedelta(minutes=15)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# jwt token for users
def generate_token_for_users(data: Dict[str, str], expires_delta: timedelta = timedelta(days=183)) -> str:
    """
    JWT token yaratish.

    Args:
        data (dict): Token ichiga qo'shiladigan ma'lumotlar (masalan, username va password).
        expires_delta (timedelta): Tokenning amal qilish muddati. har 6oyda token almashitiriladi.
        Yani token eskiradi va login qiladi qaytdan.

    Returns:
        str: Yaratilgan JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token: str) ->dict:
    try:
        # Tokenni dekodlash
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
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

def decode_jwt_token(token: str) -> Dict[str, str]:
    """
    JWT tokenni dekodlash va tekshirish.

    Args:
        token (str): JWT token.

    Returns:
        dict: Dekodlangan ma'lumotlar.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# send message to user login code using telegram bot
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
        "text": f"Sizning tasdiqlash kodingiz: {reset_code}",
    }
    post(url, data)

    return f"parolni tiklovchi code yuborildi!"


# usernameni tekshirish
# Foydalanuvchi nomini tekshirish uchun funksiya
def validate_username(username: str) -> bool:
    """Username faqat harflar, raqamlar, va pasti chiziqcha (_) dan iborat bo'lishi kerak.
    Uzunligi 25 belgidan oshmasligi kerak."""
    if len(username) > 25:
        raise HTTPException(status_code=400, detail="Usernameingiz juda uzun 25ta belgidan oshmasligi kerak!")
    
    # Regex orqali validatsiya qilamiz
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise HTTPException(status_code=400, detail="Foydalanuvchi nomi faqat harflar, raqamlar va pastki chiziqdan iborat bo'lishi mumkin!")
    
    return True
