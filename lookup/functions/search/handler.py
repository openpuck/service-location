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
    #required_keys = ['altname']

    result = {}

    try:
        # Handle any DynamoDB errors that may appear
        try:
            lib.validation.check_keys(['affiliation'], event, False)
            # Affiliation
            try:
                lib.validation.check_keys(['altname'], event, False)
                # Altname
                result = lib.LocationAltnamesTable.query(
                             IndexName='AltnameAffiliationIndex',
                             KeyConditionExpression=Key('altname').eq(event['altname'])
                                & Key('affiliation').eq(event['affiliation'])
                         )
                if result['Count'] is 0:
                    raise lib.NotFoundException("altname+affilation '%s'+'%s' not found." % (event['altname'], event['affiliation']))
            except lib.BadRequestException:
                # No Altname
                result = lib.LocationAltnamesTable.query(
                             IndexName='AffiliationIndex',
                             KeyConditionExpression=Key('affiliation').eq(event['affiliation'])
                         )
                if result['Count'] is 0:
                    raise lib.NotFoundException("affilation '%s' not found." % event['affiliation'])
        except lib.BadRequestException:
            # No affiliation
            try:
                lib.validation.check_keys(['altname'], event, False)
                # Altname
                result = lib.LocationAltnamesTable.query(
                             IndexName='AltnameIndex',
                             KeyConditionExpression=Key('altname').eq(event['altname'])
                         )
                if result['Count'] is 0:
                    raise lib.NotFoundException("altname '%s' not found." % event['altname'])
            except lib.BadRequestException:
                # No Altname
                raise lib.BadRequestException("Keys '%s'|'%s' missing." % ('altname', 'affiliation'))
    except lib.exceptions.ClientError as ce:
        raise lib.exceptions.InternalServerException(ce.message)


    return lib.get_json(result['Items'])
