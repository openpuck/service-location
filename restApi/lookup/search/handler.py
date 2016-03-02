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
from boto3.dynamodb.conditions import Key, Attr

def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))

    # Test for required attributes
    required_keys = ['altname']
    lib.test_for_keys(required_keys, event, False)

    result = {}
    if 'affiliation' in event.keys():
        if len(event['affiliation']) is not 0:
            result = lib.LocationAltnamesTable.query(
                         IndexName='AltnameIndex',
                         KeyConditionExpression=Key('altname').eq(event['altname'])
                            & Key('affiliation').eq(event['affiliation'])
                     )
        else:
            result = lib.LocationAltnamesTable.query(
                         IndexName='AltnameIndex',
                         KeyConditionExpression=Key('altname').eq(event['altname'])
                     )
    else:
        result = lib.LocationAltnamesTable.query(
                     IndexName='AltnameIndex',
                     KeyConditionExpression=Key('altname').eq(event['altname'])
                 )

    if result['Count'] is 0:
        raise lib.NotFoundException("altname '%s' not found." % event['altname'])

    return lib.get_json(result['Items'])
