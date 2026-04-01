from ingest_data import ingest_data
from db_save import save_to_db
from clean_data import clean_data
from model import train_model
from save_predictions import save_predictions
from logger import logger   # ✅ ADD THIS

def run_pipeline():

    try:
        logger.info("🚀 Pipeline started")

        df = ingest_data()
        logger.info(f"Ingested data: {len(df)} rows")

        save_to_db(df)
        logger.info("Saved raw data to PostgreSQL")

        df = clean_data(df)
        logger.info("Data cleaned")

        model, forecast, test, rmse, conf_int = train_model(df)

        if forecast is None:
            return {"results": [], "rmse": None}

        results = save_predictions(test, forecast, conf_int)

        return {
            "results": results,
            "rmse": rmse
        }
       # logger.info("Model trained")

        results = save_predictions(test, forecast)   # ✅ CAPTURE RESULTS
        logger.info("Predictions saved")

        print("✅ Pipeline completed successfully")

        return results   # 🔥 VERY IMPORTANT

    except Exception as e:
        logger.error(f"❌ Pipeline failed: {e}")
        print(f"❌ Pipeline failed: {e}")
        return []


if __name__ == "__main__":
    run_pipeline()