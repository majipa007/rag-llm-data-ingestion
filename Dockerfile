FROM apache/airflow:latest

# Switch to root user to install system dependencies
USER root

# Update package lists and install any required system-level packages
RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

# Switch back to the airflow user
USER airflow

# Install Python dependencies
RUN pip install \
    requests \
    beautifulsoup4 \
    faiss-cpu \
    scikit-learn \
    torch \
    transformers \
    numpy
