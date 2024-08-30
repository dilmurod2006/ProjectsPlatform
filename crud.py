# crud.py
import psycopg2 as pg
from settings import (
    DB_HOST,
    DB_NAME,
    DB_PORT,
    DB_USER,
    DB_PASSWORD
)


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


def fetch_data_from_table(table_name):
    with create_database_connection() as connection:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            data = cursor.fetchall()
    return data


def get_user_by_id(user_id):
    with create_database_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
    if not row:
        return None

    user_data = {
        "id": row[0],
        "full_name": row[1],
        "email": row[2],
    }
    return user_data


def get_forregister_by_id(forregister_id):
    with create_database_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT * FROM forregister WHERE id = %s"
            cursor.execute(query, (forregister_id,))
            row = cursor.fetchone()
    if not row:
        return None

    forregister_data = {
        "id": row[0],
        "tg_id": row[1],
        "phone": row[2],
        "token": row[3],
    }
    return forregister_data

def delete_user_by_id(user_id):
    user_data = get_user_by_id(user_id)
    if not user_data:
        return "User not found"

    with create_database_connection() as connection:
        with connection.cursor() as cursor:
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            connection.commit()

    return f"{user_data['full_name']} user deleted!"


def delete_forregister_by_id(forregister_id):
    forregister_data = get_forregister_by_id(forregister_id)
    if not forregister_data:
        return "Data not found"

    with create_database_connection() as connection:
        with connection.cursor() as cursor:
            query = "DELETE FROM forregister WHERE id = %s"
            cursor.execute(query, (forregister_id,))
            connection.commit()

    return f"{forregister_data['tg_id']} and {forregister_data['phone']} deleted!"