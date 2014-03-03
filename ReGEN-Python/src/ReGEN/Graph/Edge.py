"""
 A Class Representing an Edge in a Directed Graph
 
 Author: Ben Kybartas
 Student ID: 260477933
 Date: August 17, 2012
"""

from Condition import Condition
class Edge:

	"""The initialization function
	
	Args:
		name (str): The name of our edge
		
	Kwargs:
		from_node (Node): The node from which the edge originates
		to_node (Node): The node to which the edge points
	"""
	def __init__(self, name, from_node=None, to_node=None):
		
		self._name = name
		self._from_node = from_node
		self._to_node = to_node

#--------------------------------------------------------------
#	Getters
#--------------------------------------------------------------

	"""Get the name of our edge

	Returns:
		(str): The name of the edge
	"""
	def get_name(self):
		return self._name
	
	"""Get the key
	"""
	def get_key(self):
		if len(self._name.keys()) > 0:
			return self._name.keys()[0]
		else:
			return None
			
	"""Get the value
	"""
	def get_value(self):
		if len(self._name.keys()) > 0:
			return self._name[self._name.keys()[0]]
		else:
			return None
		
	"""Get our from node

	Returns:
		(Node): The node from which the edge originates
	"""
	def get_from_node(self):
		return self._from_node
		
	"""Get our to node

	Returns:
		(Node): The node to which the edge points
	"""
	def get_to_node(self):
		return self._to_node
		
#--------------------------------------------------------------
#	Setters
#--------------------------------------------------------------
	
	"""Set the name of our edge

	Args:
		new_name(str): The new name of the edge
	"""
	def set_name(self, new_name):
		self._name = new_name	

	"""Set our from node

	Args:
		new_from_node(Node): The new node from which the edge originates
	"""
	def set_from_node(self, new_from_node):
		self._from_node = new_from_node	
		
	"""Set our from node

	Args:
		new_to_node(Node): The new node to which the edge points
	"""
	def set_to_node(self, new_to_node):
		self._to_node = new_to_node	
		
#--------------------------------------------------------------
#	Functions
#--------------------------------------------------------------
	
	"""See if the names of two edges are equivalent
	
	Args:
		name (Dictionary): The name to check for equality
	"""
	def name_equals(self, name):
		
		equals = True
		
		#Do a basic check
		for attr in self._name:
			if attr in name:
				if not (self._name[attr] == name[attr]):
					if not (self._name[attr] == "N/A" or name[attr] == "N/A"):
						equals = False
			else:
				equals = False

		return equals

	def edge_to_condition(self):
		condition = Condition(False)
		condition.set_first_object(self._from_node)
		condition.set_second_object(self._to_node)
		condition.set_key(self.get_key())
		condition.set_value(self.get_value())
		return condition
		
	def Copy(self):
		return Edge(self._name.copy())
