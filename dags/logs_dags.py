from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from logs_jobs import first_function, last_function,  load_logs


with DAG(
    dag_id="s3_logs_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="*/10 * * * *",  # toutes les 10 minutes
    catchup=False,
    max_active_runs=1,
    tags=["s3", "logs"],
) as dag:

    first_task = PythonOperator(
        task_id='first_task',
        python_callable=first_function,
    )

    t_transform = PythonOperator(
        task_id="transform_logs",
        python_callable=load_logs,
    )

    last_task = PythonOperator(
        task_id='last_task',
        python_callable=last_function,
    )

    # Dépendances (pipeline)
    first_task >> t_transform >> last_task
