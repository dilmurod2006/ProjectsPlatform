"""
CREATE, READ, UPDATE, DELETE functions in database
add full CRUD data comments...
"""

import psycopg2 as pg
from settings import DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_PASSWORD

# database connection function
def database_connection():
    try:
        conn = pg.connect(
            host=DB_HOST,
            database=DB_NAME,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as err:
        print("Something went wrong.")
        print(err)


# READ data functions from databases start function

# get data function
def fetch_data(table_name: str) -> tuple:    
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM {table_name}''')
    data = cursor.fetchall()
    return data

# get user by id
def get_users_by_id(id: int) -> tuple:
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM users WHERE id = {id}''')
    data = cursor.fetchall()
    return data

# get forregister data by id
def get_forregister_by_id(id: int) -> tuple:
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM forregister WHERE id = {id}''')
    data = cursor.fetchall()
    return data

# READ data functions from databases end function


# user_data = get_users_by_id(1)
# print(user_data)
foregister_data = get_forregister_by_id(1)
print(foregister_data[0][3])


# DELETE data functions from databases start function

# delete user by id
def delete_user_by_id(id: int) -> None:
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute(f'''DELETE FROM users WHERE id = {id}''')
    conn.commit()
    conn.close()
    # get user full_names
    user_data = get_users_by_id(id)
    return f"{user_data['full_name']} foydalanuvchi o'chirildi!"

# delete forregister by id
def delete_forregister_by_id(id: int) -> None:
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute(f'''DELETE FROM forregister WHERE id = {id}''')
    conn.commit()
    conn.close()
    # get forregister full_names
    foregister_data = get_forregister_by_id(id)
    return f"{foregister_data['tg_id']} va {foregister_data['phone']} o'chirildi!"

# Control functions start function
