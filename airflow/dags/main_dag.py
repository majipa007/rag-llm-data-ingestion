from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.models import Variable
from airflow import Dataset
from pathlib import Path
from functions import scrape_data, load_json_to_faiss

url = Variable.get("url")
scrapped_data = Variable.get("scrapped_data")
vector_data = Variable.get("vector_database")
json_dataset = Dataset(str(Path(scrapped_data)))



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

    # Define a wrapper function for the PythonOperator
    def scrape_task_wrapper():
        # Call the scrape_titles function with the URL and file path
        scrape_data(url, scrapped_data)


    scrape = PythonOperator(
        task_id='scrape_task',
        python_callable=scrape_task_wrapper,
    )

    def vector_db_task_wrapper():
        load_json_to_faiss(scrapped_data, vector_data)

    vector_db = PythonOperator(
        task_id='vector_db_task',
        python_callable = vector_db_task_wrapper,
    )

    # Example of another task
    def finish_task():
        print("Finishing the DAG")

    finish = PythonOperator(
        task_id='finish_task',
        python_callable=finish_task,
    )

    # Task dependencie
    start >> scrape >> vector_db >> finish
