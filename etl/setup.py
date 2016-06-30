import ConfigParser
import logging
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

def config():
    cfg = ConfigParser.ConfigParser()
    cfg.read('../config.ini')
    return cfg

def log():
    fileConfig('../log.ini')
    logger = logging.getLogger()
    return logger

def db():
    cfg = config()

    engine = create_engine(cfg.get('DB', 'CXN'))
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return {'session': session, 'engine': engine}

