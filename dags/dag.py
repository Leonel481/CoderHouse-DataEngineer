from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from api_connect import *
from airflow.hooks.base import BaseHook
from airflow.models import XCom
import os

apikey = os.getenv("apikey")
username = os.getenv("username")
password = os.getenv("password")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 5),
    }

ETL_dag =  DAG(
    default_args = default_args,
    dag_id = 'dag_ETL',
    catchup = False,
    description = 'ETL API acciones de bolsa',
    schedule_interval = '0 * * * *'
    )

task_1 = BashOperator(task_id='primera_tarea',
    bash_command='echo Iniciando...'
)

task_2 = PythonOperator(
    task_id='transformar_data',
    python_callable=extract_transform,
    op_args=['NASDAQ', apikey],
    dag=ETL_dag,
)

task_3 = PythonOperator(
    task_id='conexion_load_redshift',
    python_callable=connect_load,
    op_args=[username, password],
    dag=ETL_dag,
)


task_1 >> task_2 >> task_3
