import boto3
from utils.constants import AWS_DEFAULT_REGION

class DynamoDBClient:
    def __init__(self, access_key, secret_key, region=AWS_DEFAULT_REGION):
        self.__session = boto3.session.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        self.dynamodb_client = self.__session.client('dynamodb')

    def get_dynamodb_client(self):
        return self.dynamodb_client


class DynamoDBManager:

        def __init__(self, dynamodb_client):
            self.dynamodb_client = dynamodb_client

        def create_table(self, table_name, key_schema, attribute_definitions, provisioned_throughput):
            try:
               
                response = self.dynamodb_client.create_table(
                    TableName=table_name,
                    KeySchema=key_schema,
                    AttributeDefinitions=attribute_definitions,
                    ProvisionedThroughput=provisioned_throughput
                )
                print(f"Table {table_name} created successfully.")
                return response
            except Exception as e:
                if "Table already exists" in str(e):
                    print(f'Table Already exists -{table_name}')
                else :
                    print(f"Error creating table {table_name}: {e}")

        def insert_item(self, table_name, item):
            try:
                response = self.dynamodb_client.put_item(
                    TableName=table_name,
                    Item=item
                )
                print(f"Item inserted into {table_name} successfully.")
                return response
            except Exception as e:
                print(f"Error inserting item into table {table_name}: {e}")