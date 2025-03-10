import telebot
from telebot import types
import requests
# from Accounts.schemas import TokenRequest
from typing import Dict
import re
from settings import ADMIN_DILMUROD, ADMIN_BEXRUZDEVELOPER, BOT_TOKEN

# Telegram bot tokenini kiritish
bot = telebot.TeleBot(BOT_TOKEN)

# Foydalanuvchi uchun ma'lumotlarni saqlash uchun dict
user_data: Dict[int, Dict[str, str]] = {}

def create_temp_account(tg_id: int, phone: str) -> str:
    """API orqali token yaratish."""
    response = requests.post("http://localhost:8000/accounts/for_register_bot_api", json={
        "tg_id": tg_id,
        "phone": phone
    })
    
    if response.status_code == 200:
        return response.json().get("token")
    else:
        error_message = response.json().get("detail")
        raise Exception(error_message)  # Exception yoki boshqa mos xato

def is_valid_phone_number(phone: str) -> bool:
    """Telefon raqamining O'zbekiston raqamiga mosligini tekshiradi.
       Masalan: O'zbekiston code:+998 dan boshlanadi
       agar boshqa davlatning raqami berilsa qabul qilmaydi.
    """
    return bool(re.match(r'^\+998[1-9][0-9]{8}$', phone))

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
                bot.send_message(chat_id, f"Vaqtinchalik account yaratildi.\nToken:{token} token\nBot link: http://localhost:8000/create-user/{token}", reply_markup=types.ReplyKeyboardRemove())
            except Exception as e:
                bot.send_message(chat_id, str(e))
        else:
            bot.send_message(chat_id, "Telefon raqamingiz O'zbekiston raqami (+998) bilan boshlanishi kerak.")

if __name__ == "__main__":
    bot.polling()