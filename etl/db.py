"""
for interfacing with DB
"""
import ConfigParser
import datetime
import logging
from logging.config import fileConfig

from models import Raw
import setup

from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table, DDL
from sqlalchemy.orm import mapper, create_session
from sqlalchemy.ext.declarative import declarative_base

logger = setup.log()
session = setup.db()['session']
engine = setup.db()['engine']
metadata = MetaData(bind=engine)
Base = declarative_base()


def _store_raw(cont, survey_name):
    logger.info('Storing raw entries for ' + survey_name)

    existing = [v.uu_id for v in session.query(Raw).all()]

    for r in cont:
        if r['instanceId'] not in existing:
            to_add = Raw(
                uu_id = r['instanceId'],
                form_id = survey_name,
                content = str(cont),
                date_added = datetime.datetime.now()
            )
            session.add(to_add)
            logger.info('Storing entry for survey: %s id:%s' % (survey_name,r['instanceId']))
        else:
            logger.warn('Existing raw entry for survey: %s id:%s' % (survey_name,r['instanceId']))

    session.commit()

def _create_table(cont, survey_name):
    """create table and all available columns"""
    keys = []
    for v in cont:
        keys+= list(v.iterkeys())

    keys = list(set(keys))
    keys.remove('instanceId')

    class TempTable(Base):
        __table__ = Table(survey_name, Base.metadata,
            Column('instanceId', String(), primary_key=True),
            * (Column(v, String()) for v in keys),
            schema = 'surveys')

    Base.metadata.create_all(engine)

def _add_missing_cols(cont, survey_name, ct):
    keys = []
    for v in cont:
        keys+= list(v.iterkeys())

    cols = [c.name for c in ct.columns]

    for v in list(set(keys)):
        if v not in cols:
            engine.execute("ALTER TABLE %s ADD COLUMN %s VARCHAR DEFAULT NULL" % ('surveys.' + survey_name, v))
            logger.info("Adding column %s for %s" % ('surveys.' + survey_name, v))

def _insert_new_valz(cont, survey_name):
    """check to see if we have new columns and add data"""
    ct = Table(survey_name, metadata, autoload=True, schema = 'surveys')
    _add_missing_cols(cont, survey_name, ct)

    class Temp(Base):
        __table__ = ct

    existing = [v.instanceId for v in session.query(Temp).all()]

    for v in cont:
        try:
            if v['instanceId'] not in existing:
                v = {k:str(v) for k, v in v.iteritems()}
                Temp.__table__.insert().execute([v])
        except:
            print 'ERROR' + str(v)



def store(cont, survey_name):
    """store a batch of surveys"""
    _store_raw(cont, survey_name)

    if not engine.has_table(survey_name, schema='surveys'):
        logger.info('Creating table for %s' % survey_name)
        _create_table(cont, survey_name)

    _insert_new_valz(cont, survey_name)