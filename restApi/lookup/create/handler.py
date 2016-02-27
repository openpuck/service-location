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
    required_keys = ['altname', 'affiliation']
    for key in required_keys:
        if key not in event['body'].keys():
            raise lib.BadRequestException("Key '%s' is missing." % key)
        if len(event['body'][key]) is 0:
            raise lib.BadRequestException("Key '%s' is empty." % key)

    # No special validation needed

    # Normalize certain fields
    for key in ['altname', 'affiliation']:
        event['body'][key] = event['body'][key].upper()

    # Add to database
    lib.LocationAltnamesTable.put_item(Item=event['body'])

    # Return
    return event['body']
