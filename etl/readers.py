"""
methods for reading in our different content types.
returns a tuple with file type and contents
"""

import xmltodict

#/Users/ewanog/Downloads/server_forms_for_script/16dcc24f-fe8f-44fe-aaeb-cadccb251e3c/data.xml'


def ingest(self, loc):
	"""figure out what kind of content type we are ingesting and send"""

	if loc.endswith('.osm'):
		return self.__read_osm(loc)

	elif loc.endswith('.json'):
		return self.__read_json(loc)

	elif loc.endswith('.xml'):
		return self.__read_xml(loc)

	elif loc.endswith('.FROMOSM?'):    	
		break

def __read_osm(self, loc):
	"""ingest osm"""


def __read_json(self, loc):
	"""ingest json - just return file contents"""	
	with open(loc) as f:
		content = ''.join(f.read().split())
	
	return ('json', content)

def __read_xml(self, loc):
	"""ingest xml"""

	with open(loc) as fd:
    	doc = xmltodict.parse(fd.read())

	return ('xml', dict([(str(k), str(v)) for k,v in doc.values()[0].items()])


def __read_FROMOSM(self, loc):


