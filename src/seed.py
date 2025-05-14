
import os
from services.s3_manager import S3Manager
from utils.constants import (
    AWS_ACCESS_KEY, AWS_DEFAULT_REGION, AWS_SECRET_KEY, 
    EXTERNAL_S3_DATA_BUCKET, 
    S3_GLUE_ATHENA_PIPELINE_CF_TEMPLATE_FILE_NAME, 
    S3_EVENT_PROCESSOR_LAMBDA_HANDLER_FILE_NAME,
    CSV_DATA_PROCESSOR_GLUE_JOB_SCRIPT_FILE_NAME,
    GLUE_EVENT_PROCESSOR_LAMBDA_HANDLER_FILE_NAME,
    ATHENA_QUERY_RUNNER_LAMBDA_HANDLER_FILE_NAME
)
from utils.utils import seed_glue_job_configuration_in_dynamodb

# deploy s3_event_processor lambda file deploy

def seed():
    s3_mgr = S3Manager(access_key = AWS_ACCESS_KEY, secret_key = AWS_SECRET_KEY, region = AWS_DEFAULT_REGION)


    # create a bucket to store the partials of the deployment
    # Creating the bucket 
    s3_mgr.create_bucket(EXTERNAL_S3_DATA_BUCKET)
    # disble public read of the bucket
    s3_mgr.disable_public_access_block(EXTERNAL_S3_DATA_BUCKET)

    # base dir

    base_dir = os.getcwd()
    # upload cloud formation template
    template_file_path = os.path.join(base_dir, "src", "partials", "cf_templates", S3_GLUE_ATHENA_PIPELINE_CF_TEMPLATE_FILE_NAME)
    s3_mgr.upload_file(template_file_path, EXTERNAL_S3_DATA_BUCKET, S3_GLUE_ATHENA_PIPELINE_CF_TEMPLATE_FILE_NAME)

    # upload s3_event_processor lambda handler function
    s3_event_processor_lambda_function_file_path = os.path.join(base_dir, "src", "partials", "lambda_scripts",S3_EVENT_PROCESSOR_LAMBDA_HANDLER_FILE_NAME)
    s3_mgr.upload_file(s3_event_processor_lambda_function_file_path, EXTERNAL_S3_DATA_BUCKET, S3_EVENT_PROCESSOR_LAMBDA_HANDLER_FILE_NAME)

    # uploading csv glue job script
    csv_data_processor_glue_job_file_path = os.path.join(base_dir, "src", "partials", "glue_job_scripts", CSV_DATA_PROCESSOR_GLUE_JOB_SCRIPT_FILE_NAME)
    s3_mgr.upload_file(csv_data_processor_glue_job_file_path, EXTERNAL_S3_DATA_BUCKET, CSV_DATA_PROCESSOR_GLUE_JOB_SCRIPT_FILE_NAME)

    # uploading glue_event processor lambda handler function
    glue_event_processor_lambda_function_file_path = os.path.join(base_dir, "src", "partials", "lambda_scripts",GLUE_EVENT_PROCESSOR_LAMBDA_HANDLER_FILE_NAME)
    s3_mgr.upload_file(glue_event_processor_lambda_function_file_path, EXTERNAL_S3_DATA_BUCKET, GLUE_EVENT_PROCESSOR_LAMBDA_HANDLER_FILE_NAME)

    # uploading athena query query lambda hanlder
    athena_query_runner_lambda_function_file_path = os.path.join(base_dir, "src", "partials", "lambda_scripts",ATHENA_QUERY_RUNNER_LAMBDA_HANDLER_FILE_NAME)
    s3_mgr.upload_file(athena_query_runner_lambda_function_file_path, EXTERNAL_S3_DATA_BUCKET, ATHENA_QUERY_RUNNER_LAMBDA_HANDLER_FILE_NAME)

    # allow public read
    s3_mgr.add_public_read_object_policy(EXTERNAL_S3_DATA_BUCKET, S3_GLUE_ATHENA_PIPELINE_CF_TEMPLATE_FILE_NAME)
    s3_mgr.add_public_read_object_policy(EXTERNAL_S3_DATA_BUCKET, S3_EVENT_PROCESSOR_LAMBDA_HANDLER_FILE_NAME)
    s3_mgr.add_public_read_object_policy(EXTERNAL_S3_DATA_BUCKET, CSV_DATA_PROCESSOR_GLUE_JOB_SCRIPT_FILE_NAME)
    s3_mgr.add_public_read_object_policy(EXTERNAL_S3_DATA_BUCKET, GLUE_EVENT_PROCESSOR_LAMBDA_HANDLER_FILE_NAME)
    s3_mgr.add_public_read_object_policy(EXTERNAL_S3_DATA_BUCKET, ATHENA_QUERY_RUNNER_LAMBDA_HANDLER_FILE_NAME)


    # writing dynamodb configuration
    print("\nWriting dynamo db configuration")
    seed_glue_job_configuration_in_dynamodb()

# code execution starts from here
seed()