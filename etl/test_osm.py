import unittest

import osm

class MyTest(unittest.TestCase):
    def test_geomify_way(self):
        osmdict_in = { 1234 : { 'etc' : 31,
                             'way_geometry_coordinates' : '{"(85.0876212,28.0291205)","(85.0876491,28.0290749)",\
                             "(85.0877664,28.0291307)","(85.0877385,28.0291763)","(85.0876212,28.0291205)"}'
                            }
                    }

        osmdict_out = { 1234 : { 'etc' : 31,
                             'way_geometry_coordinates' :
        'POLYGON(85.0876212 28.0291205,85.0876491 28.0290749,' \
        '85.0877664 28.0291307, 85.0877385 28.0291763, 85.0876212 28.0291205)'
                                 }
                        }

        self.assertEqual(osm.geomify(osmdict_in), osmdict_out)

    def test_geomify_node(self):
        pass