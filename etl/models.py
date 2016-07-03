import ConfigParser

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Date, exists, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateSchema
from sqlalchemy import create_engine

import setup
print dir(setup)
Base = declarative_base()

import os

cfg = ConfigParser.ConfigParser()
cfg.read('../config.ini')
CXN = cfg.get('DB', 'CXN')

session = setup.db()['session']
engine = setup.db()['engine']

class RawSurvey(Base):
    __table__ = Table('raw_survey', Base.metadata,
        Column('uu_id', String(), primary_key=True),
        Column('form_id', String()),
        Column('date_added', Date()),
        Column('content', String()),
        schema = 'raw')

class RawNode(Base):
    __table__ = Table('raw_node', Base.metadata,
        Column('id', String(), primary_key=True),
        Column('date_added', Date()),
        Column('content', String()),
        schema = 'raw')

class RawWay(Base):
    __table__ = Table('raw_way', Base.metadata,
        Column('id', String(), primary_key=True),
        Column('date_added', Date()),
        Column('content', String()),
        schema = 'raw')


def create():
    if not session.query(exists(select([("schema_name")]).select_from("information_schema.schemata")\
                                        .where("schema_name = 'surveys'"))).scalar():
        engine.execute(CreateSchema('surveys'))

    if not session.query(exists(select([("schema_name")]).select_from("information_schema.schemata")\
                                        .where("schema_name = 'raw'"))).scalar():
        engine.execute(CreateSchema('raw'))


    Base.metadata.create_all(engine)

create()