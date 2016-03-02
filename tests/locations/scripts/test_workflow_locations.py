#!/usr/bin/env python

import json
import requests

LOCATION_URL = "https://uclggsi59g.execute-api.us-east-1.amazonaws.com/dev/location"

def myerror(req):
    if req.status_code != 200:
        print "Status Code: %d" % req.status_code
        print "Text: %s" % req.text
        exit(1)

# Create
def create():
    print "CREATE"
    location = {
        "cn": "TESTING",
        "street": "123 Main St",
        "city": "Boston",
        "province": "MA",
        "country": "USA",
        "icao": "ABCD"
    }

    #r_loc_create = requests.post(LOCATION_URL)
    r_loc_create = requests.post(LOCATION_URL, data=json.dumps(location))
    myerror(r_loc_create)

    return json.loads(r_loc_create.text)
# Read
def read(id_):
    print "READ"
    r_loc_read = requests.get("%s/%s" % (LOCATION_URL, id_))
    myerror(r_loc_read)
    return json.loads(r_loc_read.text)

# Update
def update(r_json):
    print "UPDATE"
    location = {}
    r_json['street'] = "456 Broad Way"

    r_loc_up = requests.put("%s/%s" % (LOCATION_URL, r_json['id']), data=json.dumps(r_json))
    myerror(r_loc_up)

    return json.loads(r_loc_up.text)

# Delete
def delete(id_):
    print "DELETE"
    r_loc_del = requests.delete("%s/%s" % (LOCATION_URL, id_))
    myerror(r_loc_del)
    return json.loads(r_loc_del.text)

# List


# Do!
c_json = create()
print c_json
r_json = read(c_json['id'])
print r_json
u_json = update(r_json)
print u_json
d_json = delete(u_json['id'])
print d_json
