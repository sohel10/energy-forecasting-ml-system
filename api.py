from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from model import load_model, predict as model_predict
from ingest_data import fetch_data
from clean_data import clean_data

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# ✅ Load model ONCE
model = load_model()

# ✅ Metrics
Instrumentator().instrument(app).expose(app)

templates = Jinja2Templates(directory="templates")
templates.env.cache = {}


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/predict")
def predict_api():

    print("📡 Fetching data...")
    df = fetch_data()

    print("🧹 Cleaning data...")
    df = clean_data(df)

    print("🤖 Predicting...")
    forecast, conf_int = model_predict(model, df)

    datetime_vals = df["datetime"].tolist()

    formatted_data = []

    for i, dt in enumerate(datetime_vals):
        formatted_data.append({
            "datetime": str(dt),
            "actual": None,
            "predicted": float(forecast.iloc[i]),
            "lower": float(conf_int.iloc[i, 0]) if conf_int is not None else None,
            "upper": float(conf_int.iloc[i, 1]) if conf_int is not None else None
        })

    return {
        "status": "success",
        "message": "Forecast generated successfully",
        "data": formatted_data,
        "rmse": None
    }