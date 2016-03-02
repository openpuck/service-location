#!/usr/bin/env python

import json
import requests

ALTNAME_URL = "https://uclggsi59g.execute-api.us-east-1.amazonaws.com/dev/lookup"
LOCATION_URL = "https://uclggsi59g.execute-api.us-east-1.amazonaws.com/dev/location"

def myerror(req):
    if req.status_code != 200:
        print "Status Code: %d" % req.status_code
        print "Text: %s" % req.text
        exit(1)

def create_location():
    """
    Create a test location to work with.
    """
    print "CREATE LOCATION"
    location = {
        "cn": "TESTING",
        "street": "123 Main St",
        "city": "Boston",
        "province": "MA",
        "country": "USA",
        "icao": "ABCD"
    }
    r_loc_create = requests.post(LOCATION_URL, data=json.dumps(location))
    myerror(r_loc_create)
    return json.loads(r_loc_create.text)


def delete_location(loc_json):
    """
    Remove the test location.
    """
    print "DELETE LOCATION"
    r_loc_del = requests.delete("%s/%s" % (LOCATION_URL, loc_json['id']))
    myerror(r_loc_del)
    return json.loads(r_loc_del.text)


def create(loc_json):
    """
    Create an altname.
    """
    print "CREATE"
    altname = {
        "location_id": loc_json['id'],
        "altname": "FOOBARLOLZ"
    }
    r_loc_create = requests.post(ALTNAME_URL, data=json.dumps(altname))
    myerror(r_loc_create)
    return json.loads(r_loc_create.text)

def delete(alt_json):
    """
    Delete an altname.
    """
    print "DELETE"
    urlparts = {'location_id': alt_json['location_id'], 'altname': alt_json['altname']}
    r_loc_delete = requests.delete(ALTNAME_URL, params=urlparts)
    myerror(r_loc_delete)
    return json.loads(r_loc_delete.text)

def list_():
    """
    List all altnames.
    """
    print "LIST"
    r_loc_list = requests.get(ALTNAME_URL)
    myerror(r_loc_list)
    print len(json.loads(r_loc_list.text))

def search():
    """
    Search for an altname.
    """
    print "SEARCH"
    r_loc_search = requests.get("%s/search" % ALTNAME_URL, params={'altname': "FOOBARLOLZ"})
    myerror(r_loc_search)
    return json.loads(r_loc_search.text)

def go():
    """
    Run a workflow test.
    """
    loc_json = create_location()
    print loc_json
    alt_json = create(loc_json)
    print alt_json
    list_()
    search_json = search()
    print search_json
    del_json = delete(alt_json)
    print del_json
    delete_location(loc_json)

go()
