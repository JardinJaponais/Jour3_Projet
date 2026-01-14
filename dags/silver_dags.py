from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


with DAG(
    dag_id="bronze_to_silver_logs",
    start_date=datetime(2025, 1, 1),
    schedule="*/10 * * * *",  # toutes les 10 minutes
    catchup=False,
    max_active_runs=1,
    tags=["bronze", "silver", "logs"],
) as dag:
    PythonOperator(
        task_id="bronze_to_silver",
        python_callable=lambda: bronze_to_silver(),
    ) 