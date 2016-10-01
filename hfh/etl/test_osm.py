import unittest
from unittest import TestCase

import osm


class MyTest(unittest.TestCase):
    def test_geomify_way(self):
        inp = [[-77.1733462, 38.8921716], [-77.1733607, 38.8921144], [-77.1733106, 38.8921068], \
               [-77.173323, 38.8920574], [-77.1732006, 38.8920386], [-77.1731737, 38.8921452],
               [-77.1733462, 38.8921716]]

        res = 'POLYGON((-77.1733462 38.8921716,-77.1733607 38.8921144,-77.1733106 38.8921068,-77.173323 38.8920574, \
        -77.1732006 38.8920386,-77.1731737 38.8921452,-77.1733462 38.8921716))'

        self.assertEqual(osm._geomify_way(inp).replace(' ', ''), res.replace(' ', ''))

    def test_geomify_node(self):
        inp = [-77.1733462, 38.8921716]
        res = 'POINT(-77.1733462 38.8921716)'

        self.assertEqual(osm._geomify_node(inp), res)

    def test_qry_osm_less(self):
        res = osm._qry_osm([130, 3487709906], 'node')
        self.assertEqual(len(res), 2)
