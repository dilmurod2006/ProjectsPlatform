import telebot
from telebot import types
import requests
from typing import Dict
import re
from settings import (
    ADMIN_DILMUROD,
    ADMIN_BEXRUZDEVELOPER,
    BOT_TOKEN,
    API_ACTIVATION_ACCOUNT_SECRET_KEY,
    CHEACK_USER_FOR_BOT
)

start_text = """
*Assalomu alaykum! Xush kelibsiz!*

*ProjectsPlatform* — maktablarga yengillik yaratish uchun raqamli yechim.  
KundalikCOM auto login dasturi yordamida o'quvchilar va ota-onalar tizimga tezda kirishlari mumkin.

*Nima uchun bu xizmat kerak?*
Barcha foydalanuvchilarni tizimga avtomatik kiritish va reytingni oshirish uchun qulay imkoniyat.

*Xizmat qanday ishlaydi?*
- *Avtomatik login* va parollarni tez kiritish.
- *Bitta administrator paroli* bilan boshqarish.
- *Online tizim yig'ish* va foydalanuvchilarni boshqarish.

*Mobile variant* ham mavjud. Hozir ro'yxatdan o'ting!
"""





# Telegram bot tokenini kiritish
bot = telebot.TeleBot(BOT_TOKEN)
# bot = telebot.TeleBot("7486708710:AAFDApDU5kvV9M7bDaXjO4zd5icIgkNHH3s")

# Foydalanuvchi uchun ma'lumotlarni saqlash uchun dict
user_data: Dict[int, Dict[str, str]] = {}

def check_user(tg_id: int) -> Dict:
    """Foydalanuvchi ro'yxatdan o'tganligini tekshiradi."""
    response = requests.get(f"http://localhost:8000/accounts/check_user?KeySecret={CHEACK_USER_FOR_BOT}&tg_id={tg_id}")
    
    if response.status_code == 200:
        return response.json()  # Foydalanuvchi ma'lumotlarini qaytaradi
    elif response.status_code == 400:
        raise Exception(response.json().get("detail"))
    else:
        raise Exception("Noma'lum xatolik yuz berdi.")

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
    elif message.text == "/start download_mobile":
        try:
            bot.send_document(chat_id, open("kundalikcom_mobile.txt", "r").readlines()[-1].split("|")[1].strip(), caption=f"Dasturni telefoningizga yuklab oling va xizmatimizdan foydalaning")
            return
        except:
            pass
    elif message.text != "/start":
        token = message.text.split()[1]
        user_data[chat_id] = {
            "token": token,
        }


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

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(types.KeyboardButton('Telefon raqamni berish', request_contact=True))
            bot.send_message(chat_id, "Telefon raqamingizni tasdiqlang", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Ro'yxatdan o'tish", url="https://projectsplatform.uz"))
        bot.send_message(message.chat.id, start_text, parse_mode="Markdown", reply_markup=markup)
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    """Foydalanuvchi telefon raqamini yuborganda ishlatiladi."""
    chat_id = message.chat.id
    if message.contact is not None:
        phone = message.contact.phone_number
        if is_valid_phone_number(phone):
            user_data[chat_id]['phone'] = phone
            user = user_data[chat_id]
            try:
                res = requests.post("http://localhost:8000/accounts/activation_account", json={
                    "secret_key": API_ACTIVATION_ACCOUNT_SECRET_KEY,
                    "token": user["token"],
                    "tg_id": chat_id,
                    "phone": user["phone"],
                })
                print(res.json())
                bot.send_message(chat_id, f"Hisobingiz muvaffaqiyatli aktivatsiya qilindi", reply_markup=types.ReplyKeyboardRemove())
            except Exception as e:
                bot.send_message(chat_id, "Nimadur xato ketdi qayta urinib ko'ring")
        else:
            bot.send_message(chat_id, "Telefon raqamingiz O'zbekiston raqami (+998) bilan boshlanishi kerak.")

while __name__ == "__main__":
    # bot.polling()
    try:
        bot.polling()
    except:
        pass
