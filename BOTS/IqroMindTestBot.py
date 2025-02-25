import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

from api_functions import create_user

TOKEN = "7536980017:AAGtgsiLdVOU3nCY6dhdbVQguPqysUo4qSY"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = WebAppInfo(url="https://32fa-37-110-215-51.ngrok-free.app/asdasas/BotHome")  # Web App havolasi
    btn = KeyboardButton("🌐 Open WebApp", web_app=web_app)
    markup.add(btn)
    bot.send_message(message.chat.id, "Web App ni ochish uchun tugmani bosing:", reply_markup=markup)

bot.polling()
