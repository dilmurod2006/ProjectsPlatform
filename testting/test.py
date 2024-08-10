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


token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRldmxvcGVyMDA2IiwicGFzc3dvcmQiOiJkaWxtdXJvZDE5NTciLCJ0Z19pZCI6NTQyMDA3MTgyNCwiZXhwIjoxNzg2NDM4MjU2fQ.n312R1XwtKiwQkYTz23qKjAAd8uJXLdkrfgfTznj9YM"
SECRET_KEY_FOR_ADMINS = "LG6KoNEO5zdYWJ0BdAL2006NYQ9o15Ob1-zALTWt1IVUltPpIh-Fkv4zl1HVCz58oxvAt8iYCrzq_V_fr6tiP6AAPFx1957BVkSQ5khyF_hCgR2m-afB8TK@02328Ann1BATTOxe_STgmYgTZ5ulCymxZm_UQhsyrykKBd336Ii0mvjUiW3ybVu6noB2s5imn3yw4pPJaqN9B5NbDgTaQo9OJoiwsyX0J026FwP8FjafZc4UzUzmwMJrzL1zD6WAZIoy-ez7hSb43G-spC7LJhXrUXUDR7WW5I_Aaqf3-5Fl3LLfLcdtpDLrHw"
# JWT uchun maxfiy kalit va algoritm
ALGORITHM = "HS256"

def decode_jwt_token(token: str) -> Dict[str, str]:
    """
    JWT tokenni dekodlash va tekshirish.

    Args:
        token (str): JWT token.

    Returns:
        dict: Dekodlangan ma'lumotlar.
    """
    try:
        return jwt.decode(token, SECRET_KEY_FOR_ADMINS, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

res = decode_jwt_token(token=token)
print(res)
