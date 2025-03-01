import telebot
<<<<<<< HEAD
from telebot.types import *
from telebot import types
from utils import *
from server import ServerConnection, ServerTestBot

# Serverdan test datalariniolish va ko'rsatish uchun
server = ServerConnection()
# serverdan abtituryentlar datalarini olish va regiester qilish uchun
bot_server = ServerTestBot()
=======
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from api_functions import create_user, check_user
>>>>>>> 964b4c1c883168946fedcf99f9c4c7851c6703af

# Iqro Mind Test Boti tokeni
TOKEN = '7536980017:AAGtgsiLdVOU3nCY6dhdbVQguPqysUo4qSY'

# Botni yaratish
bot = telebot.TeleBot(TOKEN)
BaseUrl = "https://yourwebsite.com/profile/"  # Linkni o'zgartiring

text_start = """
👋 Assalomu alaykum, Iqro Mind test botiga xush kelibsiz!
Bu bot orqali siz o‘quv markazdagi offline block test natijalaringizni onlayn ko‘rishingiz mumkin.
"""

<<<<<<< HEAD
=======
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
>>>>>>> 964b4c1c883168946fedcf99f9c4c7851c6703af


# Start natijani start orqali ko'rish
@bot.message_handler(commands=['start'], func=lambda message: message.text[7:13] == 'natija')
def show_natija(message):
    try:
        # Test qismlarini o'qib olish
        key = message.text.split("u")[0][13:]
        user_id = int(message.text.split("u")[1])
        chat_id = message.chat.id
        # uni decode qilish yani month date va test keyni olish
        month_date, test_key = decode(key)

        # serverdan html formatda postni olish
        post = server.get_post_text_html(user_id, month_date, test_key)
        res = bot_server.check_user(chat_id)
        if not res["mes"]:
            # Ro'yxatdan o'tish
            print(message.chat.first_name)
            res = bot_server.register(message.chat.first_name, chat_id)
            print(res)
            if "detail" in res:
                bot.send_message(
                    message.chat.id,
                    f"Nimadur xato ketdi qayta <a href='https://t.me/IqroMindTestbot?start={message.text[7:]}'><b>start</b></a> berib ko'ring.",
                    parse_mode="html",
                    disable_web_page_preview=True,
                    reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Start berish", url=f"https://t.me/IqroMindTestbot?start={message.text[7:]}")),
                )
                return
            res["abuturent_id"] = res["user_id"]
        abt_id = res["abuturent_id"]
        markup = types.InlineKeyboardMarkup()
        # fontendga user_id query key bilan abituriyent_id ni uzatish
        markup.row(types.InlineKeyboardButton("📊 Natijalar", web_app = WebAppInfo(url=f"https://iqromind.uz/natija/{user_id}/{month_date}/{test_key}?user_id={abt_id}")))
        markup.row(types.InlineKeyboardButton("Ulashish ⤴️", switch_inline_query=f"{key}u{user_id}"))
        bot.send_message(message.chat.id, str(post), parse_mode="html", disable_web_page_preview=True, reply_markup=markup) 
    except Exception as e:
        pass
@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    try:
        text = query.query.strip()  # Foydalanuvchi kiritgan matn
        key = text.split("u")[0]
        user_id = int(text.split("u")[1])
        month_date, test_key = decode(key)
        matn = server.get_post_text_html(user_id, month_date, test_key)

        # Inline tugmalar
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("📊 Natijalar", url=f"https://t.me/IqroMindTestbot?start=natija{key}u{user_id}"))
        markup.row(types.InlineKeyboardButton("Ulashish ⤴️", switch_inline_query=text))
        # logo = server.get_edu_logo(user_id)
        # print(logo)
        result = types.InlineQueryResultArticle(
            id="1",
            title="✅ Test natijalari",
            # thumbnail_url=logo["file_url"],
            description="👉 Ko'rish uchun bosing",
            input_message_content=types.InputTextMessageContent(
                message_text=matn,
                parse_mode="html",
                disable_web_page_preview=True
            ),
            reply_markup=markup
        )

        bot.answer_inline_query(query.id, [result], cache_time=1)
    except Exception as e:
        print(e)
bot.polling()
