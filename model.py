import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error


def train_model(df):

    print("Starting SARIMAX model training...")

    # 🔹 Ensure sorted time
    df = df.sort_values("datetime")

    # 🔹 Create target
    df['energy_output'] = (
        df['wind_speed'] * 0.5 +
        df['temp'] * 0.2 -
        df['humidity'] * 0.1 +
        np.random.normal(0, 0.3, len(df))
    )

    # 🔹 Set datetime index
    df.set_index('datetime', inplace=True)

    # 🔥 Interpolate instead of ffill
    df = df.asfreq('h').interpolate()

    # 🔹 Train-test split
    train_size = int(len(df) * 0.8)
    train = df.iloc[:train_size]
    test = df.iloc[train_size:]

    if len(train) < 10:
        print("⚠️ Not enough data for SARIMAX.")
        return None, None, None, None, None

    if train[['temp','humidity','wind_speed']].isnull().any().any():
        print("❌ Missing values in TRAIN exog")
        return None, None, None, None, None

    if test[['temp','humidity','wind_speed']].isnull().any().any():
        print("❌ Missing values in TEST exog")
        return None, None, None, None, None

    try:
        # ✅ Fit ONLY on train
        model = SARIMAX(
            train['energy_output'],
            exog=train[['temp','humidity','wind_speed']],
            order=(1,1,1),
            seasonal_order=(0,0,0,0)
        )

        model_fit = model.fit(disp=False)

        # 🔥 Forecast with confidence interval (ONLY ONCE)
        forecast_obj = model_fit.get_forecast(
            steps=len(test),
            exog=test[['temp','humidity','wind_speed']]
        )

        forecast = forecast_obj.predicted_mean
        conf_int = forecast_obj.conf_int()

        # RMSE
        rmse = np.sqrt(mean_squared_error(test['energy_output'], forecast))

        print(f"✅ SARIMAX Model trained. RMSE: {rmse:.4f}")

        return model_fit, forecast, test, rmse, conf_int

    except Exception as e:
        print(f"❌ Model training failed: {e}")
        return None, None, None, None, None