from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

import db

class Test_db (TestCase):

    def test_relational_ents_mk_tbl(self):
        ents = [{'vals' : [{'meta_instanceId': 1}], 'col' : 'table1'},
               {'vals' : [{'meta_instanceId': 1, 'col2': 2}], 'col' : 'table2'},
               {'vals' : [{'meta_instanceId': 3}], 'col' : 'table1'}]

        db.relational_ents(None, 'bob', ents)

        self.assertEqual(sorted([t.name for t in db.metadata.tables.values()]), sorted(['bob_table1', 'bob_table2']))

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.session = Session(self.engine)
        self.Base = declarative_base()
        self.Base.metadata.bind = self.engine
        self.Base.metadata.create_all(self.engine)

    def tearDown(self):
        self.Base.metadata.drop_all(self.engine)