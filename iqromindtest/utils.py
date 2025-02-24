
from sqlalchemy.ext.asyncio import AsyncSession
import requests, telebot
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
from settings import IQROMINDTEST_POST_TEXT, IQROMINDTEST_MUAMMOLAR_GURUH_ID, IQROMINDTEST_BOT_TOKEN, IQROMIND_BOT_USERNAME
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
        "bio": ".",
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
        if ser == 1:
            for i in d.keys():
                send_muammo_func(d[i][-3:], 0, "1", True)
                if d[i][-3:] == "0.0":
                    d.pop(i)
        elif ser == -1:
            for i in d.keys():
                send_muammo_func(d[i][-3:], 0, "2", True)
                if d[i][-3:] != "0.0":
                    d.pop(i)
        # Tartiblash: kattadan kichikka qarab
        sorted_items = sorted(d.items(), key=string_to_number, reverse=True)
        all_pages = len(sorted_items) // 10 + int(len(sorted_items) % 10 > 0)
        max_ball = -1
        add_qiymat = 0
        for natija_data in sorted_items[:page*10]:
            ball = string_to_number(natija_data)
            if ball == max_ball:
                add_qiymat += 1
            else:
                max_ball = ball
                add_qiymat = 0
        results = []
        for i, natija_data in enumerate(sorted_items[page*10: min(len(sorted_items), (page+1)*10)]):
            ball = string_to_number(natija_data)
            if ball == max_ball:
                add_qiymat += 1
            else:
                max_ball = ball
                add_qiymat = 0
            results.append([*natija_data, page*10 - add_qiymat + i + 1])
        return results, all_pages
    except Exception as e:
        send_muammo_func(str(e), 0, "1", True)
        return [], 0

# Post formatni textga o'zgartirish
def post_format_text(format_text, sana, test_name, bio, qatnashchilar_soni):
    format_text = format_text.replace("$test_name", test_name)
    format_text = format_text.replace("$izoh", bio)
    format_text = format_text.replace("$sana", sana)
    format_text = format_text.replace("$qatnashchilar_soni", str(qatnashchilar_soni))
    return format_text
def post_format_text_html(format_text, sana, test_name, bio, qatnashchilar_soni, premium):
    text = post_format_text(format_text, sana, test_name, bio, qatnashchilar_soni)
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
    if not premium:
        html += "\n"+IQROMINDTEST_POST_TEXT
    return html

def send_muammo_func(matn, user_id, fullname, premium=False):
    bot = telebot.TeleBot(IQROMINDTEST_BOT_TOKEN)
    bot.send_message(
        IQROMINDTEST_MUAMMOLAR_GURUH_ID,
        f"""{'🔶' if premium else '🔷'}<b><a href="https://t.me/{IQROMIND_BOT_USERNAME}?start=show_user{user_id}">{fullname}</a></b>\n💬Xabar:\n<blockquote>{matn}</blockquote>""",
        parse_mode="HTML",
        disable_web_page_preview=True
    )

if __name__ == "__main__":
    print(sort_dict({
    "0": "0.0.0|BQACAgIAAxkDAAIF1We4oMxgRq4SyaD1B0HXOUDgZ86vAAIlYwACPNzBSSPl4wgJczjuNgQ|0.1|1|0.0",
    "1001": "3.0.0|BQACAgIAAxkDAAIF1We4oMxgRq4SyaD1B0HXOUDgZ86vAAIlYwACPNzBSSPl4wgJczjuNgQ|0.1|1|0.0",
    "1002": "0.2.1|BQACAgIAAxkDAAIF1We4oMxgRq4SyaD1B0HXOUDgZ86vAAIlYwACPNzBSSPl4wgJczjuNgQ|0.1|1|0.0",
    "1004": "2.2.1|BQACAgIAAxkDAAIF1We4oMxgRq4SyaD1B0HXOUDgZ86vAAIlYwACPNzBSSPl4wgJczjuNgQ|0.1|1|0.0",
    "1005": "0.2.1|BQACAgIAAxkDAAIF1We4oMxgRq4SyaD1B0HXOUDgZ86vAAIlYwACPNzBSSPl4wgJczjuNgQ|0.1|1|0.0",
    "1006": "1.0.0|BQACAgIAAxkDAAIF1We4oMxgRq4SyaD1B0HXOUDgZ86vAAIlYwACPNzBSSPl4wgJczjuNgQ|0.1|1|0.0",
    "1007": "0.1.0|BQACAgIAAxkDAAIF1We4oMxgRq4SyaD1B0HXOUDgZ86vAAIlYwACPNzBSSPl4wgJczjuNgQ|0.1|1|0.0",
    "1008": "0.0.1|BQACAgIAAxkDAAIF1We4oMxgRq4SyaD1B0HXOUDgZ86vAAIlYwACPNzBSSPl4wgJczjuNgQ|0.1|1|0.0",
    "1009": "0.0.0|BQACAgIAAxkDAAIF1We4oMxgRq4SyaD1B0HXOUDgZ86vAAIlYwACPNzBSSPl4wgJczjuNgQ|0.1|1|0.0",
    "1010": "0.0.0|BQACAgIAAxkDAAIF1We4oMxgRq4SyaD1B0HXOUDgZ86vAAIlYwACPNzBSSPl4wgJczjuNgQ|0.1|1|0.0",
    "1011": "0.0.0|BQACAgIAAxkDAAIF1We4oMxgRq4SyaD1B0HXOUDgZ86vAAIlYwACPNzBSSPl4wgJczjuNgQ|0.1|1|0.0",
}, 1, 0))
