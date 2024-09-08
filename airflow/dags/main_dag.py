from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.models import Variable
from pathlib import Path
from functions.scraper import scrape_data
from functions.vectorizer import load_json_to_faiss

# Define paths and URLs using Airflow Variables
url = Variable.get("url")
scrapped_data_path = Path(Variable.get("scrapped_data_folder"))
vector_data_path = Path(Variable.get("vector_database"))

# Default arguments for the DAG
default_args = {
    'owner': 'Sulav Kumar Shrestha',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'scraping_pipeline_dag',
    default_args=default_args,
    description='A DAG for web scraping, processing, and vector database management',
    schedule_interval=timedelta(days=1),  # Runs daily; adjust as needed
    start_date=days_ago(1),
    catchup=False,
) as dag:

    def start_task():
        print("Starting the DAG")

    start = PythonOperator(
        task_id='start_task',
        python_callable=start_task,
    )

    def scrape_task_wrapper():
        scrape_data(url, scrapped_data_path)

    scrape = PythonOperator(
        task_id='scrape_task',
        python_callable=scrape_task_wrapper,
    )

    def vector_db_task_wrapper():
        load_json_to_faiss(scrapped_data_path, vector_data_path)

    vector_db = PythonOperator(
        task_id='vector_db_task',
        python_callable=vector_db_task_wrapper,
    )

    def finish_task():
        print("Finishing the DAG")

    finish = PythonOperator(
        task_id='finish_task',
        python_callable=finish_task,
    )

    # Task dependencies
    start >> scrape >> vector_db >> finish
