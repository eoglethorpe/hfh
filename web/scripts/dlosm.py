import ConfigParser
from os import popen

cfg = ConfigParser.ConfigParser()
cfg.read('../config.ini')
LOC = cfg.get('AWS', 'DEST_LOC')

survey_name = ''

popen('sudo tar -cf t.tar.gz `find %s/%s | egrep "\.osm$"`' % (LOC, survey_name))