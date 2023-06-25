from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator 

default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='spark_etl_minio_v10',
    default_args=default_args,
    description='This is our fisrt dag that we write',
    start_date=datetime(2023, 6, 24),
    schedule_interval='@daily'
) as dag:
    task1 = SparkSubmitOperator(
		application = "/opt/airflow/dags/spark_etl_spark_minio.py",
		conn_id = 'spark_conn', 
		task_id ='spark_submit_task', 
        jars ='/opt/bitnami/spark/jars/hadoop-aws-3.2.0.jar,/opt/bitnami/spark/jars/aws-java-sdk-bundle-1.11.375.jar'
	)

    task1