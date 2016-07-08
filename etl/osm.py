"""for interacting with osm data"""

import re
import time
import datetime
import xml.dom.minidom
from os import listdir

import overpass

import setup
import db

from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table, DDL
from sqlalchemy.orm import mapper, create_session
from sqlalchemy.ext.declarative import declarative_base

logger = setup.log()
session = setup.db()['session']
engine = setup.db()['engine']
metadata = MetaData(bind=engine)
Base = declarative_base()

api = overpass.API()
logger = setup.log()

def _add_wn_prefix(indict, worn):
    """add way_ or node_ to column values of an osm dict"""
    redict = {}
    for k,v in indict.iteritems():
        redict[worn + '_' + k] = v

    return redict

def _get_osm(indict, worn):
    #TODO: fetch multiple vals in osm call

    """return a dictionary of node and way over pass data with prefix
        input: tuple with dict of {uuid : way/nodeid}, 'way'/'node'
    """
    redict = {}

    for k,v in indict.iteritems():
        #redict[k] = _add_wn_prefix(api.Get('%s(%s)' % (worn, v)), worn)
        if worn == 'way':
            redict[k] = _add_wn_prefix({'w_t2' : 'wayx', 'w_t1' : 'wayb'}, worn)
        else:
            redict[k] = _add_wn_prefix({'n_t2' : 'nodee', 'n_t1' : 'nodeb'}, worn)

    return redict

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

def _push_element(osmdict, survey_nm):
    """store osm data for >=1 ways or nodes
        input: dict of dicts: {uuid : {obj col name : obj value}, survey name
        """

    db.add_missing_cols(osmdict.values(), survey_nm)
    db.update_valz('instanceId', osmdict, survey_nm)


def store_an_osm(cont, survey_nm):
    #TODO merge way and node dicts before call - not necessary but cool
    """pull most recent nodes and ways data for given surey from osm"""
    #dict of {uuid : osm data}
    multidict = {v['instanceId'] : v['local_osm_data'] for v in cont if v.has_key('local_osm_data')}

    waydict, nodedict = _get_osm_id(multidict)

    if waydict:
        logger.info("pulling way data for %s, id: %s" % (survey_nm, waydict.keys()))
        _push_element(_get_osm(waydict, 'way'), survey_nm)

    if nodedict:
        logger.info("pulling node data for %s, id: %s" % (survey_nm, nodedict.keys()))
        _push_element(_get_osm(nodedict, 'node'), survey_nm)