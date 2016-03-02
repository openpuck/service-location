from __future__ import print_function

import json
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

# this adds the component-level `lib` directory to the Python import path
import sys, os
# get this file's directory independent of where it's run from
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../"))
sys.path.append(os.path.join(here, "../../vendored"))

# import the shared library, now anything in component/lib/__init__.py can be
# referenced as `lib.something`
import lib

def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))

    # Test for required attributes
    required_keys = ['cn', 'street', 'city', 'province', 'icao']
    for key in required_keys:
        if key not in event['body'].keys():
            raise lib.BadRequestException("Key '%s' is missing." % key)
        if len(event['body'][key]) is 0:
            raise lib.BadRequestException("Key '%s' is empty." % key)
    if 'pathId' not in event.keys():
        raise lib.BadRequestException("Key '%s' is missing." % key)

    # Validate
    lib.validate_string_length(event['body']['province'], 2)
    lib.validate_string_length(event['body']['icao'], 4)

    # Normalize certain fields
    for key in ['street', 'city', 'province', 'icao']:
        event['body'][key] = event['body'][key].upper()

    # Update
    response = lib.LocationsTable.update_item(
        Key={
            'id': event['pathId']
        },
        UpdateExpression="set cn = :cn, street = :st, city = :ct, province = :pv, country = :co, postal = :z",
        ExpressionAttributeValues={
            ':cn': event['body']['cn'],
            ':st': event['body']['street'],
            ':ct': event['body']['city'],
            ':pv': event['body']['province'],
            ':co': event['body']['country'],
            ':z' : event['body']['postal']
        },
        ReturnValues="ALL_NEW"
    )

    # Return
    return lib.get_json(response['Attributes'])
