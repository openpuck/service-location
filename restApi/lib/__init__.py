# shared logic goes here
import boto3
import json
import decimal
from exceptions import *

#LocationsTable = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1').Table('locations')
LocationsTable = boto3.resource('dynamodb', region_name='us-east-1').Table('locations')
LocationAltnamesTable = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1').Table('location_altnames')

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


def validate_string_length(input_string, num_chars):
    """
    Validate a territory code.
    """
    if len(input_string) > num_chars:
        raise BadRequestException("Value '%s' has too many characters (max: %d)." % (input_string, num_chars))

def test_for_keys(keys, event, body=True):
    """
    Test for the existance of the given list of keys in the event.
    """
    for key in keys:
        if body is True:
            if key not in event['body'].keys():
                raise BadRequestException("Key '%s' is missing." % key)
            if len(event['body'][key]) is 0:
                raise BadRequestException("Key '%s' is empty." % key)
        else:
            if key not in event.keys():
                raise BadRequestException("Key '%s' is missing." % key)
            if len(event[key]) is 0:
                raise BadRequestException("Key '%s' is empty." % key)
