from airflow import DAG
import airflow
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator 

default_args = {
    'owner': 'airflow',
    'retries': 0,
    'retry_delay': timedelta(minutes=10)
}

with DAG(
    dag_id='spark_etl_minio_9',
    default_args=default_args,
    description='This is our fisrt dag that we write',
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval=None
    ) as dag:
    task1 = SparkSubmitOperator(
		application = "/opt/airflow/dags/spark_etl_spark_minio.py",
		conn_id = 'spark_conn', 
		task_id ='spark_submit_task', 
        packages='com.amazonaws:aws-java-sdk-bundle:1.11.375,org.apache.hadoop:hadoop-aws:3.2.2',
        conf={
            "spark.hadoop.fs.s3a.acces  s.key": "minioadmin",
            "spark.hadoop.fs.s3a.secret.key": "minioadmin", 
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.aws.credentials.provider":
            "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
            "spark.hadoop.fs.s3a.path.style.access": "true",
        }
        
    )

    task1