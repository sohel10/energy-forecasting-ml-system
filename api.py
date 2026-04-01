from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from main_pipeline import run_pipeline

app = FastAPI()

templates = Jinja2Templates(directory="templates")
templates.env.cache = {}   # 🔥 FIX

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/predict")
def predict():
    output = run_pipeline()

    return {
        "status": "success",
        "message": "Forecast generated successfully",
        "data": output,   # ✅ just return list
        "rmse": None
    }