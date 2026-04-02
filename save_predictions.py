import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "weather_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD")
    )


def save_predictions(test, forecast, conf_int):
      # 🔴 DEBUG HERE (inside function)
    print("TEST COLUMNS:", test.columns)
    print("TEST HEAD:", test.head())


    # 🔴 SAFETY CHECK
    if forecast is None or test is None:
        print("❌ No predictions to save")
        return {"actual": [], "predicted": []}

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        datetime TIMESTAMP,
        actual FLOAT,
        predicted FLOAT,
        lower_ci FLOAT,
        upper_ci FLOAT
    )
    """)

    results = []

    for i in range(len(forecast)):
        if "datetime" in test.columns:
            dt = test["datetime"].iloc[i]
        else:
            dt = test.index[i]
        actual = float(test['energy_output'].iloc[i])
        pred = float(forecast.iloc[i])

        # Handle CI safely
        if conf_int is not None:
            lower = float(conf_int.iloc[i, 0])
            upper = float(conf_int.iloc[i, 1])
        else:
            lower = None
            upper = None

        cursor.execute("""
        INSERT INTO predictions (datetime, actual, predicted, lower_ci, upper_ci)
        VALUES (%s, %s, %s, %s, %s)
        """, (dt, actual, pred, lower, upper))

        results.append({
            "datetime": str(dt),
            "actual": actual,
            "predicted": pred,
            "lower": lower,
            "upper": upper
        })

    conn.commit()
    conn.close()

    return {
        "actual": [r["actual"] for r in results],
        "predicted": [r["predicted"] for r in results],
        "datetime": [r["datetime"] for r in results]
    }

