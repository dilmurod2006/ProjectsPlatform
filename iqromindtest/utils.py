
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
# from models.models import loginsdata
fanlar = [
    "O'zbekcha",
    "Ruscha",

    "Ingilizcha",
    "Qozoqcha"
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
        "javoblar": " "*420,
        "tekshirishlar": {}
    }
    return data


def generate_token(length=8):
    # Token uchun raqamlar, harflar va maxsus belgilarni tanlash
    characters = string.ascii_letters + string.digits  # harflar va raqamlar
    token = ''.join(random.choice(characters) for _ in range(length))
    return token

def string_to_number(data):
    data = data[1].split("|")[0]
    res = data.split(".")
    # umumiy balni hixoblash
    ball =  int(res[0])*11 + int(res[1])*21 + int(res[2])*31
    return ball
def sort_dict(d: dict, page: int):
    if True:
        # Tartiblash: kattadan kichikka qarab
        ballar = set()
        sorted_items = sorted(d.items(), key=string_to_number, reverse=True)
        for i in sorted_items[:page*10]:
            ballar.add(string_to_number(i))
        birxillar_soni = page*10 - len(ballar)
        return sorted_items[page*10:10+page*10], birxillar_soni
    else:
        return [], 0
if __name__ == "__main__":
    print(sort_dict({
    "0": "0.0.0|aseawdawdawd",
    "1001": "4.0.0|aseawdawdawd",
    "1002": "2.0.0|aseawdawdawd",
    "1004": "4.0.0|aseawdawdawd",
    "1005": "4.0.0|aseawdawdawd",
    "1006": "9.0.0|aseawdawdawd",
    "1007": "10.0.0|aseawdawdawd",
    "1008": "0.10.0|aseawdawdawd",
    "1009": "0.0.0|aseawdawdawd",
    "1010": "0.0.0|aseawdawdawd",
    "1011": "0.0.0|aseawdawdawd",
    }))
    