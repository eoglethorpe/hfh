#TODO: check OS to see if running out of space?
#TODO: generalize uuid col name (config?)
#TODO: column types read somehow (adjust alter table DDL etc)
#TODO: delete tar.gz file
"""
main etl executor
"""
import json
import time
from collections import OrderedDict
from os import popen, listdir, walk
from os.path import isfile, join

import db
import osm
import mgmt

#import config and set vars
cfg = mgmt.cfg
INIT_LOC = cfg.get('AWS', 'init_loc')
INIT_IP = cfg.get('AWS', 'init_ip')
DEST_LOC = cfg.get('AWS', 'dest_loc')
PEM = cfg.get('AWS', 'pem')
DV = time.strftime("%Y-%m-%d:%H%M")
DV  = '2016-10-06:2212'


logger = mgmt.logger

def transfer(imgs):
    """move files from the prod server"""
    TAR = 'transfer.tar.gz'

    logger.info('Transfering AWS')
    try:
        logger.info('Tarring files')

        if imgs:
            popen('ssh -tt -i {vPEM} ubuntu@{vINIT_IP} "sudo tar czf \
                    {vINIT_LOC}/{vTAR} -C {vINIT_LOC}/submissions ."'\
                    .format(vPEM = PEM, vINIT_IP = INIT_IP, vINIT_LOC = INIT_LOC, vTAR = TAR))
        else:
            popen('ssh -tt -i {vPEM} ubuntu@{vINIT_IP} "sudo tar czf \
                    {vINIT_LOC}/{vTAR} -C {vINIT_LOC}/submissions . --exclude=*.jpg"'\
                    .format(vPEM = PEM, vINIT_IP = INIT_IP, vINIT_LOC = INIT_LOC, vTAR = TAR))

        logger.info('SCPing files')
        popen('mkdir {vDEST_LOC}/{fn}'\
            .format(vDEST_LOC = DEST_LOC, fn = DV))
        popen('scp -r -i {vPEM} ubuntu@{vINIT_IP}:{vINIT_LOC}/{vTAR} {vDEST_LOC}/{vDV}/{vTAR}'\
                .format(vPEM = PEM, vINIT_IP = INIT_IP, vINIT_LOC = INIT_LOC, vDV = DV, vTAR = TAR, vDEST_LOC = DEST_LOC))

        logger.info('Untarring files')
        popen('tar -xzvf {vDEST_LOC}/{vDV}/{vTAR} -C {vDEST_LOC}/{vDV}'\
            .format(vTAR = TAR, vDV = DV, vDEST_LOC = DEST_LOC))

    except Exception, e:
        logger.warn('Could not import AWS files\n', e)
        raise

    else:
        logger.info('Surveys transfer completed')

def _break_up_list(k, v, list):
    """if we want to keep repeating vals in same table as opposed to rel... currently unused"""
    list_jc = []
    for num, e in enumerate(v):
        #so we don't have 0'd number entry
        add = ''
        if num != 0:
            add = str(num) + '_'

        for ik, iv in e.iteritems():
            list_jc[k + '_' + add + ik] = iv

    return list_jc

# def _break_up(jc, survey_nm):
#     """take in json contents for a single entry and handle dicts and lists
#         returns structured json content and lists for relational table creation"""
#     #TODO: param to decide if creating relational tables or keeping in same table
#     new_jc = OrderedDict()
#     rel = []
#
#     for k,v in jc.iteritems():
#         new_jc[k] = v
#
#     return {'content': new_jc, 'rel': rel}

def _parse_a_json(path, survey_nm):
    """iterate through json for a given survey on a given data.json file"""
    with open(path + 'data.json') as f:
        content = ' '.join(f.read().split())

    ret = json.loads(content)

    return {'content': ret, 'id' : ret['meta']['formId']}

def _get_an_entry(path, survey_nm):
    """handle JSON and OSM files for a given entry"""
    psd = _parse_a_json(path, survey_nm)

    #add in OSM file contents if one exists
    if osm.get_osm_file(path):
        psd['content']['local_osm_data'] = osm.get_osm_file(path)

    return psd


def find_rels(cont):
    """iterate through all entries and identify which columns contain a list and are relational entries
        input: cont (list of dictionaries)
        return: ret (list of columns that relational"""
    ret = []

    for v in cont:
        for ik, iv in v.iteritems():
            if isinstance((iv), list):
                if ik not in ret:
                    ret.append(ik)

    return ret

def _break_up(cont):
    """take in full contents, identify relational entries (ie lists) and add them to a seperate list for insertion,
        dicts for grouped questions and individual items
        input: cont (list of dictionaries)
        return: cont (list of dictionaries without rels), rel (relatinonal entries)"""

    cols = find_rels(cont)
    rel = []
    ret_cont = []
    #iterate through each entry in cont and then through each item
    for v in cont:
        add_ent = {}
        for ik, iv in v.iteritems():
            #if this is a relational item
            if ik in cols:
                if not isinstance(iv, list):
                    #if there is only one entry for a relational item we need to make it a list so it can be traversed
                    iv = [iv]

                for ind in iv:
                    #add in additional data
                    ind['general_info_registration_number'] = v['general_info']['registration_number']
                    ind['meta_instanceId'] = v['meta']['instanceId']
                rel.append({'col': ik, 'vals': iv})

            #if the value is part of a group - non repeating
            elif isinstance(iv,dict):
                for entk, entv in iv.iteritems():
                    add_ent[ik + '_' + entk] = entv
            else:
                add_ent[ik] = iv

        #if we have added any non-relational items... should probably always be true
        if add_ent:
            ret_cont.append(add_ent)

    return ret_cont, rel

def get_a_survey(schema, surname):
    base = DEST_LOC + DV

    try:
        cd = join(base, surname)
    except Exception, e:
        logger.warn('Could not locate survey %s' % surname, e)

    logger.info('Pulling %i entries for %s' % (len(walk(cd).next()[1]), surname))
    cont = []
    rel = []

    #go through all the entries for a given survey
    for sl in walk(cd).next()[1]:
        ent = _get_an_entry(join(cd, sl) + '/', surname)
        cont += [ent['content']]

    cont, rel = _break_up(cont)

    #store main entries
    logger.info('***Storing main table entries***')
    db.store(cont, ent['id'])

    logger.info('***Storing relational info***')
    #store relational entries'
    db.relational_ents(schema, surname, rel)

    #get and store OSM data
    osm.store_an_osm(cont, ent['id'])


def get_all_surveys(schema):
    """ iterate through all surveys"""
    base = DEST_LOC + DV
    surveys = [f for f in listdir(base) if not isfile(join(base, f))]
    logger.info('****Extracting the following surveys...****')
    logger.info(surveys)

    #directory structure: .../submissions/date_file/surveys/entry_id/.osm|.xml|.json

    #traverse through to get entries and their data files
    for fl in walk(base).next()[1]:
        get_a_survey(schema, fl)

if __name__ =='__main__':
    SCHEMA = 'surveys'
    #transfer(imgs = False)
    db._clear_schema(SCHEMA)
    get_all_surveys(SCHEMA)
