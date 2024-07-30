import os
from dotenv import load_dotenv

load_dotenv()


DB_NAME=os.environ.get('DB_NAME')
DB_USER=os.environ.get('DB_USER')
DB_PASSWORD=os.environ.get('DB_PASSWORD')
DB_HOST=os.environ.get('DB_HOST')
DB_PORT=os.environ.get('DB_PORT')
# SECRET_KEY=os.environ.get('SECRET_KEY')
BOT_TOKEN=os.environ.get('BOT_TOKEN')

print(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, BOT_TOKEN)