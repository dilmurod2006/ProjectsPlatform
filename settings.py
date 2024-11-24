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


# async def get_redis():
#     global redis
#     if redis is None:
#         redis = await aioredis.create_redis_pool("redis://localhost")
#     return redis


