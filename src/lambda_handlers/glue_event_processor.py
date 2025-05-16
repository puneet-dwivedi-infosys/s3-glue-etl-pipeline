import json
import boto3


# constants
PROCESSSED_DATA_GLUE_CRAWLER_NAME = "processed-data-crawler"
AWS_DEFAULT_REGION = "ap-south-1"
AWS_ACCOUNT_ID = "637607366496"
GLUE_JOB_FAILURE_ALERT_SNS_TOPIC_NAME = "glue-job-failure-sns-alert"

def start_crawler():
	glue_client = boto3.client('glue', region_name=AWS_DEFAULT_REGION)
	try:
		response = glue_client.start_crawler(Name=PROCESSSED_DATA_GLUE_CRAWLER_NAME)
		print("Crawler run successfully")
	except Exception as e:
		print(f"Error starting the crawler {e}")



# alert the glue job failure
def alert_glue_job_failure():
	sns_client = boto3.client('sns', region_name=AWS_DEFAULT_REGION)
	try:
		message = "Glue job for the new upload is failed."
		response = sns_client.publish(
            TopicArn=f"arn:aws:sns:{AWS_DEFAULT_REGION}:{AWS_ACCOUNT_ID}:{GLUE_JOB_FAILURE_ALERT_SNS_TOPIC_NAME}", # change it
            Message=json.dumps(message)
        )

		print('Alert message sent successfully')
	except Exception as e:
		print(f'Error Publishing Alert message')


def lambda_handler(event, context):
	print(event)

	job_state = event['detail']['state']
	print(job_state)
	
	if job_state == 'SUCCEEDED':
		# starting the crawler
		start_crawler()
	else:
		alert_glue_job_failure()

	return {
		'statusCode': 200,
		'body': json.dumps('Lambda Execution completed')
    }