from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from main_pipeline import run_pipeline   # 🔥 ADD THIS

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/predict")
def predict():

    output = run_pipeline()

    return {
        "status": "success",
        "message": "Forecast generated successfully",
        "data": output["results"],
        "rmse": output["rmse"]
    }