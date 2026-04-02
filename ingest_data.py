from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv()

def fetch_data():

    API_KEY = os.getenv("API_KEY")
    CITY = os.getenv("CITY", "Houston")

    if not API_KEY:
        raise ValueError("❌ API_KEY not found in .env")

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    records = []

    if "list" in data:
        for item in data["list"]:
            records.append({
                "datetime": item["dt_txt"],
                "temp": item["main"]["temp"],
                "humidity": item["main"]["humidity"],
                "wind_speed": item["wind"]["speed"]
            })

    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError("❌ No data returned from API")

    df["datetime"] = pd.to_datetime(df["datetime"])

    return df