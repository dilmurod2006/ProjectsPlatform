import psycopg2

def check_postgres_connection():
    try:
        # PostgreSQL ma'lumotlar bazasiga ulanish
        conn = psycopg2.connect(
            host="0.tcp.eu.ngrok.io",
            port="11524",
            database="PROJECTSPLATFORM",
            user="postgres",
            password="admin1957"
        )
        conn.close()
        print("Ulanish muvaffaqiyatli")
    except psycopg2.Error as e:
        print(f"Ulanish muvaffaqiyatsiz: {e}")

# Dasturni ishga tushirish
check_postgres_connection()
