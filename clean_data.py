import pandas as pd
import numpy as np


def clean_data(df):

    print("🔍 CLEAN INPUT COLUMNS:", df.columns)

    # 🔥 STEP 1: Ensure datetime exists
    if 'datetime' not in df.columns:

        found = False
        for col in df.columns:
            if 'time' in col.lower() or 'date' in col.lower():
                df.rename(columns={col: 'datetime'}, inplace=True)
                found = True
                print(f"✅ Renamed {col} → datetime")
                break

        if not found:
            print("⚠️ No datetime column found → creating synthetic datetime")
            df['datetime'] = pd.date_range(
                start="2023-01-01",
                periods=len(df),
                freq="H"
            )

    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    df = df.dropna(subset=['datetime'])

    # 🔹 Clean numeric columns
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df = df.dropna(subset=['temp', 'humidity', 'wind_speed'])

    # 🔹 Feature engineering
    df['hour'] = df['datetime'].dt.hour
    df['dayofweek'] = df['datetime'].dt.dayofweek
    df['lag_1'] = df['wind_speed'].shift(1)

    df = df.ffill().bfill()

    print("✅ CLEAN OUTPUT COLUMNS:", df.columns)

    return df


# ==============================
# MAIN EXECUTION (THIS WAS MISSING)
# ==============================
if __name__ == "__main__":

    print("📡 Fetching data from pipeline...")

    try:
        from ingest_data import fetch_data  # adjust if function name differs
        df = fetch_data()
    except Exception as e:
        print(f"❌ Failed to fetch data: {e}")
        exit()

    print("🧹 Cleaning data...")

    df_clean = clean_data(df)

    # 🔥 SAVE FILE
    df_clean.to_csv("cleaned_data.csv", index=False)

    print("💾 cleaned_data.csv saved successfully")