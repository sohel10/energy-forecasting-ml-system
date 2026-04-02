from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from main_pipeline import run_pipeline

# 👉 ADD THIS
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# 👉 ENABLE METRICS
Instrumentator().instrument(app).expose(app)

templates = Jinja2Templates(directory="templates")
templates.env.cache = {}

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/predict")
def predict():
    output = run_pipeline()
    print("DEBUG OUTPUT:", output)

    actual = output.get("actual", [])
    predicted = output.get("predicted", [])
    datetime_vals = output.get("datetime", [])

    # 🚨 fallback if datetime missing
    if not datetime_vals:
        datetime_vals = list(range(len(actual)))

    formatted_data = [
        {
            "datetime": str(dt),
            "actual": float(a),
            "predicted": float(p),
            "lower": None,
            "upper": None
        }
        for dt, a, p in zip(datetime_vals, actual, predicted)
    ]

    return {
        "status": "success",
        "message": "Forecast generated successfully",
        "data": formatted_data,
        "rmse": float(output.get("rmse")) if output.get("rmse") else None
    }