import os

import psycopg2

def save_to_db(df):
    conn = psycopg2.connect(
        host="localhost",
        database="weather_db",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )

    cursor = conn.cursor()

    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        datetime TIMESTAMP,
        temp FLOAT,
        humidity INT,
        wind_speed FLOAT
    )
    """)

    # Insert data
    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO weather_data (datetime, temp, humidity, wind_speed)
        VALUES (%s, %s, %s, %s)
        """, (row['datetime'], row['temp'], row['humidity'], row['wind_speed']))

    conn.commit()
    conn.close()