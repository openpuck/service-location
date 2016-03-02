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
from uuid import uuid4

def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))

    # Auto-generate an ID
    event['body']['id'] = str(uuid4())

    # Test for required attributes
    required_keys = ['id', 'cn', 'street', 'city', 'province', 'icao']
    for key in required_keys:
        if key not in event['body'].keys():
            raise lib.BadRequestException("Key '%s' is missing." % key)
        if len(event['body'][key]) is 0:
            raise lib.BadRequestException("Key '%s' is empty." % key)

    # Validate
    lib.validate_string_length(event['body']['province'], 2)
    lib.validate_string_length(event['body']['icao'], 4)

    # Normalize certain fields
    for key in ['street', 'city', 'province', 'icao']:
        event['body'][key] = event['body'][key].upper()

    # Add to database
    lib.LocationsTable.put_item(Item=event['body'])

    # Return
    return event['body']
