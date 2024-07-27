import telebot
from telebot import types
import requests
from Accounts.schemas import TokenRequest
from typing import Dict
import re

# Telegram bot tokenini kiritish
API_TOKEN = '6651751855:AAHKbRLbwupDBCVIFv01d8_m9rvjCQcPYfA'
bot = telebot.TeleBot(API_TOKEN)

# Foydalanuvchi uchun ma'lumotlarni saqlash uchun dict
user_data: Dict[int, Dict[str, str]] = {}

def create_temp_account(tg_id: int, phone: str) -> str:
    """API orqali token yaratish."""
    response = requests.post("http://localhost:8000/generate-token", json={
        "tg_id": tg_id,
        "phone": phone
    })
    
    if response.status_code == 200:
        return response.json().get("token")
    else:
        raise Exception("Token yaratishda xatolik yuz berdi.")

def is_valid_phone_number(phone: str) -> bool:
    """Telefon raqamining O'zbekiston raqamiga mosligini tekshiradi.
       Masalan: O'zbekiston code:+998 dan boshlanadi
       agar boshqa davlatning raqami berilsa qabul qilmaydi.
    """
    return bool(re.match(r'^\+998[0-9]{9}$', phone))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Foydalanuvchi start bosganda ishlatiladi."""
    chat_id = message.chat.id
    user_data[chat_id] = {}
    user_data[chat_id]['tg_id'] = chat_id

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton('Telefon raqamni berish', request_contact=True))
    bot.send_message(chat_id, "Telefon raqamingizni yuboring:", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    """Foydalanuvchi telefon raqamini yuborganda ishlatiladi."""
    chat_id = message.chat.id
    if message.contact is not None:
        phone = message.contact.phone_number
        if is_valid_phone_number(phone):
            user_data[chat_id]['phone'] = phone

            try:
                token = create_temp_account(tg_id=chat_id, phone=phone)
                bot.send_message(chat_id, f"Vaqtinchalik account yaratildi.\nToken: {token}\nBot link: http://localhost:8000/create-user/{token}", reply_markup=types.ReplyKeyboardRemove())
            except Exception as e:
                bot.send_message(chat_id, str(e))
        else:
            bot.send_message(chat_id, "Telefon raqamingiz O'zbekiston raqami (+998) bilan boshlanishi kerak.")

if __name__ == "__main__":
    bot.polling()
