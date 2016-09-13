import ConfigParser
import logging
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

cfg = ConfigParser.ConfigParser()
cfg.read('./config.ini')

# FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
# logging.basicConfig(filename='example.log',level=logging.DEBUG, format = FORMAT)
#logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

logging.config.fileConfig('./log.ini')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

engine = create_engine(cfg.get('DB', 'CXN'))

Base = declarative_base()
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)
