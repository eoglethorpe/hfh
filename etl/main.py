#TODO: check OS to see if running out of space?

"""
main etl executor
"""
import time
from os import environ, popen

#import config and set vars
import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read('config.ini')
INIT_LOC = cfg.get('AWS', 'init_loc')
INIT_IP = cfg.get('AWS', 'init_ip')
DEST_LOC = cfg.get('AWS', 'dest_loc')
PEM = cfg.get('AWS', 'pem')

#logging
import logging
from logging.config import fileConfig

fileConfig('../log.ini')
logger = logging.getLogger()

def transfer():
    """move files from the prod server"""
    TAR = 'transfer.tar.gz'
    DV = time.strftime("%Y-%m-%d:%H%M")

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

if __name__ =='__main__':
    transfer()
