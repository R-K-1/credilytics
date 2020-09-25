from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook
from pyspark.sql import SparkSession, Window

class TransformOperator(BaseOperator):
    ui_color = '#358140'
    
    copy_sql_template = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        REGION AS '{}'
        FORMAT as json '{}'
    """

    @apply_defaults
    def __init__(self,
                 s3_bucket="",
                 s3_input_key="",
                 s3_output_folder="",
                 region="",
                 aws_credentials_id="",
                 *args, **kwargs):

        super(TransformOperator, self).__init__(*args, **kwargs)
        self.s3_bucket = s3_bucket
        self.s3_input_key = s3_input_key
        self.s3_output_folder = s3_output_folder
        self.region = region
        self.aws_credentials_id = aws_credentials_id

    def execute(self, context):
        self.log.info('TransformOperator implemented and running')
        
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        
        self.log.info("Transforming input data and storing it into staging area")
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
        
        spark = SparkSession \
            .builder \
            .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
            .getOrCreate()
        
        df = spark.read.csv(s3_path)
        self.log.info(df.printSchema())






