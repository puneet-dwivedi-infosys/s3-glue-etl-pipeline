import boto3
import json
from boto3.dynamodb.conditions import Attr

# constants
GLUE_JOB_CONFIGURATION_DYNAMO_DB_TABLE_NAME= "glue-job-configurations"
AWS_DEFAULT_REGION = "ap-south-1"


# function to get the job configurations from the 
def get_job_name_by_format(object_format=None, object_size = 0):

    # if not format return none
    if not object_format:
        return None

    # getting boto dynamodb resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(GLUE_JOB_CONFIGURATION_DYNAMO_DB_TABLE_NAME)

    # scanning logic
    try:
        response = table.scan(
            FilterExpression=(
                Attr('format').eq(object_format) &
                Attr('upper_limit').gte(object_size) &
                Attr('lower_limit').lt(object_size)
            )
        )
        items = response.get('Items', None)
        
        if not items:
            return None

        glue_job_name = items[0].get("job_name")
        print(f"Found Glue job: {glue_job_name}")
        return glue_job_name
    
    except Exception as e:
        print(f"Error fetching job name: {e}")
        return None


def run_glue_job(job_name, arguments = {}, region=AWS_DEFAULT_REGION):
    glue_client = boto3.client('glue', region_name=region)
    try:
        response = glue_client.start_job_run(
            JobName=job_name,
            Arguments=arguments,
            
        )
        job_run_id = response['JobRunId']
        return job_run_id
    except Exception as e:
        print(f"Failed to start Glue job: {e}")
        return None
    

def lambda_handler(event, context): 

    try:
        
        record = event['Records'][0]
        # extracing the bucket and object key
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        object_size = record['s3']['object'].get('size', 0)

        # obect format
        object_foramt = object_key.split('.')[-1]

        print(bucket_name, object_key, object_foramt, object_size)

        # get the glue job name
        glue_job_name = get_job_name_by_format(object_foramt, object_size)

        print(glue_job_name)
        if not glue_job_name:
            print(f"No job configured for format {object_foramt}")
            return {"status": "No job found"}

        # filling the arguments
        glue_job_arguments = {
            '--JOB_NAME': glue_job_name,
            '--bucket_name': bucket_name,
            '--object_key': object_key
        }

        glue_job_runner_id = run_glue_job(glue_job_name, glue_job_arguments)
        if not glue_job_runner_id:
            return {"status": "failed to run the glue job"}

        # job run successfully 
        print("Glue Job Runned succesfully")


        return {
            'statusCode': 200,
            'body': json.dumps('Job run successfully')
        }
    
    except Exception as e :
        print(e)
        return {
            'statusCode': 200,
            'body': json.dumps('Something went wrong')
        }

