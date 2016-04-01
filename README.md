# hfh

ETL logic:

1. Send data from OMK prod server to scripting server
2. Extract way ids from OMK import and pull their data from OSM
3. F/e entry, upload to PostGIS:
  * .json
  * .xml
  * .osm
  * relevant OSM
