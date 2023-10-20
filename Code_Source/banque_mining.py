from datetime import timedelta,datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.postgres_operator import PostgresOperator
from time import time,sleep


default_args = {
    'owner':'yassine',
    'retries': 5,
    'retry_delay':timedelta(minutes=2)
}

with DAG(
    dag_id = 'Bank_statistics',
    default_args=default_args,
    description='this operator try to scrap data from RABAT banks and make some data processing',
    start_date=datetime(2023,5,24,2),
    schedule_interval='@daily',
    catchup = False
) as dag:
        task1 = BashOperator(
                task_id = 'get_data',
                bash_command = "python /home/yassine/python_works/scrapBank.py"
        )
        task2 = BashOperator(
                task_id = 'process_data',
                bash_command = "python /home/yassine/python_works/processingData.py"
        )
        task3 = PostgresOperator(
                task_id = 'truncate_table',
                postgres_conn_id = 'yassine',
                sql = "DELETE FROM banques;"
        )
        task4 = BashOperator(
                task_id = 'load_data',
                bash_command = "python /home/yassine/python_works/load_data.py"
        )


        task1 >> task2 >> task3 >> task4
