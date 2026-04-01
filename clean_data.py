import pandas as pd
import numpy as np

def clean_data(df):

    df['datetime'] = pd.to_datetime(df['datetime'])

    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    df = df.dropna(subset=['temp', 'humidity', 'wind_speed'])

    df['hour'] = df['datetime'].dt.hour
    df['dayofweek'] = df['datetime'].dt.dayofweek

    df['lag_1'] = df['wind_speed'].shift(1)

    df = df.fillna(method='ffill')   # ✅ FIX

    return df