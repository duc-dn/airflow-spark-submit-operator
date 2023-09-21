from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'coder2j',
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

def greet(some_dict, ti):
    print('My dict: ', some_dict)

    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    my_dict = ti.xcom_pull(task_ids='get_dict', key='my_dict')

    print(my_dict)
    print(f"Hello everyone, my name is {first_name} {last_name} and my age is {age}")

def get_name(ti, first_name: str, last_name: str):
    ti.xcom_push(key='first_name', value=first_name)
    ti.xcom_push(key='last_name', value=last_name)

def get_age(ti):
    age = 22
    ti.xcom_push(key='age', value=age)

def get_dict(profile, ti):
    ti.xcom_push(key='my_dict', value=profile)

with DAG(
    default_args=default_args,
    dag_id='python_operator_dag_with_xcom1',
    start_date=datetime.now(),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id = 'greet',
        python_callable=greet,
        op_kwargs={'some_dict': {'a': 1, 'b': 2}}
    )

    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name,
        op_kwargs={"first_name": "Duc", "last_name": "Do"}
    )

    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )

    task4 = PythonOperator(
        task_id='get_dict',
        python_callable=get_dict,
        provide_context=True,
        op_kwargs={'profile': {'name': 'Do Ngoc Duc', 'age': 22, 'passed': True}}
    )

    [task2, task3, task4] >> task1