import os
from dotenv import load_dotenv

# loading env variables
load_dotenv()


# env variables
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")


# static constants
EXTERNAL_S3_DATA_BUCKET = "project-partials-1745563858254"

S3_GLUE_ATHENA_PIPELINE_CF_TEMPLATE_FILE_NAME = "s3-glue-athena-pipeline.yaml"

S3_EVENT_PROCESSOR_LAMBDA_HANDLER_FILE_NAME = "s3_event_processor.zip"

S3_GLUE_ATHENA_PIPELINE_STACK_NAME = "s3-glue-athena-pipeline-stack"

S3_GLUE_ATHENA_PIPELINE_CF_STACK_TEMPLATE_URL = f"https://{EXTERNAL_S3_DATA_BUCKET}.s3.{AWS_DEFAULT_REGION}.amazonaws.com/{S3_GLUE_ATHENA_PIPELINE_CF_TEMPLATE_FILE_NAME}"

CSV_DATA_PROCESSOR_GLUE_JOB_JOB_NAME = "csv-data-processor-glue-job"

CSV_DATA_PROCESSOR_GLUE_JOB_SCRIPT_FILE_NAME = f"{CSV_DATA_PROCESSOR_GLUE_JOB_JOB_NAME}.py"

GLUE_JOB_CONFIGURATION_DYNAMO_DB_TABLE_NAME= "glue-job-configurations"

GLUE_EVENT_PROCESSOR_LAMBDA_HANDLER_FILE_NAME = "glue_event_processor.zip"

PROCESSSED_DATA_GLUE_CRAWLER_NAME = "processed-data-crawler"

ATHENA_QUERY_RUNNER_LAMBDA_HANDLER_FILE_NAME = "athena_query_runner.zip"