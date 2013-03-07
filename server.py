import digraph
from types import *
import math
import sys
import serial
import argparse

class Server:
	"""
	The server class. Works by instantiating a server object which has only
	one user-accessable member method: get_route.
	"""

	def __init__(self, args):
		if args.serialport:
			print("Opening serial port: %s" % args.serialport)
			self.serial_out = self.serial_in =  serial.Serial(args.serialport, 9600)
		else:
			print("No serial port.  Supply one with the -s port option")
			exit()

		if args.verbose:
			self.debug = True
		else:
			self.debug = False
		vertex_edge_tuple = digraph.graph_from_text(args.graphname)
		self.vertices = vertex_edge_tuple[0]
		self.edges = vertex_edge_tuple[1]
		self.graph = digraph.Digraph(self.edges)

	def _parse_input(self, in_str):
		"""
		Takes a space separated list of 4 inputs. Inputs must be integers

		>>> S = Server(parse_args())
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
		
		S._parse_input("17.4 ham cheese yum")
		This one gets all huffy and puffy about throwing its own exceptions
		so it's remaining commented. Manually testing reveals it behaves as 
		expected (TypeError)

		"""

		split_string = in_str.split(' ')

		if len(split_string) != 4:
			raise RuntimeError('You must pass in 4 inputs')

		# We want to change all strings to integers. If not, exceptions must be raised

		for i, value in enumerate(split_string):
			try:
				int_cast = int(value) # This will raise an exception if non-ints are passed in
			except ValueError:
				raise TypeError('All inputs must be integers')
			split_string[i] = int_cast
				
		input_dict = {'lat': {'orig': split_string[0], 'dest': split_string[2]}, 
				'lon': {'orig': split_string[1], 'dest': split_string[3]}}

		return input_dict

	
	
	def cost_distance(self, e):
		"""
		Given edge e, we will compute the cost using pythagorean theorum.

		>>> S = Server(parse_args())
		>>> C = S.cost_distance( (276281417,276281415) )
		>>> C
		85.05292469985967
		>>> S = Server("edmonton-roads-digraph.txt")
		"""
		vertex_1_lat = self.vertices[e[0]][0]
		vertex_1_lon = self.vertices[e[0]][1]
		vertex_2_lat = self.vertices[e[1]][0]
		vertex_2_lon = self.vertices[e[1]][1]

		computed_lat = math.pow( math.fabs(vertex_1_lat - vertex_2_lat), 2)
		computed_lon = math.pow( math.fabs(vertex_1_lon - vertex_2_lon), 2)
		cost = math.sqrt( computed_lat + computed_lon )
		return cost

	def send(self, serial_port, message):
		"""
		Sends a message back to the client device.
		"""
		full_message = ''.join((message, "\n"))

		(self.debug and
			print("server:" + full_message + ":") )

		reencoded = bytes(full_message, encoding='ascii')
		serial_port.write(reencoded)


	def receive(self, serial_port, timeout=None):
		"""
		Listen for a message. Attempt to timeout after a certain number of
		milliseconds.
		"""
		raw_message = serial_port.readline()

		self.debug and print("client:", raw_message, ":")

		message = raw_message.decode('ascii')

		return message.rstrip("\r\n")
	
	
	def get_route(self, in_str):
		"""
		Primary server function, what should be called on every input

		>>> S = Server(parse_args())
		>>> S.get_route("5365488 -11333914 5364727 -11335890")
		8
		5365488 -11333914
		5365238 -11334423
		5365157 -11334634
		5365035 -11335026
		5364789 -11335776
		5364774 -11335815
		5364756 -11335849
		5364727 -11335890

		>>> S.get_route("5344628 -11345124 5344596 -11345087")
		2
		5344628 -11345124
		5344596 -11345087

		HUGE ROUTE
		S.get_route("5357300 -11361627 5347078 -11341668")

		THIS ROUTE IS HUGE SO IT'S NOT RUNNING
		S.get_route("5351621 -11337271 5344647 -11357049")

		"""
		input_dict = self._parse_input(in_str)

		origin_vertex_id = get_vertex_id(self.vertices, input_dict['lat']['orig'], 
				input_dict['lon']['orig'])
		dest_vertex_id = get_vertex_id(self.vertices, input_dict['lat']['dest'],
				input_dict['lon']['dest'])

		path = digraph.least_cost_path(self.graph, origin_vertex_id, dest_vertex_id, self.cost_distance)
		

		return path
		
		
def get_vertex_id(vertex_dict, lat, lon):
	"""

	"""
	distances = { }
	for id, value in vertex_dict.items():
		computed_lat = math.pow( math.fabs(lat - value[0]), 2)
		computed_lon = math.pow( math.fabs(lon - value[1]), 2)
		cost = math.sqrt( computed_lat + computed_lon )
		distances[cost] = id
	
	return distances[min(distances)]



"""if __name__ == "__main__":
	import doctest
	doctest.testmod()"""
if __name__ == "__main__":
	def parse_args():
		"""
		Parses arguments for this program.
		Returns an object with the following members:
			args.
				 serialport -- str
				 verbose    -- bool
				 graphname  -- str
		"""

		parser = argparse.ArgumentParser(
			description='Assignment 1: Map directions.',
			epilog = 'If SERIALPORT is not specified, stdin/stdout are used.')
		parser.add_argument('-s', '--serial',
							help='path to serial port',
							dest='serialport',
							default=None)
		parser.add_argument('-v', dest='verbose',
							help='verbose',
							action='store_true')
		parser.add_argument('-g', '--graph',
							help='path to graph (DEFAULT = "edmonton-roads-2.0.1.txt")',
							dest='graphname',
							default='edmonton-roads-2.0.1.txt')
)
		return parser.parse_args()

	S = Server(parse_args())
	while True:
		in_msg = S.receive(S.serial_in)
		try:
			path = S.get_route(in_msg)
		except RuntimeError:
			continue

		if path is None:
			path_length = 0
		else:
			path_length = len(path)
		S.send(S.serial_out, path_length)
		for p in path:
			S.send(S.serial_out, str(self.vertices[p][0]) + " " + str(self.vertices[p][1]))


	"""user_in = input('Enter the four co-ordinates [quit to kill everything] \n')
	while not user_in == "quit":
		S.get_route(user_in)		
		user_in = input('Enter the four co-ordinates [quit to kill everything] \n')"""

