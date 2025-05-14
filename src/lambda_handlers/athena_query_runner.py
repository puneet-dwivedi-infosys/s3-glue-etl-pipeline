import json
import boto3

QUERY_OUTPUT_BUCKET_LOCATION = "s3://etl-pipeline-input-data-bucket/athena-query-result/"
AWS_DEFAULT_REGION = "ap-south-1"
GLUE_CRAWLER_DATABASE = "processed_data_db"

def run_athena_query():
    athena = boto3.client('athena', region_name=AWS_DEFAULT_REGION)
    try:
        query = """
            CREATE OR REPLACE VIEW processed_view AS 
            SELECT * FROM table_processed_data
        """

        # runing athena query
        response = athena.start_query_execution(
            QueryString=query,
            ResultConfiguration={
                'OutputLocation': QUERY_OUTPUT_BUCKET_LOCATION
            },
            QueryExecutionContext={
                'Database': GLUE_CRAWLER_DATABASE  
            },
        )
        print(f"Athena query started: {response}")
    except Exception as e:
        print(f'Error running Query {e}')


def lambda_handler(event, context):

    print(event)

    #running athena query
    run_athena_query()

    return {
            'statusCode': 200,
            'body': json.dumps('Query run successfully')
        }