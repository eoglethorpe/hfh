"""
methods for reading in our different content types. returns a dict
"""

class read(Object):
	def __init__():
		pass

	def ingest(self, loc):
		"""figure out what kind of content type we are ingesting and send"""

		with open(loc) as f:
			content = ''.join(f.read().split())

    	if loc.endswith('.osm'):
    		return self.__read_osm(content)

    	elif loc.endswith('.json'):
    		return self.__read_json(content)

    	elif loc.endswith('.xml'):
			return self.__read_xml(content)

		elif loc.endswith('.FROMOSM?'):    	
			break

	def __read_osm(self, content):
		"""ingest osm"""


	def __read_json(self, content):
		"""ingest json"""
			return json.loads(content)

	def __read_xml(self, content):
		#do we need?
			pass

	def __read_FROMOSM(self, content):


