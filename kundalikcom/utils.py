
from sqlalchemy.ext.asyncio import AsyncSession
import requests
from sqlalchemy import(
    select,
    delete
)
from bs4 import BeautifulSoup
from urllib.parse import unquote
from fastapi import Depends, HTTPException
from typing import Dict
from models.models import loginsdata


def months_size_price(months_count: int, month_price: int, month_chegirma: int) -> int:
    months_count = months_count
    months_count -= 3*(months_count//12)
    if months_count < 3:
        return month_price*months_count
    return month_chegirma*months_count

def months_size_price_mobile(months_count: int, month_price: int, month_chegirma: int) -> int:
    months_count = months_count
    if months_count < 3:
        return month_price*months_count
    return month_chegirma*months_count

async def get_user_logins(user_id: int, session: AsyncSession) -> Dict[str, str]:
    # Ma'lumotlarni olish
    result = await session.execute(select(loginsdata).filter_by(user_id=user_id))
    # Malumotlar olingandan keyin uchirib tashlash
    await session.execute(delete(loginsdata).filter_by(user_id=user_id))
    rows = result.fetchall()

    # Loginlar va parollarni dict ga saqlash
    login_password_dict = {row.login: row.password for row in rows}

    return login_password_dict



# login qo'shish uchun login parolni tekshirish
async def login_user_check(login_data):
    login, parol, capcha_id, capcha_value  = login_data.login, login_data.parol, login_data.capcha_id, login_data.capcha_value
    try:
        if capcha_id != "":
            r = requests.post(
                "https://login.emaktab.uz/",
                {"exceededAttempts": "True", "login": login, "password": parol, "Captcha.Input": capcha_value, "Captcha.Id": capcha_id},
            )
            soup = BeautifulSoup(r.content, "html.parser")
            if "Chiqish" in soup.get_text():
                return True, {"how": True}
            elif soup.find_all(class_="message")[0].get_text().strip() == "Parol yoki login notoʻgʻri koʻrsatilgan. Qaytadan urinib koʻring.":
                return False, {"how": False, "capcha": False, "message": "Login yoki parol xato"}
            else:
                try:
                    capcha_id = unquote(r.cookies.get('sst')).split("|")[0]
                    url = f"https://login.emaktab.uz/captcha/True/{capcha_id}"
                    return False, {"how": False, "capcha": True, "capcha_id": capcha_id, "url": url, "message": "Rasmdagi raqamlarni xato kiritdingiz"}
                except:
                    return False, {"how": False, "capcha": False, "message": "Ayni paytda eMaktab.uz sayti profilaktikada keyinroq urinib ko'ring"}
        r = requests.post(
            "https://login.emaktab.uz/",
            {"exceededAttempts": "True", "login": login, "password": parol},
        )
        soup = BeautifulSoup(r.content, "html.parser")
        if "Chiqish" in soup.get_text():
            return True, {"how": True}
        else:
            if soup.find_all(class_="message")[0].get_text().strip() == "Parol yoki login notoʻgʻri koʻrsatilgan. Qaytadan urinib koʻring.":
                return False, {"how": False, "capcha": False, "message": "Login yoki parol xato"}
            else:
                try:
                    capcha_id = unquote(r.cookies.get('sst')).split("|")[0]
                    url = f"https://login.emaktab.uz/captcha/True/{capcha_id}"
                    return False, {"how": False, "capcha": True, "capcha_id": capcha_id, "url": url}
                except:
                    return False, {"how": False, "capcha": False, "message": "Ayni paytda eMaktab.uz sayti profilaktikada keyinroq urinib ko'ring"}
    except requests.exceptions.ConnectionError:
        return False, {"how": False, "capcha": False, "message": "Nimadur xato ketdi qayta urinib ko'ring"}
    except:
        return False, {"how": False, "capcha": False, "message": "Nimadur xato ketdi qayta urinib ko'ring"}
