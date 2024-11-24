import psycopg2
import pandas as pd
import telebot

# Telegram bot tokeni va chat_id
bot_token = '7486708710:AAFDApDU5kvV9M7bDaXjO4zd5icIgkNHH3s'
chat_id = '5139310978'  # Telegram ID

# PostgreSQL ma'lumotlar bazasiga ulanish
conn = psycopg2.connect(
    host="localhost",
    database="PROJECTSPLATFORM",  # Database nomi
    user="postgres",  # PostgreSQL foydalanuvchisi
    password="admin1957",  # Parol
    port="5432"  # Port (agar boshqa bo'lsa, uni o'zgartiring)
)

# Jadval nomlari ro'yxati
table_names = [
    'users', 'payment', 'reportsbalance', 'products',
    'school_data', 'pckundalikcom', 'mobilekundalikcom',
    'loginsdata', 'majburiyobuna', 'admins'
]

# Excel fayliga yozish
file_path = "/projects/ProjectsPlatform/exported_data_multiple_sheets.xlsx"

# ExcelWriter yordamida bir nechta varaqlarni yaratish
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    for table in table_names:
        # Har bir jadval uchun ma'lumotlarni olish
        sql_query = f"SELECT * FROM {table};"
        df = pd.read_sql_query(sql_query, conn)
        
        # Har bir jadvalni alohida varaq sifatida saqlash
        df.to_excel(writer, sheet_name=table, index=False)

# Ulanishni yopish
conn.close()

# Telegram botni yaratish
bot = telebot.TeleBot(bot_token)

# Xabar yuborish va faylni yuborish
message = "Salom! Ma'lumotlar eksport qilindi va quyidagi faylga saqlandi:"
bot.send_message(chat_id, message)
with open(file_path, 'rb') as file:
    bot.send_document(chat_id, file)

print("Ma'lumotlar Excelga eksport qilindi va Telegramga fayl yuborildi.")
