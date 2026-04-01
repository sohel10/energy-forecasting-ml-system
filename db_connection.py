import time
import psycopg2
import os

def get_connection():
    for i in range(10):
        try:
            conn = psycopg2.connect(
                host="db",
                database="weather_db",
                user="postgres",
                password=os.getenv("DB_PASSWORD")
            )
            print("✅ Connected to DB")
            return conn
        except Exception as e:
            print("⏳ Waiting for DB...", e)
            time.sleep(3)

    raise Exception("❌ DB connection failed")