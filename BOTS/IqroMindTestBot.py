import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from api_functions import create_user

TOKEN = "7536980017:AAGtgsiLdVOU3nCY6dhdbVQguPqysUo4qSY"
bot = telebot.TeleBot(TOKEN)

text_start = """
👋 Assalomu alaykum, Iqro Mind test botiga xush kelibsiz!
BU bot orqali siz O'quv markazdai offline block testga qatnashgan natijangizni online ko'rsangiz bo'ladi,
va bu botda 2024-yilgi O'zbekistoning Oliy Ta'liim markazlarni kirish ballari bor bu bilan siz o'zingizni natijangizni solishtirib borishingiz va 
avto statiska shaklanib boradi sizga juda qulay ko'rinishda natijalaringizni tahlil qiishingiz mumkin!
"""

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text_start)
    
    # Yangi foydalanuvchi yaratish
    user_id = create_user(first_name=message.from_user.first_name, tg_id=message.chat.id)
    
    # Inline keyboard yaratamiz
    markup = InlineKeyboardMarkup()
    profile_link = f"https://yourwebsite.com/profile/{user_id}"  # Linkni o'zgartiring
    btn = InlineKeyboardButton("🔗 Profilingizni ko'rish", url=profile_link)
    markup.add(btn)
    
    # Foydalanuvchiga inline tugma yuborish
    bot.send_message(message.chat.id, f"ID: {user_id}", reply_markup=markup)

bot.polling()
