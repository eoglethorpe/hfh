import argparse

import osm


parser = argparse.ArgumentParser()

parser.add_argument('schema')
parser.add_argument('survey_nm')
parser.add_argument('uuidcol')
parser.add_argument('wcol')
parser.add_argument('ncol')

def update_osm():
    args = parser.parse_args()
    osm.update_all_osm(args.schema, args.survey_nm, args.uuidcol, args.wcol, args.ncol)


if __name__ == '__main__':
    update_osm()