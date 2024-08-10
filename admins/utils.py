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




# generate jwt token for admin
def generate_token_for_admin(data: Dict[str, str], expires_delta: timedelta = timedelta(days=731)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY_FOR_ADMINS, algorithm=ALGORITHM)

def verify_jwt_token(token: str):
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
