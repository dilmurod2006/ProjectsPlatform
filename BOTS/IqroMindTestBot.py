import telebot
from telebot.types import *
from telebot import types
from utils import *
from server import ServerConnection, ServerTestBot

# Serverdan test datalariniolish va ko'rsatish uchun
server = ServerConnection()
# serverdan abtituryentlar datalarini olish va regiester qilish uchun
bot_server = ServerTestBot()

# Iqro Mind Test Boti tokeni
TOKEN = '7536980017:AAGtgsiLdVOU3nCY6dhdbVQguPqysUo4qSY'

# Botni yaratish
bot = telebot.TeleBot(TOKEN)



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
        markup.row(types.InlineKeyboardButton("📊 Natijalar", web_app = WebAppInfo(url=f"https://iqromind.uz/BotHome/natija/{user_id}/{month_date}/{test_key}?abt_idcha={abt_id}")))
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
