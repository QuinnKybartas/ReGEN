"""
 A graph which represents a narrative specifically 
 
 Author: Ben Kybartas
 Student ID: 260477933
 Date: August 17, 2012
"""

from Node import *
from Edge import *
from Graph import *

class StoryGraph(Graph):

	"""Initialize the story
	"""
	def initialize(self):
		self._cast = None
		self._preconditions = []
		self._postconditions = []
			
	"""Get the starting node
	
	Returns:
		(Node): The first node in the story array
	"""
	def get_start_node(self):
		return self._nodes[0]
		
	"""Get the ending node
	
	Returns:
		(Node): The ending node in the story array
	"""
	def get_end_node(self):
		return self._nodes[1]
	
	"""Get the cast of the story graph
	
	Returns:
		(Node Array): The cast for the story
	"""
	def get_cast(self):
		return self._cast

	"""Get the preconditions
	
	Returns:
		(str Array): The preconditions of the story
	"""
	def get_preconditions(self):
		return self._preconditions
		
	"""Get the postconditions
	
	Returns:
		(str Array): The postconditions of the story
	"""
	def get_postconditions(self):
		return self._postconditions
		
	"""Set the objects for the story graph
	
	Args:
		objects(Node Array): The array of nodes in the story
	"""
	def set_cast(self, objects):
		self._cast = objects
	
	"""Set the entire precondition set for a story
	
	Args:
		preconditions: The preconditions to be added
	"""
	def set_preconditions(self, preconditions):
		self._preconditions = preconditions
	
	"""Set the entire postcondition set for a story
	
	Args:
		postconditions: The postconditions to be added
	"""
	def set_postconditions(self, postconditions):
		self._postconditions = postconditions
		
	"""Add a new precondition to the story
	
	Args:
		preconditions(str): The precondition to be added
	"""	
	def add_precondition(self, precondition):
		self._preconditions.append(precondition)

	"""Add a new postcondition to the story
	
	Args:
		postconditions(str): The postcondition to be added
	"""	
	def add_postcondition(self, postcondition):
		self._postconditions.append(postcondition)
	
	"""Add a new cast
	
	Args:
		cast(str): The cast to be added
		node(Node): The node linked to in the cast
	"""
	def add_cast(self, cast, node):
		self._cast[cast] = node
	
	"""Replace a Node with a new graph
	
	Args:
		node(Node): The node we are replacing
		new(Graph): The graph we are adding
	"""
	def replace_node_with_new(self, node, new):

		#The rule is that we connect all the incoming edges
		#of the old node to the nodes in the new graph with no incoming
		#edges
		#
		#Likewise we connect all the outgoing edges of the old node
		#with the nodes in the new graph with no outgoing edges
		old_incoming_nodes = []
		old_outgoing_nodes = []
		
		for edge in node.get_incoming_edges():
			old_incoming_nodes.append(edge.get_from_node())
			
		for edge in node.get_outgoing_edges():
			old_outgoing_nodes.append(edge.get_to_node())
			
		for new_node in new.get_nodes():
			self.add_node(new_node)

		for new_node in new.get_nodes():
			if len(new_node.get_incoming_edges()) == 0:
				for old_node in old_incoming_nodes:
					self.connect(old_node, {}, new_node)
			if len(new_node.get_outgoing_edges()) == 0:
				for old_node in old_outgoing_nodes:
					self.connect(new_node, {}, old_node)
					
		for edge in new.get_edges():
			self.add_edge(edge)
			
		self._nodes.remove(node)
		
		for edge in node.get_incoming_edges():
			self._edges.remove(edge)
		
		for edge in node.get_outgoing_edges():
			self._edges.remove(edge)
		
	"""Add a new node
	
	Args:
		node (Node): The node to be added
	"""
	def add_new_node(self, node):
		
		#Make the new node
		new_node = Node(node.get_name(), node.get_attributes())
		
		#Add the new node
		self._nodes.append(new_node)
		
		#Update the adjacency matrix
		new_adj = zeros((len(self._nodes), len(self._nodes)))
		
		for row in range(len(self._adjacency)):
			for col in range(len(self._adjacency)):
				new_adj[row][col] = self._adjacency[row][col]
		self._adjacency = new_adj
	
	"""Find a path, used for get_all_paths
	"""
	def find_path(self, node, path):
		
		path = list(path)

		for edge in node.get_outgoing_edges():
						
			other_node = edge.get_to_node()
			new_path = list(path)
			new_path.append(other_node)
			
			if len(other_node.get_outgoing_edges()) == 0:
				self._paths.append(new_path)
			else:
				self.find_path(other_node, new_path)
	
	"""Get all paths through a narrative
	"""		
	def get_all_paths(self):
			
		self._paths = []
		self.fix_graph()
		starting_nodes = []
		ending_nodes = []

		for node in self._nodes:
			if len(node.get_incoming_edges()) == 0:
				starting_nodes.append(node)

		for start in starting_nodes:
			self.find_path(start, [start])
		
		return self._paths

	"""Get if a story is valid or not
	"""
	def validate_story(self):
		
		for node in self._nodes:
			node.set_valid(True)
			
		self.get_end_node().validate([], True)
		
		return self.get_start_node().get_valid()
		
	def initialize_conditions(self):
		self.get_start_node().set_preconditions(self._preconditions)
	
	def refine_lost_conditions(self):
		
		starting_nodes = []
		
		for node in self._nodes:
			if len(node.get_incoming_edges()) == 0:
				starting_nodes.append(node)
				
		for start_node in starting_nodes:
			start_node.refine([])
		
	"""Begin the process of applying node pre/post conditions
	"""
	"""Copy a narrative
	"""
	def Copy(self):
		
		self.fix_graph()
		
		copied_nodes = []
		copied_edges = []
		
		for node in self._nodes:
			new_node = node.Copy_Story_Node()
			copied_nodes.append(new_node)
		
		for edge in self._edges:
			
			new_edge = edge.Copy()
			
			from_index = self._nodes.index(edge.get_from_node())
			new_edge.set_from_node(copied_nodes[from_index])
			copied_nodes[from_index].add_outgoing_edge(new_edge)
			
			to_index = self._nodes.index(edge.get_to_node())
			new_edge.set_to_node(copied_nodes[to_index])
			copied_nodes[to_index].add_incoming_edge(new_edge)
			
			copied_edges.append(new_edge)
		
		Story_Graph_Copy = StoryGraph(self._name[:], copied_nodes)

		for edge in copied_edges:
			Story_Graph_Copy.add_edge(edge)
			
		Story_Graph_Copy.set_preconditions(list(self._preconditions))
		Story_Graph_Copy.set_postconditions(list(self._postconditions))
		Story_Graph_Copy.set_cast(self._cast.copy())
		return Story_Graph_Copy
