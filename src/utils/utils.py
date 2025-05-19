from services.dynamo_db_handler import DynamoDBClient, DynamoDBManager
from utils.constants import (
    AWS_ACCESS_KEY, AWS_DEFAULT_REGION, AWS_SECRET_KEY, 
    GLUE_JOB_CONFIGURATION_DYNAMO_DB_TABLE_NAME,
    CSV_DATA_PROCESSOR_GLUE_JOB_JOB_NAME,
    GLUE_JOBS_CONFGIGURATION
)

def seed_glue_job_configuration_in_dynamodb():
    
    # creating dynamodb client
    dynamodb_client = DynamoDBClient(access_key=AWS_ACCESS_KEY, secret_key=AWS_SECRET_KEY, region=AWS_DEFAULT_REGION)

    # creating dynaodb manager
    dynamodb_manager = DynamoDBManager(dynamodb_client.get_dynamodb_client())

    # creating glue job configuration table
    key_schema = [
        {'AttributeName': 'job_name', 'KeyType': 'HASH'}
    ]

    attribute_definitions = [
        {'AttributeName': 'job_name', 'AttributeType': 'S'}
    ]

    provisioned_throughput = {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
    dynamodb_manager.create_table(
        table_name=GLUE_JOB_CONFIGURATION_DYNAMO_DB_TABLE_NAME,
        key_schema=key_schema,
        attribute_definitions=attribute_definitions,
        provisioned_throughput=provisioned_throughput
    )

    for job in GLUE_JOBS_CONFGIGURATION:
        dynamodb_manager.insert_item(
            item=job,
            table_name=GLUE_JOB_CONFIGURATION_DYNAMO_DB_TABLE_NAME
        )
