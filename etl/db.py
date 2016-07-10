"""
for interfacing with DB
"""
import ConfigParser
import datetime
import logging
from logging.config import fileConfig

from sqlalchemy.engine import result

from models import RawSurvey
import setup

from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table, event
from sqlalchemy.orm import mapper, create_session
from sqlalchemy.ext.declarative import declarative_base

logger = setup.log()
session = setup.db()['session']
engine = setup.db()['engine']
metadata = MetaData(bind=engine)
Base = declarative_base()


def _store_raw(cont, survey_name):
    logger.info('Storing raw entries for ' + survey_name)

    existing = [v.uu_id for v in session.query(RawSurvey).all()]

    for r in cont:
        if r['instanceId'] not in existing:
            to_add = RawSurvey(
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

def _fetch_table(survey_name):
    """return table object of table created on the fly"""
    metadata = MetaData(bind=engine)
    return Table(survey_name, metadata, autoload=True, schema = 'surveys')

def add_missing_cols(cont, survey_name):
    """add any additional columns and return table object"""
    session.close()
    metadata = MetaData(bind=engine)
    ct =  _fetch_table(survey_name)
    keys = []

    for v in cont:
        keys+= list(v.iterkeys())

    cols = [c.name for c in ct.columns]

    for v in list(set(keys)):
        if v not in cols:
            logger.info("Adding column %s for %s" % (v, 'surveys.' + survey_name))
            session.close()
            engine.execute("ALTER TABLE %s ADD COLUMN %s VARCHAR DEFAULT NULL" % ('surveys.' + survey_name, v))

    return ct

def update_valz(idcol, indict, survey_name):
    #TODO: possible update all in 1 call? not sure if worth effort if update calls are fast enough and low volume
    #TODO: fix idcol to use ref instead of hardcode
    """update given columns with associated values
        idcol: column whose id is being used in update
        cont: dict of dicts containing {uuid : {colnm : val}}
        survey_name: table to update
    """
    ct = _fetch_table(survey_name)

    for k,v in indict.iteritems():
        stmt = ct.update().where(ct.c.instanceId == k).values(v)
        engine.execute(stmt)

def _insert_new_valz(cont, survey_name):
    """check to see if we have new entries and add data"""
    ct = add_missing_cols(cont, survey_name)

    class Temp(Base):
        __table__ = ct

    print 'right before'
    session.close()
    existing = [v.instanceId for v in session.query(Temp).all()]
    print 'right after'

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