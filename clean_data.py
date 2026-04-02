import pandas as pd
import numpy as np

def clean_data(df):

    print("🔍 CLEAN INPUT COLUMNS:", df.columns)

    # 🔥 STEP 1: Ensure datetime exists
    if 'datetime' not in df.columns:

        # try to auto-detect
        found = False
        for col in df.columns:
            if 'time' in col.lower() or 'date' in col.lower():
                df.rename(columns={col: 'datetime'}, inplace=True)
                found = True
                print(f"✅ Renamed {col} → datetime")
                break

        # 🔴 If still not found → CREATE FAKE DATETIME (FAILSAFE)
        if not found:
            print("⚠️ No datetime column found → creating synthetic datetime")
            df['datetime'] = pd.date_range(
                start="2023-01-01",
                periods=len(df),
                freq="H"
            )

    # 🔹 Convert to datetime
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

    # 🔴 Drop rows where datetime failed
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