from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (PostgresOperator)
from airflow.models import Variable
from operators import (StageToRedshiftOperator, TransformOperator, LoadOperator,
                      DataQualityOperator)
from helpers import SqlQueries

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

transform_data = TransformOperator(
    task_id='transform_data',
    s3_bucket='credilytics',
    s3_input_key='input/credit_data.csv',
    s3_staging_folder='staging',
    region='us-west-2',
    aws_credentials_id='aws_credentials',
    dag=dag
)

create_tables = PostgresOperator(
    task_id="create_tables",
    postgres_conn_id="redshift",
    sql= SqlQueries.create_tables,
    dag=dag
)

load_into_stage_table = StageToRedshiftOperator(
    task_id='load_into_stage_table',
    table='stage',
    s3_bucket='credilytics',
    s3_key='staging/stage_table.parquet',
    region='us-west-2',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    dag=dag
)

load_borrowers_fact_table = LoadOperator(
    task_id='load_borrowers_fact_table',
    table='borrowers',
    select_sql=SqlQueries.borrowers_table_insert,
    redshift_conn_id='redshift',
    dag=dag
)

load_demographics_dim_table = LoadOperator(
    task_id='load_demographics_dim_table',
    table='demographics',
    select_sql=SqlQueries.demographics_table_insert,
    redshift_conn_id='redshift',
    dag=dag
)

load_finances_dim_table = LoadOperator(
    task_id='load_finances_dim_table',
    table='finances',
    select_sql=SqlQueries.finances_table_insert,
    redshift_conn_id='redshift',
    dag=dag
)

load_delinquencies_dim_table = LoadOperator(
    task_id='load_delinquencies_dim_table',
    table='delinquencies',
    select_sql=SqlQueries.delinquencies_tables_insert,
    redshift_conn_id='redshift',
    dag=dag
)

check_data_quality = DataQualityOperator(
    task_id='check_data_quality',
    redshift_conn_id='redshift',
    test_queries=SqlQueries.data_quality_check_queries,
    expected_result=int(Variable.get("number_of_rows")),
    dag=dag
)

end_operator = DummyOperator(task_id='stop_execution',  dag=dag)

start_operator >> transform_data
transform_data >> create_tables
create_tables >> load_into_stage_table
load_into_stage_table >> load_borrowers_fact_table >> check_data_quality
load_into_stage_table >> load_demographics_dim_table >> check_data_quality
load_into_stage_table >> load_finances_dim_table >> check_data_quality
load_into_stage_table >> load_delinquencies_dim_table >> check_data_quality
check_data_quality >> end_operator
