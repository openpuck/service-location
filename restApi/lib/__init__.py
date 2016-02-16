# shared logic goes here
import boto3

LocationsTable = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1').Table('locations')
