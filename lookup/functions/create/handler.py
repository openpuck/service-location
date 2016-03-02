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
    required_keys = ['altname']
    lib.test_for_keys(required_keys, event)

    # Make sure the relation ids exists
    location_id = event['body']['location_id']
    response = lib.LocationsTable.get_item(Key={'id': location_id})
    if 'Item' not in response.keys():
        raise lib.NotFoundException("Location '%s' not found." % location_id)
    # @TODO: Teams when they exist

    # Normalize certain fields
    for key in ['altname']:
        event['body'][key] = event['body'][key].upper()

    # Add to database
    lib.LocationAltnamesTable.put_item(Item=event['body'])

    # Return
    return event['body']
