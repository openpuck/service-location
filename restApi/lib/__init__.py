# shared logic goes here
import boto3
import json
import decimal
from uuid import uuid4
from exceptions import BadRequestException

LocationsTable = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1').Table('locations')
#LocationsTable = boto3.resource('dynamodb', region_name='us-east-1').Table('locations')

def make_uuid():
    """
    Return a string of a randomly generated UUID.
    """
    return str(uuid4())

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def get_json(response):
    """
    Return a JSON object with actual number types.
    """
    return json.loads(json.dumps(response, cls=DecimalEncoder))

