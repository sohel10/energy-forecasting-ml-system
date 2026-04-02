from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    "ml_pipeline",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
) as dag:

    run_pipeline = BashOperator(
        task_id="run_ml_pipeline",
        bash_command="cd /app && python main_pipeline.py"
    )
