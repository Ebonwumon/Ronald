import digraph
from types import *
class Server:
	"""
	The server class. Works by instantiating a server object which has only
	one user-accessable member method: get_route.
	"""

	def __init__(self, graph_file):
		vertex_edge_tuple = digraph.graph_from_text(graph_file)
		self.vertices = vertex_edge_tuple[0]
		self.edges = vertex_edge_tuple[1]
		self.graph = digraph.Digraph(self.edges)

	def _calculate_route(self, origin_lat, origin_lon, dest_lat, dest_lon):
		"""
		Given the original and destination lat/lons, calculate route determines
		the best method of travel utilizing best_route finding algorithms in
		TODO


		"""
		pass

	
	def _parse_input(self, in_str):
		"""
		Takes a space separated list of 4 inputs. Inputs must be integers

		>>> S = Server("test.txt")
		>>> result = S._parse_input("5365488 -11333914 5364727 -11335890")
		>>> result['lat']['orig']
		5365488
		>>> result['lat']['dest']
		5364727
		>>> result['lon']['orig']
		-11333914
		>>> result['lon']['dest']
		-11335890
		>>> S._parse_input("1114")
		Traceback (most recent call last):
			...
		Exception: You must pass in 4 inputs
		
		This is code to test later when exceptions are easier
		S._parse_input("eggs ham cheese yum")

		"""
		split_string = in_str.split(' ')

		if len(split_string) != 4:
			raise Exception('You must pass in 4 inputs')

		# We want to change all strings to integers. If not, exceptions must be raised

		for i, value in enumerate(split_string):
			try:
				int_cast = int(value)
			except ValueError:
				raise TypeError('All inputs must be integers')
			split_string[i] = int_cast
				
		input_dict = {'lat': {'orig': split_string[0], 'dest': split_string[2]}, 
				'lon': {'orig': split_string[1], 'dest': split_string[3]}}

		return input_dict
	
	def cost_distance(self, e):
		"""
		>>> S = Server("test.txt")
		>>> C = S.cost_distance( (276281417,276281415) )
		>>> C
		85.05292469985967
		>>> S = Server("edmonton-roads-digraph.txt")
		"""
		for (start, stop, cost) in self.edges:
			if start == e[0] and stop == e[1]:
				return cost


	def get_route(self, in_str):
		"""
		Primary server function, what should be called on every input
		>>> S = Server("edmonton-roads-digraph.txt")
		>>> S.get_route("5365488 -11333914 5364727 -11335890")
		314088878

		"""
		input_dict = self._parse_input(in_str)
		vertex_id = get_vertex_id(self.vertices, input_dict['lat']['orig'], input_dict['lon']['orig'])
		return vertex_id

		#least_cost_path(input_dict['lat']['orig'], input_dict['lon']['orig'],
		#		input_dict['lat']['dest'], input_dict['lon']['dest'])

def get_vertex_id(vertex_dict, lat, lon):
	"""

	"""
	for id, value in vertex_dict.items():
		if lat in value and lon in value:
			return id

if __name__ == "__main__":
	import doctest
	doctest.testmod()
