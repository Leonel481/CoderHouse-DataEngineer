# First-time build can take upto 10 mins.

FROM apache/airflow:2.9.1

USER root

COPY requirements.txt .
COPY config/airflow.cfg /opt/airflow/config/

USER airflow

RUN pip install --no-cache-dir -r requirements.txt