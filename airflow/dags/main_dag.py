from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from airflow.models import Variable
from pathlib import Path
from airflow import Dataset
from scraper import CollegeSpider 
from scripts import load_json_to_faiss 

# Load Airflow variables
url = Variable.get("url")  
scraped_data_folder = Variable.get("scraped_data_folder")  
vector_data_path = Variable.get("vector_database")  
json_dataset = Dataset(str(Path(scraped_data_folder)))  

# Default arguments for the DAG
default_args = {
    'owner': 'Nishanthini M.',
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
    description='A DAG for web scraping and vectorization',
    schedule_interval=timedelta(days=1),  # Runs every day
    start_date=days_ago(1),
    catchup=False,
) as dag:

    #  Start task
    def start_task():
        print("Starting the scraping pipeline.")

    start = PythonOperator(
        task_id='start_task',
        python_callable=start_task,
    )

    #  Scrape data using Scrapy
    def scrape_data():
        process = CrawlerProcess(get_project_settings())  
        process.crawl(CollegeSpider, url=url)  
        process.start()  

    scrape = PythonOperator(
        task_id='scrape_task',
        python_callable=scrape_data,
    )

    # Vectorize and save data using FAISS
    def vectorize_and_save():
        load_json_to_faiss(scraped_data_folder, vector_data_path)  # Load JSON and create FAISS index

    vector_db = PythonOperator(
        task_id='vector_db_task',
        python_callable=vectorize_and_save,
    )

    #  Finish task
    def finish_task():
        print("Scraping and vectorization complete.")

    finish = PythonOperator(
        task_id='finish_task',
        python_callable=finish_task,
    )

    # Define task dependencies
    start >> scrape >> vector_db >> finish
