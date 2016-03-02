#!/usr/bin/env python

import json
import requests

LOCATION_URL = "https://uclggsi59g.execute-api.us-east-1.amazonaws.com/dev/location"
ALTNAME_URL = "https://uclggsi59g.execute-api.us-east-1.amazonaws.com/dev/lookup"


r_locations = requests.get(LOCATION_URL)
locations = json.loads(r_locations.text)

for item in locations:
    altname_data = {
        'altname': item['cn'],
        'location_id': item['id']
    }
    
    print altname_data
    alt_r = requests.post(ALTNAME_URL, data=json.dumps(altname_data))
    if alt_r.status_code != 200:
        print alt_r.status_code
        print alt_r.text
    else:
        print json.loads(alt_r.text)['altname']
