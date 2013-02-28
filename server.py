import digraph
from types import *
class Server:
	"""
	The server class. Works by instantiating a server object which has only
	one user-accessable member method: get_route.
	"""

	def __init__(self, graph_file):
		self.edges = digraph.edges_from_text(graph_file)
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
		
		THESE TESTS MUST BE FINISHED TODO

		>>> S = Server("test.txt")
		>>> result = S._parse_input("5365488 -11333914 5364727 -11335890")
		>>> result['lat']['orig']
		'5365488'
		>>> result['lat']['dest']
		'5364727'
		>>> result['lon']['orig']
		'-11333914'
		>>> result['lon']['dest']
		'-11335890'
		>>> S._parse_input("1114")
		Traceback (most recent call last):
			...
		Exception: You must pass in 4 inputs

		"""
		split_string = in_str.split(' ')

		if len(split_string) != 4:
			raise Exception('You must pass in 4 inputs')

		# We check if all inputs are integers by casting to an int and listening
		# for exceptions

		for i in split_string:
			try:
				i = int(i)
			except ValueError:
				raise TypeError('All inputs must be integers')

		input_dict = {'lat': {'orig': split_string[0], 'dest': split_string[2]}, 
				'lon': {'orig': split_string[1], 'dest': split_string[3]}}

		return input_dict
	
	def cost_distance(self, e):
		"""
		>>> S = Server("test.txt")
		>>> C = S.cost_distance( (276281417,276281415) )
		>>> C
		0.0008483923856308028
		"""
		for (start, stop, cost) in self.edges:
			if start == e[0] and stop == e[1]:
				return cost


	def get_route(self, in_str):
		input_dict = self._parse_input(in_str)

		least_cost_path(input_dict['lat']['orig'], input_dict['lon']['orig'],
				input_dict['lat']['dest'], input_dict['lon']['dest'])


if __name__ == "__main__":
	import doctest
	doctest.testmod()
