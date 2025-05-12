
from services.cloud_formation_stack import  CloudFormationStack, CloudFormationClient
from utils.constants import (
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
    AWS_DEFAULT_REGION,
    S3_GLUE_ATHENA_PIPELINE_CF_TEMPLATE_FILE_NAME,
    S3_GLUE_ATHENA_PIPELINE_STACK_NAME,
    S3_GLUE_ATHENA_PIPELINE_CF_STACK_TEMPLATE_URL
)

def run():

    '''Creating the CloudFormation client with aws credentials '''
    cf_client = CloudFormationClient(AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_DEFAULT_REGION).get_cf_client()
    

    ''' Deploying Cloud Formation stack '''
    template_parameters = [
    ]

    cf_stack = CloudFormationStack(
        stack_name = S3_GLUE_ATHENA_PIPELINE_STACK_NAME,
        template_url = S3_GLUE_ATHENA_PIPELINE_CF_STACK_TEMPLATE_URL,
        parameters = template_parameters,
        cf_client = cf_client
    )

    cf_stack.deploy()


# code execution starts from here
run()