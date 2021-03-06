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
    lib.validation.check_keys(required_keys, event)
    lib.validation.check_keys(['pathId'], event, False)

    # Validate
    lib.validation.string_length(event['body']['province'], 2)
    lib.validation.string_length(event['body']['icao'], 4)

    # Normalize certain fields
    for key in ['street', 'city', 'province', 'icao']:
        event['body'][key] = event['body'][key].upper()

    # Update
    try:
        response = lib.LocationsTable.update_item(
            Key={
                'id': event['pathId']
            },
            UpdateExpression="set cn = :cn, street = :st, city = :ct, province = :pv, country = :co",
            ExpressionAttributeValues={
                ':cn': event['body']['cn'],
                ':st': event['body']['street'],
                ':ct': event['body']['city'],
                ':pv': event['body']['province'],
                ':co': event['body']['country']
            },
            ReturnValues="ALL_NEW"
        )
    except lib.exceptions.ClientError as ce:
        raise lib.exceptions.InternalServerException(ce.message)

    # Return
    return lib.get_json(response['Attributes'])
