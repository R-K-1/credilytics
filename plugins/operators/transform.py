import os
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator, Variable
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf

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
        
        os.environ['AWS_ACCESS_KEY_ID'] = Variable.get('aws_access_key_id')
        os.environ['AWS_SECRET_ACCESS_KEY']= Variable.get('aws_secret_key_id')

        spark = SparkSession \
            .builder \
            .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
            .getOrCreate()
        
        spark_context = spark.sparkContext
        hadoop_conf = spark_context._jsc.hadoopConfiguration()
        hadoop_conf.set("fs.s3a.awsAccessKeyId", Variable.get('aws_access_key_id'))
        hadoop_conf.set("fs.s3a.awsSecretAccessKey", Variable.get('aws_secret_key_id'))
        
        rendered_key = self.s3_input_key.format(**context)
        s3_path = "s3a://{}/{}".format(self.s3_bucket, rendered_key)
        self.log.info("S3 PATH IS {}".format(s3_path))
        
        df = spark.read.csv(s3_path)
        self.log.info(df.printSchema())