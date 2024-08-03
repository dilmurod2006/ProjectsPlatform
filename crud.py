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
def fetch_data(table_name: str) -> list:    
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM {table_name}''')
    data = cursor.fetchall()
    conn.close()
    return data

# get user by id
def get_user_by_id(id: int) -> dict:
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users WHERE id = %s''', (id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return None

    user_data = {
        "id": row[0],
        "full_name": row[1],
        "email": row[2],
        # Add other fields as necessary
    }
    
    return user_data

# get forregister data by id
def get_forregister_by_id(id: int) -> dict:
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM forregister WHERE id = %s''', (id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return None

    foregister_data = {
        "id": row[0],
        "tg_id": row[1],
        "phone": row[2],
    }
    
    return foregister_data

# READ data functions from databases end function

# Test fetching data
foregister_data = get_forregister_by_id(1)
print(foregister_data)

# DELETE data functions from databases start function

# delete user by id
def delete_user_by_id(id: int) -> str:
    user_data = get_user_by_id(id)
    
    if user_data is None:
        return "Foydalanuvchi topilmadi"
    
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM users WHERE id = %s''', (id,))
    conn.commit()
    conn.close()
    
    return f"{user_data['full_name']} foydalanuvchi o'chirildi!"

# delete forregister by id
def delete_forregister_by_id(id: int) -> str:
    foregister_data = get_forregister_by_id(id)
    
    if foregister_data is None:
        return "Ma'lumot topilmadi"

    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM forregister WHERE id = %s''', (id,))
    conn.commit()
    conn.close()
    
    return f"{foregister_data['tg_id']} va {foregister_data['phone']} o'chirildi!"

# Test deleting data
# result = delete_forregister_by_id(1)
# print(result)


# egister(5420071824, '+998912106339', 'cpEDw327Skwk4cWNrUUdcg1DVi9I0GVv')
# print(result)