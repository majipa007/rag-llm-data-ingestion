from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from datetime import datetime, timedelta
import os
# importing my functions
from scraper.scrapper import extract_medium_text
from scripts.file_comparision import has_file_changed
from scripts.vectorize_data import vectorize_and_save

# setting file paths
url = Variable.get("url")
scrapped_data_path = "/opt/airflow/Scrapped_data/data.txt"
vector_database_path = "/opt/airflow/vector_db/vector_database.faiss"
hash_storage_path  = "/opt/airflow/Scrapped_data/last_file_hash.txt"

# Default arguments for the DAG
default_args = {
    'owner': 'Sulav Kumar Shrestha',
    'start_date' : days_ago(1),
    'end_date' : datetime(2024, 11, 30),
    'depends_on_past': False,
    'execution_timeout' : timedelta(hours=2),
    'email_on_failure': True,
    'email_on_retry': True,
    'email' : ['sulavstha007@gmail.com', '22ad057@kpriet.ac.in'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
# functions
def run_scraper():
    extract_medium_text(url, scrapped_data_path)

def check_file_change():
    if has_file_changed(scrapped_data_path, hash_storage_path):
        return "vectorization_task"
    else:
        return "no_changes_flag"

def run_vectorization():
    vectorize_and_save(scrapped_data_path, vector_database_path)

def start_task():
    print("Starting the DAG")

def completed_flag():
    print("Successfully Completed")


# Define the DAG
with DAG(
    'hourly_scraping_pipeline',
    default_args=default_args,
    description='A DAG for web scraping, processing, and vector database management',
    schedule_interval='@hourly', # or we can use timedelta(days=1) for one day.
    catchup=False,
) as dag:

    start = DummyOperator(task_id='start_task')

    scrape = PythonOperator(
        task_id='scrape_task',
        python_callable=run_scraper,
    )

    branch = BranchPythonOperator(
        task_id = 'branch_task',
        python_callable=check_file_change,
    )

    vectorize = PythonOperator(
        task_id='vectorization_task',
        python_callable = run_vectorization,
    )

    completion_flag = DummyOperator(task_id='completion_flag')
    no_changes_flag = DummyOperator(task_id='no_changes_flag')

    # Task dependencie
    start >> scrape >> branch
    branch >> vectorize >> completion_flag
    branch >> no_changes_flag
