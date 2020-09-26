from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from operators import (TransformOperator)

default_args = {
    'owner': 'Raymond Kalonji',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
    'catchup': False,
    'email_on_retry': False
}

dag = DAG('credilytics',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow and PySpark',
          schedule_interval=None,
          max_active_runs=1
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

create_tables = DummyOperator(task_id='create_tables',  dag=dag)
transform_data = TransformOperator(
    task_id='transform_data',
    s3_bucket='credilitycs',
    s3_input_key='input/credit_data.csv',
    s3_output_folder='output',
    region='us-west-2',
    aws_credentials_id='aws_credentials',
    dag=dag
)
load_accounts_fact = DummyOperator(task_id='load_accounts_fact',  dag=dag)
load_delinquencies_dimension = DummyOperator(task_id='load_delinquencies_dimension',  dag=dag)
load_finances_dimension = DummyOperator(task_id='load_finances_dimension',  dag=dag)
load_demographics_dimension = DummyOperator(task_id='load_demographics_dimension',  dag=dag)
check_data_quality = DummyOperator(task_id='check_data_quality',  dag=dag)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> create_tables
create_tables >> transform_data
transform_data >> load_accounts_fact
load_accounts_fact >> load_delinquencies_dimension >> check_data_quality
load_accounts_fact >> load_finances_dimension >> check_data_quality
load_accounts_fact >> load_demographics_dimension >> check_data_quality
check_data_quality >> end_operator
