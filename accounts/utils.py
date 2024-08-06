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

from settings import BOT_TOKEN, SECRET_KEY, ALGORITHM


# password hashing
def hash_password(password: str) -> str:
    """Parolni hash qilish."""
    salt = binascii.hexlify(os.urandom(16)).decode()
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return salt + '$' + binascii.hexlify(pwdhash).decode()
# Misol uchun parol
# hashed_password = hash_password(secure_password)
# print(len(hashed_password))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Hashlangan parolni tekshirish."""
    salt, stored_password = hashed_password.split('$')
    pwdhash = hashlib.pbkdf2_hmac('sha256', plain_password.encode(), salt.encode(), 100000)
    return binascii.hexlify(pwdhash).decode() == stored_password



# generate token for forregister
def generate_token_for_forregister(length=32):
    """32 ta simvoldan iborat tokenni yaratadi."""
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(length))
    return token


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
        "text": f"Your login code is: {code}",
    }
    post(url, data)

    return f"code yuborildi!"