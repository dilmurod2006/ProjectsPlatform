
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
    ball =  int(res[0])*11 + int(res[1])*31 + int(res[2])*21
    return ball
def sort_dict(d: dict, page: int, ser: int):
    try:
        # Tartiblash: kattadan kichikka qarab
        for i in d.keys():
            if ser != 0 and (ser == -1 or d[i][-3:] == "0.0") and (ser == 1 or d[i][-3:] != "0.0"):
                d.pop(i)

        sorted_items = sorted(d.items(), key=string_to_number, reverse=True)
        max_ball = -1
        add_qiymat = 0
        for i in sorted_items[:page*10]:
            ball = string_to_number(i)
            if ball == max_ball:
                add_qiymat += 1
            else:
                max_ball = string_to_number(i)
                add_qiymat = 0
        return sorted_items[page*10:10+page*10], {
            "max_ball": max_ball/10,
            "add_qiymat": add_qiymat
        }
    except:
        return {"max_ball": -1, "add_qiymat": 0}
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

# Post formatni textga o'zgartirish
def post_format_text(format_text, sana, test_name, qatnashchilar_soni):
    format_text = format_text.replace("$test_name", test_name)
    format_text = format_text.replace("$sana", sana)
    format_text = format_text.replace("$qatnashchilar_soni", str(qatnashchilar_soni))
    return format_text
def post_format_text_html(format_text, sana, test_name, qatnashchilar_soni):
    text = post_format_text(format_text, sana, test_name, qatnashchilar_soni)
    text = text.replace("\n", "<br>")
    html = ""
    ochilishlar = ""
    for v in text:
        if v == "*":
            if ochilishlar == "" or ochilishlar == "i":
                ochilishlar += "b"
                html += "<b>"
            elif ochilishlar == "b":
                ochilishlar = ""
                html += "</b>"
            elif ochilishlar == "ib":
                ochilishlar = "i"
                html += "</b>"
            else:
                ochilishlar = "i"
                html += "</i></b><i>"
        elif v == "~":
            if ochilishlar == "" or ochilishlar == "b":
                ochilishlar += "i"
                html += "<i>"
            elif ochilishlar == "i":
                ochilishlar = ""
                html += "</i>"
            elif ochilishlar == "bi":
                ochilishlar = "b"
                html += "</i>"
            else:
                ochilishlar = "b"
                html += "</b></i><b>"
        else:
            html += v
    if ochilishlar == "i":
        html += "</i>"
    elif ochilishlar == "b":
        html += "</b>"
    elif ochilishlar == "ib":
        html += "</b></i>"
    elif ochilishlar == "bi":
        html += "</i></b>"
    return html

