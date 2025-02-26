import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from api_functions import create_user,check_user

TOKEN = "7536980017:AAGtgsiLdVOU3nCY6dhdbVQguPqysUo4qSY"
bot = telebot.TeleBot(TOKEN)
BaseUrl = f"https://yourwebsite.com/profile/"  # Linkni o'zgartiring

text_start = """
👋 Assalomu alaykum, Iqro Mind test botiga xush kelibsiz!
BU bot orqali siz O'quv markazdai offline block testga qatnashgan natijangizni online ko'rsangiz bo'ladi,
va bu botda 2024-yilgi O'zbekistoning Oliy Ta'liim markazlarni kirish ballari bor bu bilan siz o'zingizni natijangizni solishtirib borishingiz va 
avto statiska shaklanib boradi sizga juda qulay ko'rinishda natijalaringizni tahlil qiishingiz mumkin!
"""

@bot.message_handler(commands=['start'])
def start(message):
    text = message.text 
    if "=" in text:
        data = text.split("=")[1]  # "user_id@test_key@month_date"
        parts = data.split("@")  # ["user_id", "test_key", "month_date"]

        if len(parts) == 3:
            user_id, test_key, month_date = parts
            # check user
            user_check = check_user(message.chat.id)
            if user_check["mes"]==True:
                btn = InlineKeyboardButton("🔗 Test natijani ko'rish", url=f"{BaseUrl}/{user_id}/{test_key}/{month_date}/{user_check["abuturent_id"]}/BotHome")
                markup.add(btn)
                markup = InlineKeyboardMarkup()
                bot.send_message(message.chat.id, f"TestNatijangizni Ko'rishingiz mumkin!", reply_markup=markup)

            else:
                bot.send_message(message.chat.id, text_start)
                # Yangi foydalanuvchi yaratish
                abuturent_id = create_user(first_name=message.from_user.first_name, tg_id=message.chat.id)
                btn = InlineKeyboardButton("🔗 Test natijani ko'rish", url=f"{BaseUrl}{abuturent_id}")
                markup.add(btn)
                markup = InlineKeyboardMarkup()
                bot.send_message(message.chat.id, f"TestNatijangizni Ko'rishingiz mumkin!", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Xato format! To‘g‘ri format: /start=user_id@test_key@month_date")
    else:
        bot.send_message(message.chat.id, "Foydalanuvchi ID kiritilmagan!")
    
    
    
    # Foydalanuvchiga inline tugma yuborish

@bot.message_handler(commands=['asosiy_url'])
def asosiy_url(message):
    global BaseUrl
    BaseUrl=message
    bot.send_message(message.chat.id, "Link muvaffaqiyatli o'zgartirildi")

bot.polling()
