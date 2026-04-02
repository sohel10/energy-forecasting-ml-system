import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error


def train_model(df):
    np.random.seed(42)
    print("Starting SARIMAX model training...")

    df = df.copy()

    # 🔴 SAFETY CHECK
    if 'datetime' not in df.columns:
        raise ValueError("❌ 'datetime' column missing before model")

    # 🔹 Ensure datetime format
    df['datetime'] = pd.to_datetime(df['datetime'])

    # 🔹 Sort by time
    df = df.sort_values("datetime")

    # 🔹 Create target
    df['energy_output'] = (
        df['wind_speed'] * 0.5 +
        df['temp'] * 0.2 -
        df['humidity'] * 0.1 +
        np.random.normal(0, 0.3, len(df))
    )

    # 🔹 Set datetime index
    df = df.set_index('datetime')

    # 🔹 Ensure frequency + interpolate
    df = df.asfreq('h').ffill().bfill()

    # 🔹 Train-test split
    train_size = int(len(df) * 0.8)
    train = df.iloc[:train_size]
    test = df.iloc[train_size:]

    if len(train) < 5:
        print("⚠️ Small dataset, continuing anyway...")


    try:
        model = SARIMAX(
            train['energy_output'],
            exog=train[['temp','humidity','wind_speed']],
            order=(1,1,1),
            seasonal_order=(0,0,0,0)
        )

        model_fit = model.fit(disp=False)

        forecast_obj = model_fit.get_forecast(
            steps=len(test),
            exog=test[['temp','humidity','wind_speed']]
        )

        forecast = forecast_obj.predicted_mean
        conf_int = forecast_obj.conf_int()

        rmse = np.sqrt(mean_squared_error(test['energy_output'], forecast))

        print(f"✅ SARIMAX Model trained. RMSE: {rmse:.4f}")

        return model_fit, forecast, test, rmse, conf_int

    except Exception as e:
        print("⚠️ Model failed → using fallback")

        forecast = pd.Series(
        [train['energy_output'].mean()] * len(test),
        index=test.index
        )

        return None, forecast, test, None, None