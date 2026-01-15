from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

DBT_PROJECT_DIR = "/opt/airflow/dbt/Jour3_Projet"  # adapte au chemin dans ton environnement
DBT_PROFILES_DIR = "/opt/airflow/dbt/Jour3_Projet"


with DAG(
    dag_id="silver_to_gold_logs",
    start_date=datetime(2025, 1, 1),
    schedule="*/10 * * * *",  # toutes les 10 minutes
    catchup=False,
    max_active_runs=1,
    tags=["silver", "gold", "logs"],
) as dag:

    dbt_run_gold_logs = BashOperator(
        task_id="dbt_run_gold_logs",
        bash_command=(
            f"cd {DBT_PROJECT_DIR} && "
            f"dbt run -s GOLD_DIM_PAGES GOLD_DIM_STATUS GOLD_FAIT_VISITE --profiles-dir {DBT_PROFILES_DIR} --target dev"
        ),
    )
