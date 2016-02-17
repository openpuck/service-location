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
    response = lib.LocationsTable.update_item(
        Key={
            'id': event['id']
        },
        #UpdateExpression="set cn = :cn, street = :st, city = :ct, state = :sa, country = :co, postal = :z",
        UpdateExpression="set cn = :cn, street = :st, city = :ct, country = :co, postal = :z",
        ExpressionAttributeValues={
            ':cn': event['cn'],
            ':st': event['street'],
            ':ct': event['city'],
            #':sa': event['state'],
            ':co': event['country'],
            ':z' : event['postal']
        },
        ReturnValues="ALL_NEW"
    )
    return lib.get_json(response['Attributes'])
