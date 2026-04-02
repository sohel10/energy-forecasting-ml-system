# energy-forecasting-ml-system
# ⚡ Energy Forecasting ML System (Production-Ready)

## 🚀 Overview
Built an end-to-end machine learning system that ingests real-time weather data, performs feature engineering, trains a time-series model, and serves predictions via a production-ready API.

## 🧠 Key Features
- Real-time data ingestion from OpenWeather API
- Feature engineering pipeline
- SARIMAX time-series forecasting model
- Model persistence (`model.pkl`)
- FastAPI-based prediction API
- Dockerized microservices architecture
- Monitoring with Prometheus
- Visualization with Grafana
- Workflow orchestration with Airflow

---

## 🏗️ Architecture
````
energy_forecasting/
│
├── api.py
├── model.py
├── clean_data.py
├── ingest_data.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .env (NOT pushed)
├── .gitignore
│
├── templates/
│     └── index.html
│
├── dags/
│     └── ml_pipeline.py
│
├── README.md   

````

````

## ⚙️ Tech Stack
- Python (Pandas, NumPy, Statsmodels)
- FastAPI
- Docker & Docker Compose
- PostgreSQL
- Prometheus & Grafana
- Apache Airflow

````

## 🚀 How to Run

```bash
git clone <repo>
cd energy_forecasting

docker-compose up --build

API → http://localhost:8000/predict
Grafana → http://localhost:3000
Airflow → http://localhost:8080