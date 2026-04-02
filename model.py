import pandas as pd
import numpy as np
import joblib
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error

MODEL_PATH = "model.pkl"


# ==============================
# TRAIN MODEL
# ==============================
def train_model(df):
    print("🚀 Starting SARIMAX model training...")

    df = df.copy()

    # 🔴 CHECK datetime
    if 'datetime' not in df.columns:
        raise ValueError("❌ 'datetime' column missing before model")

    # 🔹 Convert datetime
    df['datetime'] = pd.to_datetime(df['datetime'])

    # 🔹 Sort
    df = df.sort_values("datetime")

    # 🔥 CREATE TARGET (NO RANDOM NOISE)
    df['energy_output'] = (
        df['wind_speed'] * 0.6 +
        df['temp'] * 0.3 -
        df['humidity'] * 0.2
    )

    # 🔹 Set index
    df = df.set_index('datetime')

    # 🔹 Ensure hourly frequency
    df = df.asfreq('h').ffill().bfill()

    # 🔹 Train-test split
    train_size = int(len(df) * 0.8)
    train = df.iloc[:train_size]
    test = df.iloc[train_size:]

    if len(train) < 10:
        print("⚠️ Small dataset, model may be unstable")

    try:
        model = SARIMAX(
            train['energy_output'],
            exog=train[['temp', 'humidity', 'wind_speed']],
            order=(1, 1, 1),
            seasonal_order=(0, 0, 0, 0)
        )

        model_fit = model.fit(disp=False)

        # 🔹 Forecast
        forecast_obj = model_fit.get_forecast(
            steps=len(test),
            exog=test[['temp', 'humidity', 'wind_speed']]
        )

        forecast = forecast_obj.predicted_mean
        conf_int = forecast_obj.conf_int()

        rmse = np.sqrt(mean_squared_error(test['energy_output'], forecast))

        print(f"✅ Model trained successfully | RMSE: {rmse:.4f}")

        # 💾 SAVE MODEL
        joblib.dump(model_fit, MODEL_PATH)
        print("💾 model.pkl saved")

        return model_fit, forecast, test, rmse, conf_int

    except Exception as e:
        print(f"⚠️ Model failed: {e}")

        forecast = pd.Series(
            [train['energy_output'].mean()] * len(test),
            index=test.index
        )

        return None, forecast, test, None, None


# ==============================
# LOAD MODEL
# ==============================
def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded")
        return model
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return None


# ==============================
# PREDICT (API USE)
# ==============================
def predict(model, df):
    if model is None:
        raise ValueError("❌ Model not loaded")

    df = df.copy()

    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values("datetime")
    df = df.set_index('datetime')
    df = df.asfreq('h').ffill().bfill()

    forecast_obj = model.get_forecast(
        steps=len(df),
        exog=df[['temp', 'humidity', 'wind_speed']]
    )

    forecast = forecast_obj.predicted_mean
    conf_int = forecast_obj.conf_int()

    return forecast, conf_int


# ==============================
# MAIN EXECUTION
# ==============================
if __name__ == "__main__":

    print("📦 Loading cleaned data...")

    try:
        df = pd.read_csv("cleaned_data.csv")
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        exit()

    print("📊 Data loaded, starting training...")

    train_model(df)

    print("🎯 Training complete!")