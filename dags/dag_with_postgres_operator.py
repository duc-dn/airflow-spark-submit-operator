from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator

default_args = {
    'owner': 'ducdn',
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    default_args=default_args,
    dag_id='postgres_operator',
    start_date=datetime.now(),
    schedule_interval='@daily'
) as dag:
    task1 = PostgresOperator(
        task_id='create_postgres_table',
        postgres_conn_id='postgres_conn',
        sql="""
            create table if not exists dag_runs (
                dt date, 
                dag_id character varying,
                primary key (dt, dag_id)
            )
        """
    )

    # https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html
    task2 = PostgresOperator(
        task_id='insert_postgres_table',
        postgres_conn_id='postgres_conn',
        sql="""
            insert into dag_runs (dt, dag_id)
            values ('{{ ds }}', '{{ dag.dag_id }}')
        """
    )
    task2>>task1