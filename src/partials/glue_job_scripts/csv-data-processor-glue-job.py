import sys
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext


args = getResolvedOptions(sys.argv, ['JOB_NAME', 'bucket_name', 'object_key'])
file_name = args['object_key'].split("/")[-1]

input_path = f"s3://{args['bucket_name']}/{args['object_key']}"
#output_path = f"s3://{args['bucket_name']}/processed_data/{args['object_key']}"
output_path = f"s3://{args['bucket_name']}/processed_data/{file_name}"



sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


df = spark.read.format("csv").option("header", "true").load(input_path)

df.write.mode("overwrite").parquet(output_path)

job.commit()
