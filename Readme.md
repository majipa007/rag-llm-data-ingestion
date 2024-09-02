# Automated Web Scraping and Data Ingestion for RAG LLM Model

This project automates the process of web scraping, data processing, and vector database management using Apache Airflow. The scraped data is used to create a vector database that feeds a Retrieval-Augmented Generation (RAG) Large Language Model (LLM), enabling it to use the most recent data for contextual responses.

## Project Overview

The project involves the following key steps:

1. **Web Scraping**: Data is scraped from a college website using Scrapy.
2. **Data Change Detection**: The newly scraped data is compared with previous versions to detect any changes.
3. **Vectorization**: If changes are detected, the data is vectorized and stored in a vector database.
4. **Vector Database Management**: The vector database is updated and made available for the LLM to use as context.
5. **Airflow Automation**: The entire workflow is managed and scheduled using Apache Airflow.

## Project Structure
```bash
├── dags/
│   └── web_scraping_pipeline.py       # Airflow DAG for the entire workflow
├── scrapy_project/
│   ├── spiders/
│   │   └── college_spider.py          # Scrapy spider to scrape the college website
│   └── scrapy.cfg                     # Scrapy configuration file
├── vector_db/
│   └── vector_database.faiss          # Vector database file
├── scripts/
│   ├── detect_changes.py              # Script to detect changes in scraped data
│   ├── vectorize_data.py              # Script to vectorize data and update the vector database
│   └── make_vector_db_available.py    # Script to make the vector database available to the LLM
└── README.md                          # Project documentation
```
## Prerequisites

Ensure you have the following installed:

- Python 3.7+
- Apache Airflow
- Scrapy
- `faiss` for vector database management
- `sentence-transformers` for text vectorization
- Other dependencies listed in `requirements.txt`

## Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/automated-web-scraping-RAG-LLM.git
    cd automated-web-scraping-RAG-LLM
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Airflow**:
    - Set up Airflow by initializing the database and starting the web server:
    ```bash
    airflow db init
    airflow webserver --port 8080
    airflow scheduler
    ```
    - Place the `web_scraping_pipeline.py` file in the `dags/` directory.

4. **Configure Scrapy**:
    - Navigate to the `scrapy_project/` directory and configure your spider in `spiders/college_spider.py`.
    - Run the spider manually to test the scraping process:
    ```bash
    cd scrapy_project
    scrapy crawl college_spider
    ```

5. **Run the Pipeline**:
    - Trigger the DAG from the Airflow UI or let it run based on the schedule interval.

6. **Monitor and Manage**:
    - Use Airflow's UI to monitor the execution, logs, and status of each task in the pipeline.

## Workflow Details

1. **Web Scraping**:
    - Scrapy spider scrapes data from the specified college website and saves it in a structured format (e.g., JSON, CSV).
  
2. **Data Change Detection**:
    - The `detect_changes.py` script compares the newly scraped data with the previous data to detect any updates.
  
3. **Vectorization**:
    - If changes are detected, the `vectorize_data.py` script converts the new data into vector embeddings using a pre-trained model (e.g., BERT, Sentence-Transformers).
  
4. **Vector Database Management**:
    - The vector embeddings are stored in a FAISS-based vector database. The `make_vector_db_available.py` script ensures the vector database is accessible to the LLM.

5. **Airflow DAG**:
    - The Airflow DAG `web_scraping_pipeline.py` orchestrates the entire process, ensuring that each step is executed in the correct order.

