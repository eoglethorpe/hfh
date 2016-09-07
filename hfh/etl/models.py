from sqlalchemy import Column, String, Table, Date, exists, select
from sqlalchemy.schema import CreateSchema

import mgmt

Base = mgmt.Base
CXN = mgmt.cfg.get('DB', 'CXN')
session = mgmt.Session()
engine = mgmt.engine

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
