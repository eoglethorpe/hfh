"""for interacting with extracting data from osm"""

import overpass
api = overpass.API()

def get_way(way_id):
    """return a dictionary of overpass data"""
    r = api.Get('way(%s)' % way_id)

    #do stuff
    return r

def get_node(node_id):
    """return a dictionary of overpass data"""
    r = api.Get('node(%s)' % node_id)

    #do stuff
    return r
