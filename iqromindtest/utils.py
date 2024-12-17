
from sqlalchemy.ext.asyncio import AsyncSession
import requests
import random
import string
from sqlalchemy import(
    select,
    delete
)
from bs4 import BeautifulSoup
from urllib.parse import unquote
from fastapi import Depends, HTTPException
from typing import Dict
from models.models import loginsdata
fanlar = [
    "matematika",
    "fizika",

    "ona tili",
    "kimyo",
    "biologiya",
    "tarix",

    "geografiya",
    "ingliz tili",
    "rus tili",
    "huquq"
]

def months_size_price(month: int, year: int, months_count: int) -> int:
    if months_count <= 0:
        return 0
    return month*(months_count%12) + year * (months_count//12)

def create_test(name, date):
    date_str = date.strftime("%d.%m.%Y")
    data = {
        "name": name,
        "bio": "",
        "date": date_str,
        "javoblar": " "*410,
        "tekshirishlar": {}
    }
    return data


def generate_token(length=8):
    # Token uchun raqamlar, harflar va maxsus belgilarni tanlash
    characters = string.ascii_letters + string.digits  # harflar va raqamlar
    token = ''.join(random.choice(characters) for _ in range(length))
    return token

