import unittest

import osm

class MyTest(unittest.TestCase):
    def test_geomify_way(self):
        inp = [[-77.1733462, 38.8921716], [-77.1733607, 38.8921144], [-77.1733106, 38.8921068], \
               [-77.173323, 38.8920574], [-77.1732006, 38.8920386], [-77.1731737, 38.8921452], [-77.1733462, 38.8921716]]

        res = 'POLYGON((-77.1733462 38.8921716,-77.1733607 38.8921144,-77.1733106 38.8921068,-77.173323 38.8920574, \
        -77.1732006 38.8920386,-77.1731737 38.8921452,-77.1733462 38.8921716))'

        self.assertEqual(osm._geomify_way(inp).replace(' ', ''), res.replace(' ', ''))

    def test_geomify_node(self):
        inp = [-77.1733462, 38.8921716]
        res = 'POINT(-77.1733462 38.8921716)'

        self.assertEqual(osm._geomify_node(inp), res)

    def test_get_osm_way(self):
        print osm._get_osm({1:'256667335'}, 'way')

        {1: {'way_type': 'Feature', 'way_properties_addr_city': 'Falls Church', 'way_geometry_coordinates': [[-77.1733462, 38.8921716], [-77.1733607, 38.8921144], [-77.1733106, 38.8921068], [-77.173323, 38.8920574], [-77.1732006, 38.8920386], [-77.1731737, 38.8921452], [-77.1733462, 38.8921716]], 'way_properties_addr_street': 'Langston Lane', 'way_properties_addr_state': 'va', 'way_properties_addr_postcode': '22046', 'way_geometry_type': 'LineString', 'way_properties_building': 'house', 'way_id': 256667335, 'way_properties_addr_housenumber': '603'}}

    def test_get_osm_node(self):
        print osm._get