import psycopg2
from settings import DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_PASSWORD

def check_postgres_connection():
    try:
        # PostgreSQL ma'lumotlar bazasiga ulanish
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.close()
        print("Ulanish muvaffaqiyatli")
    except psycopg2.Error as e:
        print(f"Ulanish muvaffaqiyatsiz: {e}")

# Dasturni ishga tushirish
check_postgres_connection()
