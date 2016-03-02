#!/usr/bin/env python

import json
import requests

LOCATION_URL = "https://uclggsi59g.execute-api.us-east-1.amazonaws.com/dev/location"
ALTNAME_URL = "https://uclggsi59g.execute-api.us-east-1.amazonaws.com/dev/lookup"

data = ""
with open('locations.json', 'r') as fh:
    data = fh.read()

jsondata = json.loads(data)
for item in jsondata:
    #print "ITEM: %s" % item
    loc_r = requests.post(LOCATION_URL, data=json.dumps(item))
    if loc_r.status_code != 200:
        print loc_r.status_code
        print loc_r.text

    item_id = json.loads(loc_r.text)['id']
    altname_data = {
        'altname': item['cn'],
        'location_id': item_id
    }
    alt_r = requests.post(ALTNAME_URL, data=json.dumps(altname_data))
    if alt_r.status_code != 200:
        print alt_r.status_code
        print alt_r.text
