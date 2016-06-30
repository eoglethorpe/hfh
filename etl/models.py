import ConfigParser

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateSchema
from sqlalchemy import create_engine

Base = declarative_base()

import os
print os.getcwd()

cfg = ConfigParser.ConfigParser()
cfg.read('../config.ini')
CXN = cfg.get('DB', 'CXN')
print cfg.items('DB')

class Raw(Base):
    __table__ = Table('raw_survey', Base.metadata,
        Column('uu_id', String(), primary_key=True),
        Column('form_id', String()),
        Column('date_added', Date()),
        Column('content', String()),
        schema = 'surveys')

def create():
    engine = create_engine(CXN)
    #engine.execute(CreateSchema('surveys'))
    Base.metadata.create_all(engine)

create()