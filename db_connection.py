import time
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def get_connection(max_retries=10, delay=3):
    """
    Create a PostgreSQL connection with retry logic.
    Works for both local and Docker environments.
    """

    host = os.getenv("DB_HOST", "db")          # Docker default = db
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME", "weather_db")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", os.getenv("POSTGRES_PASSWORD"))

    if not password:
        raise ValueError("❌ DB_PASSWORD is not set in environment variables")

    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            print(f"✅ Connected to DB at {host}:{port}")
            return conn

        except Exception as e:
            print(f"⏳ Attempt {attempt+1}/{max_retries} - Waiting for DB... {e}")
            time.sleep(delay)

    raise Exception("❌ DB connection failed after multiple retries")