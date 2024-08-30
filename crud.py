# crud.py

import psycopg2 as pg
from settings import (
    DB_HOST,
    DB_NAME,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    BOT_TOKEN
)
from admins.utils import generate_token_for_admin
from datetime import datetime
from requests import post
import json

def create_database_connection():
    try:
        connection = pg.connect(
            host=DB_HOST,
            database=DB_NAME,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except Exception as error:
        raise Exception("Failed to establish database connection") from error

def create_admin(full_name, phone, email, username, password, sex, tg_id, premissions):
    connection = create_database_connection()
    cursor = connection.cursor()
    
    premissions_str = json.dumps(premissions)
    data_token = {
        "username": username,
        "password": password,
        "tg_id": tg_id
    }
    token = generate_token_for_admin(data_token)
    
    insert_query = """
    INSERT INTO admins (full_name, phone, email, username, password, sex,tg_id, premessions, token)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    
    cursor.execute(insert_query, (full_name, phone, email, username, password, sex, tg_id, premissions_str, token))
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return {"username": username, "password": password, "token": token}

def send_admins_data(admin_id: int, data):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    files = {
        "document": data
    }
    data = {
        "chat_id": admin_id
    }
    response = post(url, data=data, files=files)
    return response
    

if __name__ == "__main__":
    # 1-admin uchun ma'lumotlar
    admin1_data = create_admin(
        full_name="Amonov Dilmurod",
        phone="+998912106339",
        email="dilmurodamonov006@gmail.com",
        username="Softwere_engineer006",
        password="ProjectsPlatformAdmin@Dilmurod1945&1957",
        sex=True,
        tg_id=5420071824,
        premissions={
            "permessions": {
                "admin": {
                    "create_projectsdata": "True",
                    "update_projectsdata": "True",
                    "get_projectsdata": "True",
                    "login_admin": "True",
                    "check_login_admin": "True",
                    "reset_password_request_admin": "True",
                    "reset_password_admin": "True",
                    "add_admin": "True",
                    "update_admin": "True",
                    "delete_admin": "True",
                    "add_products": "True",
                    "update_products": "True",
                    "delete_products": "True",
                    "add_payment": "True",
                    "get_forregister_data": "True",
                    "get_users_data": "True",
                    "get_reportsbalance_data": "True",
                    "get_payment_data": "True",
                    "get_products_data": "True",
                    "get_school_data": "True",
                    "get_pckundalikcom_data": "True",
                    "get_mobilekundalikcom_data": "True",
                    "get_majburiyobuna_data": "True",
                    "get_admins_data": "True",
                    "get_all_telegram_ids_data": "True",
                    "get_all_phone_numbers_data": "True",
                    "update_users_data": "True",
                    "delete_users_data": "True"
                }
            }
        }
    )
    
    # 2-admin uchun ma'lumotlar
    admin2_data = create_admin(
        full_name="Boynazarov Bexruz",
        phone="+9989147202321",
        email="bexruzpy@gmail.com",
        username="bexruzdeveloper",
        password="abdeix1006",
        sex=True,
        tg_id=5139310978,
        premissions={
            "permessions": {
                "admin": {
                    "create_projectsdata": "True",
                    "update_projectsdata": "True",
                    "get_projectsdata": "True",
                    "login_admin": "True",
                    "check_login_admin": "True",
                    "reset_password_request_admin": "True",
                    "reset_password_admin": "True",
                    "add_admin": "True",
                    "update_admin": "True",
                    "delete_admin": "True",
                    "add_products": "True",
                    "update_products": "True",
                    "delete_products": "True",
                    "add_payment": "True",
                    "get_forregister_data": "True",
                    "get_users_data": "True",
                    "get_reportsbalance_data": "True",
                    "get_payment_data": "True",
                    "get_products_data": "True",
                    "get_school_data": "True",
                    "get_pckundalikcom_data": "True",
                    "get_mobilekundalikcom_data": "True",
                    "get_majburiyobuna_data": "True",
                    "get_admins_data": "True",
                    "get_all_telegram_ids_data": "True",
                    "get_all_phone_numbers_data": "True",
                    "update_users_data": "True",
                    "delete_users_data": "True"
                }
            }
        }
    )
    
    # Ikkala admin ma'lumotlarini saqlash
    with open("sizning_admin_malumotlaringiz.json", "w") as f:
        json.dump(admin1_data, f)
    
    with open("sizning_admin_malumotlaringiz.json", "w") as f:
        json.dump(admin2_data, f)
    
    # send data to telegram bot
    with open("sizning_admin_malumotlaringiz.json", "r") as f:
        admin1_data = json.load(f)

    send_admins_data(admin_id=5420071824, data=admin1_data)

    with open("sizning_admin_malumotlaringiz.json", "r") as f:
        admin2_data = json.load(f)

    send_admins_data(admin_id=5139310978, data=admin2_data)
