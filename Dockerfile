FROM apache/airflow:latest

USER root

RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean


USER airflow

RUN pip install requests 
RUN pip install beautifulsoup4
RUN pip install faiss-cpu 
