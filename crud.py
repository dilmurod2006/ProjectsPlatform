# crud.py

import psycopg2 as pg
from settings import (
    DB_HOST,
    DB_NAME,
    DB_PORT,
    DB_USER,
    DB_PASSWORD
)
from admins.utils import generate_token_for_admin
from datetime import datetime
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

def create_admin():
    connection = create_database_connection()
    cursor = connection.cursor()
    # Admin ma'lumotlari
    full_name = "Amonov Dilmurod"
    phone = "+998912106339"
    email = "dilmurodamonov006@gmail.com"
    username = "Softwere_engineer006"
    password = "ProjectsPlatformAdmin@Dilmurod1945&1957"
    sex=True
    tg_id = 5420071824
    premissions = {
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
    premessions_str = json.dumps(premissions)
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
    
    cursor.execute(insert_query, (full_name, phone, email, username, password, sex, tg_id, premessions_str, token))
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return {"username": username, "password": password, "token": token}

if __name__ == "__main__":
    admin_data = create_admin()
    with open("admin_data.json", "w") as f:
        json.dump(admin_data, f)
