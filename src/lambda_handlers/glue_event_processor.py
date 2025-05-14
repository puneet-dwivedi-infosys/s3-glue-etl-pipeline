import json
import boto3


# constants
PROCESSSED_DATA_GLUE_CRAWLER_NAME = "processed-data-crawler"
AWS_DEFAULT_REGION = "ap-south-1"

def start_crawler():
	glue_client = boto3.client('glue', region_name=AWS_DEFAULT_REGION)
	try:
		response = glue_client.start_crawler(Name=PROCESSSED_DATA_GLUE_CRAWLER_NAME)
		print("Crawler run successfully")
	except Exception as e:
		print(f"Error starting the crawler {e}")


def lambda_handler(event, context):
	# starting the crawler
	start_crawler()

	return {
		'statusCode': 200,
		'body': json.dumps('Lambda Execution completed')
    }