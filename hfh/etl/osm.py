"""for interacting with osm data"""

import datetime
import time
import xml.dom.minidom
from os import listdir

import overpass
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

import db
import mgmt

logger = mgmt.logger
session = mgmt.Session()
engine = mgmt.engine
Base = declarative_base()
metadata = MetaData(bind=engine)

def _add_wn_prefix(indict, worn):
    """add way_ or node_ to column values of an osm dict"""
    redict = {}
    for k,v in indict.iteritems():
        redict[worn + '_' + k] = v

    return redict

def _osm_wn_qry(ids, worn):
    """structure query to send to OSM - generates for multiple ID looks up in one call
        input: list of IDs, 'way'/'node'
        return: query to use for OSM call
    """
    return '(' + ''.join(map(str, ['%s(%s);'% (worn,v) for v in ids])) + ')'

def _columnify_osm_res(res, worn):
    """turn a dict of osm results into a dict that can be used for db insertion
        input: osm resultset for just one feature
        return: dict with values of colname:value
            colname structured with layers of dict ie geometry_cooredinates or properties_building

            sample res: {"features": [{"geometry": {"coordinates": [,], "type": "Point"},
                            "id": int, "properties": {}, "type": "Feature"}],
                            "type": "FeatureCollection"}

            https://github.com/mvexel/overpass-api-python-wrapper/blob/master/overpass/api.py#L137-L141
    """
    coldict = {}

    for k,v in res.iteritems():
        if not isinstance(v, dict):
            coldict['%s' % k] = v
        else:
            for sk,sv in v.iteritems():
                #some property keys have colons which won't work as col names, so replace with _
                coldict['%s_%s' % (k, sk.replace(':','_'))] = sv

    if worn == 'way':
        coldict['geometry_coordinates'] = _geomify_way(coldict['geometry_coordinates'])
    elif worn == 'node':
        coldict['geometry_coordinates'] =_geomify_node(coldict['geometry_coordinates'])
        pass

    return coldict

def _get_osm(indict, worn):
    #TODO: fix logic of this
    """return a dictionary of node and way over pass data with prefix for a series of wn IDs
        input: tuple with dict of {uuid : way/nodeid}, 'way'/'node'
    """
    #middict is used as a midddle man for processsing
    middict = {}
    ids = filter(None, indict.values())
    logger.info('Pulling osm %s data for %s' % (worn, str(ids)))

    api = overpass.API()
    osmdict = api.Get(_osm_wn_qry(ids, worn))

    for v in osmdict['features']:
        middict[str(v['id'])] = v


    retdict = {}
    #use the value of indict to match with key of redict to match osm data with proper uuid
    for k,v in indict.iteritems():
        if middict.has_key(v):
            retdict[k] = _add_wn_prefix(_columnify_osm_res(middict[v], worn), worn)

    #TODO: better way to terminate overpass connections - http://overpass-api.de/api/kill_my_queries
    del(api)

    return retdict

def _get_max_nw(osment):
    """get ids for most recently added nodes or ways
        input: a string repr of an osm xml file
        output: a dict containing {'way' : id, 'node': id} if the given element is in the osm string
    """
    tsformat = '%Y-%m-%dT%H:%M:%SZ'
    curosm = xml.dom.minidom.parseString(osment.replace("'","\"")).documentElement

    attdict = [{'id' : e.getAttribute('id'), 'ts' : time.mktime(datetime.datetime.strptime(\
            e.getAttribute('timestamp'), tsformat).timetuple()), 'type': e.localName} for e in curosm.childNodes]

    rdict = {}
    for t in ('way', 'node'):
        clist = [i for i in attdict if i['type'] == t]
        if clist:
            rdict[t] = max(clist, key=lambda x:x['ts'])['id']

    return rdict

def _get_osm_id(indict):
    """extract osm ids from >=1 list of .osm files contents - only reads most recent entry
        input: dict with {uuid: osm data}
        output: dicts of {uuid: wayid} , {uuid: nodeid}
    """
    waydict = {}
    nodedict = {}

    for k,v in indict.iteritems():
        maxs = _get_max_nw(v)

        if maxs.has_key('way'):
            waydict[k] = maxs['way']
        if maxs.has_key('node'):
            nodedict[k] = maxs['node']

    return waydict, nodedict

def get_osm_file(path):
    try:
        loc = [v.split('.')[-1] for v in listdir(path)].index('osm')
        with open(path + listdir(path)[loc]) as f:
		    content = ' '.join(f.read().split())

        return content

    except:
        pass

def _geomify_node(coordlist):
    return 'POINT(' + str(coordlist[0]) + ' ' + str(coordlist[1]) + ')'

def _geomify_way(coordlist):
    """convert to coordinate value to POLYGON()"""
    out = 'POLYGON(('
    for i,v in enumerate(coordlist):
        out += str(v[0]) + ' ' + str(v[1])
        if i == len(coordlist)-1:
            out += '))'
        else:
            out += ','

    return out

def _push_element(osmdict, survey_nm):
    """store osm data for >=1 ways or nodes
        input: dict of dicts: {uuid : {obj col name : obj value}, survey name
        """
    db.add_missing_cols(osmdict.values(), survey_nm)
    db.update_valz('meta_instanceId', osmdict, survey_nm)


def update_all_osm(schema, survey_nm, uuidcol, wcol, ncol):
    #TODO: handle if column doesnt' exist (currently just get None object returned
    """blanket update all OSM values with IDs from wcol and/or ncol"""
    #create dicts of {uuid: wnid} as this is format needed for methods
    waydict = dict(zip(db.get_column(survey_nm, uuidcol), db.get_column(survey_nm, wcol)))
    nodedict = dict(zip(db.get_column(survey_nm, uuidcol), db.get_column(survey_nm, ncol)))

    _push_element(_get_osm(waydict, 'way'), survey_nm)
    _push_element(_get_osm(nodedict, 'node'), survey_nm)

def store_an_osm(cont, survey_nm):
    #TODO merge way and node dicts before call - not necessary but cool
    """pull most recent nodes and ways data for given surey from osm"""
    #dict of {uuid : osm data}
    multidict = {v['meta_instanceId'] : v['local_osm_data'] for v in cont if v.has_key('local_osm_data')}

    waydict, nodedict = _get_osm_id(multidict)

    if waydict:
        logger.info("Pulling way data for %s, id: %s" % (survey_nm, waydict.keys()))
        _push_element(_get_osm(waydict, 'way'), survey_nm)

    if nodedict:
        logger.info("Pulling node data for %s, id: %s" % (survey_nm, nodedict.keys()))
        _push_element(_get_osm(nodedict, 'node'), survey_nm)