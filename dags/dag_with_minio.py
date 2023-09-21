from datetime import datetime, timedelta
from airflow import DAG
from airflow.sensors.s3_key_sensor import S3KeySensor

default_args = {
    'owner': 'ducdn',
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    default_args=default_args,
    dag_id='minio_sensor',
    start_date=datetime.now(),
    schedule_interval='@daily'
) as dag:
    task_id = S3KeySensor(
        task_id="sensor_minio_s3", 
        bucket_name="airflow",
        bucket_key='data.csv',
        aws_conn_id='minio_conn'
    )