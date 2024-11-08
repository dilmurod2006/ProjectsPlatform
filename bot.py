import telebot
from telebot import types
import requests
from typing import Dict
import re
from settings import (
    ADMIN_DILMUROD,
    ADMIN_BEXRUZDEVELOPER,
    BOT_TOKEN,
    API_FORREGISTER_SECRET_KEY,
    CHEACK_USER_FOR_BOT
)

# Telegram bot tokenini kiritish
bot = telebot.TeleBot(BOT_TOKEN)
# bot = telebot.TeleBot("7486708710:AAFDApDU5kvV9M7bDaXjO4zd5icIgkNHH3s")

# Foydalanuvchi uchun ma'lumotlarni saqlash uchun dict
user_data: Dict[int, Dict[str, str]] = {}

def check_user(tg_id: int) -> Dict:
    """Foydalanuvchi ro'yxatdan o'tganligini tekshiradi."""
    response = requests.get(f"https://api.projectsplatform.uz/accounts/check_user?KeySecret={CHEACK_USER_FOR_BOT}&tg_id={tg_id}")
    
    if response.status_code == 200:
        return response.json()  # Foydalanuvchi ma'lumotlarini qaytaradi
    elif response.status_code == 400:
        raise Exception(response.json().get("detail"))
    else:
        raise Exception("Noma'lum xatolik yuz berdi.")

def create_for_register(tg_id: int, phone: str, ref_id: int) -> str:
    """API orqali ro'yxatdan o'tish uchun token yaratish."""
    response = requests.post("https://api.projectsplatform.uz/accounts/for_register_bot_api", json={
        "secret_key": API_FORREGISTER_SECRET_KEY,
        "tg_id": tg_id,
        "phone": phone,
        "ref_id": str(ref_id)
    })
    
    if response.status_code == 200:
        return response.json().get("token")
    else:
        error_message = response.json().get("detail")
        raise Exception(error_message)

def is_valid_phone_number(phone: str) -> bool:
    """Telefon raqamini O'zbekiston raqamiga mosligini tekshiradi."""
    return bool(re.match(r'^\+998[1-9][0-9]{8}$', phone)) or bool(re.match(r'^998[1-9][0-9]{8}$', phone))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Foydalanuvchi start bosganda ro'yxatdan o'tganligini tekshiradi."""
    chat_id = message.chat.id
    if message.text == "/start download":
        try:
            bot.send_document(chat_id, open("kundalikcom.txt", "r").readlines()[-1].split("|")[1].strip(), caption=f"KundalikCOM avto login (Desktop)\nVersiya: {open('kundalikcom.txt', 'r').readlines()[-1].split('|')[0].strip()}\n\nTizim: Windows 10/11 - 64x\nMinimum ram: 2 GB\nMinimum video karta: 512 MB\n")
            return
        except:
            pass
    try:
        user_info = check_user(tg_id=chat_id)
        # Agar foydalanuvchi ro'yxatdan o'tgan bo'lsa, ma'lumotlarini yuborish
        message = user_info.get("message")
        full_name = user_info.get("full_name")
        balance = user_info.get("balance")
        username = user_info.get("username")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Kabinetga kirish", url="https://projectsplatform.uz/login"))
        bot.send_message(chat_id, f"Assalomu alaykum *{full_name}*!\n👤 Username: *{username}*\n💵 Sizning balansingiz: *{balance:,}* so'm", parse_mode="markdown", reply_markup=markup)
    except Exception as e:
        # Agar foydalanuvchi ro'yxatdan o'tmagan bo'lsa, ro'yxatdan o'tish uchun yo'naltirish
        if chat_id in user_data:
            ref_id = user_data[chat_id]['ref_id']
        else:
            user_data[chat_id] = dict()
            ref_id = "-"
        try:
            ref_id = int(message.text.split()[1])

        except:
            if message.text == "/start download":
                try:
                    bot.send_document(chat_id, open("kundalikcom.txt", "r").readlines()[-1].split("|")[1].strip(), caption=f"KundalikCOM avto login (Desktop)\nVersiya: {open('kundalikcom.txt', 'r').readlines()[-1].split('|')[0].strip()}\n\nTizim: Windows 10/11 - 64x\nMinimum ram: 2 GB\nMinimum video karta: 512 MB\n")
                    return
                except:
                    pass
        user_data[chat_id]['ref_id'] = str(ref_id)
        if ref_id != "-":
            bot.forward_message(chat_id, "@PyPrime", 121)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton('Telefon raqamni berish', request_contact=True))
        bot.send_message(chat_id, "Ro'yxatdan o'tish uchun telefon raqamingizni yuboring:", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    """Foydalanuvchi telefon raqamini yuborganda ishlatiladi."""
    chat_id = message.chat.id
    if message.contact is not None:
        phone = message.contact.phone_number
        if is_valid_phone_number(phone):
            user_data[chat_id]['phone'] = phone
            try:
                token = create_for_register(tg_id=chat_id, phone=phone, ref_id=user_data[chat_id]['ref_id'])
                bot.send_message(chat_id, f"Kontakt ma'lumotlaringiz muvaffaqiyatli yuborildi!", reply_markup=types.ReplyKeyboardRemove())
                
                # Davom etish uchun inline tugma
                bot.send_message(chat_id, f"Ro'yxatdan o'tish uchun quyidagi tugmani bosing:", reply_markup=types.InlineKeyboardMarkup([[
                    types.InlineKeyboardButton("Davom etish", url=f"https://projectsplatform.uz/register?token={token}")
                ]]))
            except Exception as e:
                bot.send_message(chat_id, str(e))
        else:
            bot.send_message(chat_id, "Telefon raqamingiz O'zbekiston raqami (+998) bilan boshlanishi kerak.")

if __name__ == "__main__":
    try:
        bot.polling()
    except:
        pass
