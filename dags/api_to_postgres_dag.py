import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from utils.api_utils import get_bearer_token, fetch_data_from_api
from utils.db_utils import insert_data_into_postgres
#from load_env import load_env_file

#load_env_file("../../.env")

# Load environment variables (ensure to set these in your .env or environment)
API_BASE_URL = os.getenv("API_BASE_URL")
API_CNPJ = os.getenv("API_CNPJ")
API_HASH = os.getenv("API_HASH")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    "api_to_postgres",
    default_args=default_args,
    description="Fetch data from API and store it in PostgreSQL",
    schedule_interval="@daily",
    catchup=False,
)

def fetch_data_task(**kwargs):
    """Fetch data from the API."""
    token = get_bearer_token(API_BASE_URL,API_CNPJ,API_HASH)
    data = fetch_data_from_api(API_BASE_URL, token)
    kwargs['ti'].xcom_push(key='fetched_data', value=data)

def store_data_task(**kwargs):
    """Store the fetched data in PostgreSQL."""
    data = kwargs['ti'].xcom_pull(task_ids='fetch_data_task', key='fetched_data')
    insert_data_into_postgres(data, POSTGRES_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)

# Define tasks
fetch_data = PythonOperator(
    task_id="fetch_data_task",
    python_callable=fetch_data_task,
    provide_context=True,
    dag=dag,
)

store_data = PythonOperator(
    task_id="store_data_task",
    python_callable=store_data_task,
    provide_context=True,
    dag=dag,
)

# Task dependencies
fetch_data >> store_data
