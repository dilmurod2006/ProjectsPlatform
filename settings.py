"""
Projects all settings function in this file

"""
import os
from dotenv import load_dotenv
# import aioredis
load_dotenv()
# SECRET_KEY for project
SECRET_KEY=os.environ.get('SECRET_KEY')
# ALGORITHM
ALGORITHM=os.environ.get('ALGORITHM')
# API URL
API_URL=os.environ.get('API_URL')
# API DOCS URL
API_DOCS_URL=os.environ.get('API_DOCS_URL')
API_REDOC_URL=os.environ.get("API_REDOC_URL")
# DATABASE CONFUGRATION KEYS
DB_NAME=os.environ.get('DB_NAME')
DB_USER=os.environ.get('DB_USER')
DB_PASSWORD=os.environ.get('DB_PASSWORD')
DB_HOST=os.environ.get('LOCAL_HOST')
DB_PORT=os.environ.get('LOCAL_PORT')
# TELEGRAM CONFUGRATION KEYS
BOT_TOKEN=os.environ.get('BOT_TOKEN')
ADMIN_DILMUROD=os.environ.get('ADMIN_DILMUROD')
ADMIN_BEXRUZDEVELOPER=os.environ.get('ADMIN_BEXRUZDEVELOPER')
PRODUCT_ID=os.environ.get('PRODUCT_ID')
IQROMINDTEST_ID=os.environ.get('IQROMINDTEST_ID')
# ADMINS CONFUGRATIONS KEYS
SECRET_KEY_FOR_ADMINS=os.environ.get('SECRET_KEY_FOR_ADMINS')
# API FORREGISTER SECRET KEY
API_ACTIVATION_ACCOUNT_SECRET_KEY=os.environ.get('API_ACTIVATION_ACCOUNT_SECRET_KEY')
# REDIS
REDIS_HOST=os.environ.get('REDIS_HOST')
REDIS_PORT=os.environ.get('REDIS_PORT')
# create user secret key
CREATE_USER_SECRET_KEY=os.environ.get("CREATE_USER_SECRET_KEY")
# CHEACK_USER_FOR_BOT
CHEACK_USER_FOR_BOT=os.environ.get('CHEACK_USER_FOR_BOT')
IQROMIND_TEST_BOT_SECRET_KEY=os.environ.get('IQROMIND_TEST_BOT_SECRET_KEY')

MONGODB_1_USERNAME = os.environ.get('MONGODB_1_USERNAME')
MONGODB_1_PASSWORD = os.environ.get('MONGODB_1_PASSWORD')
MONGODB_1_HOST = os.environ.get('MONGODB_1_HOST')

# Iqro mind test
IQROMINDTEST_POST_TEXT = os.environ.get('IQROMINDTEST_POST_TEXT').replace("\\n", "\n")

# IqroMindTest muammolar guruhi ID si
IQROMINDTEST_MUAMMOLAR_GURUH_ID = os.environ.get('IQROMINDTEST_MUAMMOLAR_GURUH_ID')

# IqroMindTest bot token
IQROMINDTEST_BOT_TOKEN = os.environ.get('IQROMINDTEST_BOT_TOKEN')

# IqroMindTest bot username
IQROMIND_BOT_USERNAME = os.environ.get('IQROMIND_BOT_USERNAME')