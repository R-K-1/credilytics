import os, uuid
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.base_hook import BaseHook
from airflow.models import BaseOperator, Variable
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import ( StructType, StructField, DoubleType, IntegerType)
from pyspark.sql.functions import lit

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
                 s3_staging_folder="",
                 region="",
                 aws_credentials_id="",
                 *args, **kwargs):

        super(TransformOperator, self).__init__(*args, **kwargs)
        self.s3_bucket = s3_bucket
        self.s3_input_key = s3_input_key
        self.s3_staging_folder = s3_staging_folder
        self.region = region
        self.aws_credentials_id = aws_credentials_id

    def execute(self, context):
        self.log.info('TransformOperator implemented and running')
        
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        
        self.log.info("SETTING UP SPARK")
        aws_credentials_conn = BaseHook.get_connection("aws_credentials")      
        os.environ['AWS_ACCESS_KEY_ID'] = aws_credentials_conn.login
        os.environ['AWS_SECRET_ACCESS_KEY']= aws_credentials_conn.password

        
        spark = SparkSession \
            .builder \
            .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
            .getOrCreate()

        rendered_key = self.s3_input_key.format(**context)
        s3_input_file_path = "s3a://{}/{}".format(self.s3_bucket, rendered_key)
        self.log.info("S3 PATH FOR PD IS {}".format(s3_input_file_path))
        
        credit_data_schema = StructType([
            StructField("RevolvingUtilizationOfUnsecuredLines", DoubleType(), True),
            StructField("age", IntegerType(), True),
            StructField("NumberOfTime30-59DaysPastDueNotWorse", IntegerType(), True),
            StructField("DebtRatio", DoubleType(), True),
            StructField("MonthlyIncome", IntegerType(), True),
            StructField("NumberOfOpenCreditLinesAndLoans", IntegerType(), True),
            StructField("NumberOfTimes90DaysLate", IntegerType(), True),
            StructField("NumberRealEstateLoansOrLines", IntegerType(), True),
            StructField("NumberOfTime60-89DaysPastDueNotWorse", IntegerType(), True),
            StructField("NumberOfDependents", IntegerType(), True),
        ])
        df = spark.read.json(s3_input_file_path, schema=credit_data_schema)
        df2 = df.withColumn("account_id", lit(str(uuid.uuid4())))
        self.log.info(df2.printSchema())

        s3_output_file_path = "s3a://{}/{}/stage_table.parquet".format(self.s3_bucket, self.s3_staging_folder)

        df2.write.parquet(
            s3_output_file_path,
            mode="overwrite",
        )