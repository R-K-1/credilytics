from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator, Variable
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 test_queries="",
                 expected_result="",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.test_queries = test_queries
        self.expected_result = expected_result

    def execute(self, context):
        self.log.info('DataQualityOperator implemented and running')
        redshift_hook_conn = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info("Running Data Quality test")
        for test_query in self.test_queries:
            rows = redshift_hook_conn.get_records(test_query)
            if int(rows[0][0]) != self.expected_result:
                raise ValueError(f"""
                    Data quality test failed. \
                    {rows[0][0]} does not equal {self.expected_result}
                """)
            else:
                self.log.info("Data quality test passed")