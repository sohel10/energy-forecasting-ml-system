from ingest_data import ingest_data
from db_save import save_to_db
from clean_data import clean_data
from model import train_model
from save_predictions import save_predictions
from logger import logger
import pandas as pd


def run_pipeline():
    try:
        logger.info("🚀 Pipeline started")

        df = ingest_data()
        print("STEP 1 - After ingest:", df.columns)

        save_to_db(df)
        
        print("STEP 1 RAW DF COLUMNS:", df.columns)
        print(df.head())

        df = clean_data(df) 
        # 🚨 FORCE datetime (FINAL FIX)
        if 'datetime' not in df.columns:
            print("⚠️ datetime missing → creating fallback datetime")

            df['datetime'] = pd.date_range(
                start="2023-01-01",
                periods=len(df),
                freq="H"
            )

        # Ensure proper type
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

        # Drop bad rows
        df = df.dropna(subset=['datetime'])

        print("✅ FINAL DF COLUMNS:", df.columns)
        
        

        model, forecast, test, rmse, conf_int = train_model(df)
        test = test.reset_index().rename(columns={"index": "datetime"})
        print("STEP 3 - Model OK")

        if forecast is None:
            return {"actual": [], "predicted": [], "rmse": None}

        results = save_predictions(test, forecast, conf_int)
        print("STEP 4 - Save predictions OK")

        return {
            "actual": results.get("actual", []),
            "predicted": results.get("predicted", []),
            "datetime": results.get("datetime", []), 
            "rmse": rmse
        }

    except Exception as e:
        logger.error(f"❌ Pipeline failed: {e}")
        print(f"❌ Pipeline failed: {e}")
        return {"actual": [], "predicted": [], "rmse": None}


if __name__ == "__main__":
    run_pipeline()