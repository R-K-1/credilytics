from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'Raymond Kalonji',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
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

extract_and_stage = DummyOperator(task_id='extract_and_stage',  dag=dag)
load_accounts_fact = DummyOperator(task_id='load_accounts_fact',  dag=dag)
load_delinquencies_dimension = DummyOperator(task_id='load_delinquencies_dimension',  dag=dag)
load_finances_dimension = DummyOperator(task_id='load_finances_dimension',  dag=dag)
load_demographics_dimension = DummyOperator(task_id='load_demographics_dimension',  dag=dag)
check_data_quality = DummyOperator(task_id='check_data_quality',  dag=dag)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

