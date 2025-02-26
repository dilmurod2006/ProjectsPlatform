import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from api_functions import create_user, check_user

TOKEN = "7536980017:AAGtgsiLdVOU3nCY6dhdbVQguPqysUo4qSY"
bot = telebot.TeleBot(TOKEN)
BaseUrl = "https://yourwebsite.com/profile/"  # Linkni o'zgartiring

text_start = """
👋 Assalomu alaykum, Iqro Mind test botiga xush kelibsiz!
Bu bot orqali siz o‘quv markazdagi offline block test natijalaringizni onlayn ko‘rishingiz mumkin.
"""

@bot.message_handler(commands=['start'])
def start(message):
    text = message.text  

    if text.startswith("/start=24@"):  # Havola orqali kelgan xabarni tekshiramiz
        data = text.replace("/start=", "")  # "/start=" ni olib tashlaymiz
        parts = data.split("@")  # ["24", "52123", "202502"]

        if len(parts) == 3:
            user_id, test_key, month_date = parts

            # Foydalanuvchi mavjudligini tekshiramiz
            user_check = check_user(message.chat.id)
            
            markup = InlineKeyboardMarkup()  # InlineKeyboardMarkup obyektini yaratamiz

            if user_check["mes"] == True:
                btn = InlineKeyboardButton(
                    "🔗 Test natijani ko'rish", 
                    url=f"{BaseUrl}{user_id}/{test_key}/{month_date}/{user_check['abuturent_id']}/BotHome"
                )
                markup.add(btn)
                bot.send_message(message.chat.id, "Test natijangizni ko‘rishingiz mumkin!", reply_markup=markup)

            else:
                bot.send_message(message.chat.id, text_start)
                # Yangi foydalanuvchi yaratish
                abuturent_id = create_user(first_name=message.from_user.first_name, tg_id=message.chat.id)
                btn = InlineKeyboardButton(
                    "🔗 Test natijani ko'rish", 
                    url=f"{BaseUrl}{user_id}/{test_key}/{month_date}/{abuturent_id}/BotHome"
                )
                markup.add(btn)
                bot.send_message(message.chat.id, "Test natijangizni ko‘rishingiz mumkin!", reply_markup=markup)
        
        else:
            bot.send_message(message.chat.id, "❌ Xato format! To‘g‘ri format: /start=user_id@test_key@month_date")
    else:
        bot.send_message(message.chat.id, text_start)

@bot.message_handler(commands=['asosiy_url'])
def asosiy_url(message):
    global BaseUrl
    parts = message.text.split()
    
    if len(parts) > 1:
        BaseUrl = parts[1]  # Yangi URL ni o‘rnatish
        bot.send_message(message.chat.id, f"✅ Link muvaffaqiyatli o‘zgartirildi: {BaseUrl}")
    else:
        bot.send_message(message.chat.id, "❌ Iltimos, yangi linkni qo‘shing.\nFoydalanish: `/asosiy_url https://yangi-url.com`")

bot.polling()
