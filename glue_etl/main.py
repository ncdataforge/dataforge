import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

s3_raw_dataset = "s3://bank-account-opening-fraud-detection-s3-dataset/baofd-dataset/base-dataset/"

dyf_raw_base = glueContext.create_dynamic_frame_from_options(connection_type='s3',
                                                            connection_options={"paths": [s3_raw_dataset]},
                                                            format='csv',
                                                            format_options={"withHeader": True})

dyf_raw_base_col_removed = dyf_raw_base.drop_fields(paths=['month', 'zip_count_4w', 'velocity_6h', 'velocity_24h',
                                                    'velocity_4w', 'device_fraud_count', 'source',
                                                    'prev_address_months_count', 'intended_balcon_amount'], transformation_ctx='drop_column')

dyf_raw_base_col_removed.toDF().show(5)
dyf_raw_base_col_removed.printSchema()

conn_options = {
    "database": "db_fraud_detection",
    "dbtable": "public.baofd_ml-training_data",
    # "query": "CREATE TABLE IF NOT EXISTS public.baofd_ml-training_data",
}

redshift_res = glueContext.write_dynamic_frame_from_jdbc_conf(
    frame=dyf_raw_base_col_removed,
    catalog_connection="baofd-glue-redshift-connection",
    connection_options=conn_options,
    redshift_tmp_dir="s3://bank-account-opening-fraud-detection-s3-dataset/temp-data/"
)