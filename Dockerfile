FROM python:3.9-slim

# Set up working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Entry point
CMD ["airflow", "webserver"]
