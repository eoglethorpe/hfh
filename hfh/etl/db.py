"""
for interfacing with DB
"""
import datetime
import traceback
from itertools import groupby

from sqlalchemy.exc import InternalError
from sqlalchemy import Column, String, MetaData, Table, Sequence, Integer
from sqlalchemy.ext.declarative import declarative_base

import mgmt
from models import RawSurvey

logger = mgmt.logger
session = mgmt.Session()
engine = mgmt.engine
Base = mgmt.Base
metadata = MetaData(bind = engine, schema = 'surveys')

COORD_COL = mgmt.cfg.get('OSM', 'WAY_COL')

def _store_raw(cont, survey_name):
    logger.info('Storing raw entries for ' + survey_name)

    existing = [v.uu_id for v in session.query(RawSurvey).all()]

    for r in cont:
        if r['meta_instanceId'] not in existing:
            to_add = RawSurvey(
                uu_id = r['meta_instanceId'],
                form_id = survey_name,
                content = str(cont),
                date_added = datetime.datetime.now()
            )
            session.add(to_add)
            logger.info('Storing entry for survey: %s id:%s' % (survey_name,r['meta_instanceId']))
        else:
            logger.warn('Existing raw entry for survey: %s id:%s' % (survey_name,r['meta_instanceId']))

    session.commit()

def _create_table_serial_uuid(schm, survey_name):
    """create table with serial UUID"""
    seq = Sequence('id')
    __table__ = Table(survey_name, metadata,
        Column('id', Integer, seq, primary_key=True, server_default=seq.next_value()), schema = schm)

    metadata.create_all(engine)
    logger.info('Created table ' + str(schm) + '.' + survey_name)

def _create_table(cont, survey_name):
    """create table"""
    __table__ = Table(survey_name, Base.metadata,
        Column('meta_instanceId', String(), primary_key=True), schema = 'surveys')

    __table__.create(checkfirst=True)
    logger.info('Created table' + survey_name)

def _fetch_table(survey_name):
    """return table object of table created on the fly"""
    metadata = MetaData(bind = engine, schema = 'surveys')
    return Table(survey_name, metadata, autoload=True, schema = 'surveys')


def relational_ents(schema, survey_name, cont):
    """handle creation/update for a relational table w/ values from a repeating question
        input: survey name,
        cont: [{vals: [values], col: [column name} ...] """
    session.close()
    metadata = MetaData(bind=engine, schema=schema)
    metadata.reflect(engine)

    c_srt = sorted(cont, key = lambda x: x['col'])

    for key, group in groupby(c_srt, lambda x: x['col']):
        tbl_nm = '%s_%s' % (survey_name, key)
        logger.info('Handling relational table: ' + tbl_nm)

        #check and if see we already have a table for this column
        if tbl_nm not in [t.name for t in metadata.tables.values()]:
            _create_table_serial_uuid(schema, tbl_nm)

        #for each listing in an entry, add a column listing the count
        for v in group:
            for i,iv in enumerate(v['vals']):
                iv['count'] = i+1

        _insert_new_valz([p for p in v['vals'] for v in c_srt], tbl_nm)

def add_missing_cols(cont, survey_name):
    """add any additional columns and return table object"""
    ct =  _fetch_table(survey_name)
    keys = []

    for v in cont:
        keys += v.iterkeys()

    cols = [c.name.lower() for c in ct.columns]

    with engine.begin() as connection:
        for v in sorted(set(keys)):
            if v.lower() not in cols:
                    if v.lower() in ('way_' + COORD_COL, 'node_' + COORD_COL) :
                        logger.info("Adding geometry column %s for %s" % (v, 'surveys.' + survey_name))
                        connection.execute('ALTER TABLE %s ADD COLUMN "%s" GEOMETRY DEFAULT NULL' % ('surveys.' + survey_name, v))
                        logger.info("Col added")
                    else:
                        logger.info("Adding column %s for %s" % (v, 'surveys.' + survey_name))
                        connection.execute('ALTER TABLE %s ADD COLUMN "%s" VARCHAR DEFAULT NULL' % ('surveys.' + survey_name, v))
                        logger.info("Col added")

def get_column(survey_name, colnm):
    """get all values for a given column"""
    ct = _fetch_table(survey_name)

    if ct.c.has_key(colnm):
        #all() returns a tuple, we want first value as only returning 1 column
        ret = [v[0] for v in session.query(ct.c.get(colnm)).all()]
        session.commit()
        return ret
    else:
        return None

def update_valz(idcol, indict, survey_name):
    #TODO: possible update all in 1 call? not sure if worth effort if update calls are fast enough and low volume
    """update given columns with associated values
        idcol: column whose id is being used in update
        cont: dict of dicts containing {uuid : {colnm : val}}
        survey_name: table to update
    """
    ct = _fetch_table(survey_name)
    err = []

    with engine.begin() as connection:
        for k,v in indict.iteritems():
            stmt = ct.update().where(ct.c.meta_instanceId == k).values(v)
            try:
                connection.execute(stmt)

            except Exception, e:
                #catch issue where there is an unclosed polygon
                err.append(str(stmt.parameters))
                connection = engine.connect()
                continue

    if len(err) > 0:
        logger.warn('\n\n*/*/* Problems inserting the following: */*/*\n')
        logger.warn(err)

def _insert_new_valz(cont, survey_name):
    """check to see if we have new entries and add data
        cont is a list containing dicts of values to insert [{col1: val1 etc} ... {col1: valx}]"""
    add_missing_cols(cont, survey_name)

    class Temp(Base):
        __table__ = _fetch_table(survey_name)

    existing = [v.meta_instanceId for v in session.query(Temp).all()]
    session.commit()

    with engine.begin() as connection:
        for v in cont:
            try:
                if v['meta_instanceId'] not in existing:
                    v = {k:str(v) for k, v in v.iteritems()}
                    ins = Temp.__table__.insert()
                    connection.execute(ins, [v])

            except Exception, e:
                raise

def _clear_schema(schm):
    #clear the a given schema
    logger.info('Deleting all tables for ' + schm)
    metadata = MetaData(bind=engine, schema = schm)
    metadata.reflect(engine)
    for t in metadata.tables.values():
        if t.schema == schm:
            _fetch_table(t.name).drop()

def store(cont, survey_name):
    """store a batch of surveys"""
    #_store_raw(cont, survey_name)

    logger.info('Creating table for %s' % survey_name)
    _create_table(cont, survey_name)

    _insert_new_valz(cont, survey_name)
    engine.dispose()