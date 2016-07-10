#TODO: check OS to see if running out of space?
#TODO: generalize uuid col name
#TODO: column types read somehow (adjust alter table DDL etc)
"""
main etl executor
"""
import time
import json
from os import popen, listdir, walk
from os.path import isfile, join

import overpass

import db
import setup
import osm
import test

#import config and set vars
cfg = setup.config()
INIT_LOC = cfg.get('AWS', 'init_loc')
INIT_IP = cfg.get('AWS', 'init_ip')
DEST_LOC = cfg.get('AWS', 'dest_loc')
PEM = cfg.get('AWS', 'pem')
DV = time.strftime("%Y-%m-%d:%H%M")
DV = '2016-05-26:1211'

logger = setup.log()

def transfer():
    """move files from the prod server"""
    TAR = 'transfer.tar.gz'

    logger.info('Transfering AWS')
    try:
        logger.info('Tarring files')
        popen('ssh -tt -i {vPEM} ubuntu@{vINIT_IP} "sudo tar czf \
                {vINIT_LOC}/{vTAR} -C {vINIT_LOC}/submissions ."'\
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

def get_an_entry(path):
    res,id = _get_json(path)

    if osm.get_osm_file(path):
        res['local_osm_data'] = osm.get_osm_file(path)

    return res, id

def _get_json(path):
    with open(path + 'data.json') as f:
		content = ''.join(f.read().split())

    jc = json.loads(content)

    #add meta contents as top level info
    for k in jc['meta'].iterkeys():
        if k != 'deviceId':
            jc[k] = jc['meta'][k]

    return jc, jc['formId']

def get_a_survey(surname):
    base = DEST_LOC + DV

    try:
        cd = join(base, surname)
    except Exception, e:
        logger.warn('Could not locate survey %s' % surname, e)

    logger.info('Pulling %i entries for %s' % (len(walk(cd).next()[1]), surname))
    cont = []
    for sl in walk(cd).next()[1]:
        res, id = get_an_entry(join(cd, sl) + '/')
        cont+=[res]

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
        pass

if __name__ =='__main__':
    get_all_surveys()
    #transfer()