

import requests
import pandas as pd


#API_KEY = "95774e34fcabbeb236401ceed0377f6f"

#CITY = "Houston"

def ingest_data():
    import requests
    import pandas as pd

    API_KEY = "95774e34fcabbeb236401ceed0377f6f"
    CITY = "Houston"
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

    # 🔥 FIX HERE
    df["datetime"] = pd.to_datetime(df["datetime"])

    return df