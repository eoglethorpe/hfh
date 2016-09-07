import ConfigParser
import logging
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

cfg = ConfigParser.ConfigParser()
cfg.read('/Users/ewanog/code/repos/hfh/hfh/etl/config.ini')

logging.config.fileConfig('/Users/ewanog/code/repos/hfh/hfh/etl/log.ini')
logger = logging.getLogger()

engine = create_engine(cfg.get('DB', 'CXN'))

Base = declarative_base()
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)