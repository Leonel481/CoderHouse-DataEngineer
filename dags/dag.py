from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from api_connect import *
from airflow.hooks.base import BaseHook
from airflow.models import XCom
import os

import smtplib
from email import message

apikey = os.getenv("apikey")
username = os.getenv("username")
password = os.getenv("password")


# Configuracion de envio de correo en caso el dag falle en ejecutarse
# Configuracion de los parametros y el correo de destino. 
# las credenciales para que utilice airflow como correo de remitente se configuro en airflow.cfg

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 5),
    'email': ['leonel.aliaga.v@gmail.com'],  # Dirección de correo electrónico de destino
    'email_on_failure': True,  # Envía correo electrónico en caso de fallo
    'email_on_retry': False,
    # 'task_instance_trigger_send_email': True, # Enviar todo el log al correo electronico
    }

ETL_dag =  DAG(
    default_args = default_args,
    dag_id = 'dag_ETL',
    catchup = False,
    description = 'ETL API acciones de bolsa',
    schedule_interval = '0 * * * *'
)


task_1 = BashOperator(
    task_id='primera_tarea',
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
