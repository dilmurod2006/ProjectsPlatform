"""
Projects all settings function in this file

"""

import os
from dotenv import load_dotenv

load_dotenv()

# SECRET_KEY for project
SECRET_KEY=os.environ.get('SECRET_KEY')

# ALGORITHM
ALGORITHM=os.environ.get('ALGORITHM')

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

