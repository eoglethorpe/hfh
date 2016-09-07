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
DV = '2016-05-26:1211'

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

def _get_an_entry(path, survey_nm):
    res,id = _get_json(path, survey_nm)

    if osm.get_osm_file(path):
        res['local_osm_data'] = osm.get_osm_file(path)

    return res, id

def _break_up_list(k, v, list):
    """if we want to keep repeatin vals in same table"""
    list_jc = []
    for num, e in enumerate(v):
        #so we don't have 0'd number entry
        add = ''
        if num != 0:
            add = str(num) + '_'

        for ik, iv in e.iteritems():
            list_jc[k + '_' + add + ik] = iv

    return list_jc

def _break_up(jc, survey_nm):
    """take in json contents for a given entry and break up dicts and lists"""
    new_jc = OrderedDict()

    for k,v in jc.iteritems():
        #if the value is part of a group - non repeating
        if isinstance(v,dict):
            for ik, iv in v.iteritems():
                new_jc[k + '_' + ik] = iv

        elif isinstance(v,list):
            #if the value is part of repeating question (ie household member occupations)
            for ent in v:
                db.rltl_tbl(tbl = survey_nm, col = k, addl = {'general_info_registration_number' : jc['general_info']['registration_number'],
                     'meta_instanceId' : jc['meta']['instanceId']}, vals = v)

        #TODO: param to decide if creating relational tables or keeping in same table
        # elif isinstance(v,list):
        #     new_jc += _break_up_list(k, v, list)

        else:
            new_jc[k] = v

    return new_jc

def _get_json(path, survey_nm):
    with open(path + 'data.json') as f:
        content = ' '.join(f.read().split())

    jc = _break_up(json.loads(content), survey_nm)

    return jc, jc['meta_formId']

def get_a_survey(surname):
    base = DEST_LOC + DV

    try:
        cd = join(base, surname)
    except Exception, e:
        logger.warn('Could not locate survey %s' % surname, e)

    logger.info('Pulling %i entries for %s' % (len(walk(cd).next()[1]), surname))
    cont = []

    for sl in walk(cd).next()[1]:
        res, id = _get_an_entry(join(cd, sl) + '/', surname)
        cont += [res]

    db.store(cont, id)
    osm.store_an_osm(cont, id)


def get_all_surveys():
    """ iterate through all surveys"""
    base = DEST_LOC + DV
    surveys = [f for f in listdir(base) if not isfile(join(base, f))]
    logger.info('****Extracting the following surveys...****')
    logger.info(surveys)

    #directory structure: .../submissions/date_file/surveys/entry_id/.osm|.xml|.json

    #traverse through to get entries and their data files
    for fl in walk(base).next()[1]:
        get_a_survey(fl)

if __name__ =='__main__':
    db._clear_schema('surveys')
    get_all_surveys()
    #transfer(imgs = False)