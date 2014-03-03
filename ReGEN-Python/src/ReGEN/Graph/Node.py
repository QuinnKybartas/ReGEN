"""
 A Class Representing a Node in a Directed Graph
 
 Author: Ben Kybartas
 Student ID: 260477933
 Date: August 17, 2012
"""
from Edge import *
from Condition import Condition
class Node:
	
	"""The initialization function
	
	Args:
		name (str): The name of our node
		attributes (dict): A dictionary of our attributes, and their corresponding values

	"""
	def __init__(self, name, attributes):
		
		self._name = name
		self._attributes = attributes
		self._incoming_edges = []
		self._outgoing_edges = []

	def __str__(self):
		return self._name
#--------------------------------------------------------------
#	Getters
#--------------------------------------------------------------
	"""Get the name of our node

	Returns:
		(str): The name of the node
	"""
	def get_name(self):
		return self._name

	"""Get the incoming edges
	
	Returns:
		(Edge array): The list of incoming edges
	"""
	def get_incoming_edges(self):
		return self._incoming_edges

	"""Get the outgoing edges
	
	Returns:
		(Edge array): The list of outgoing edges
	"""
	def get_outgoing_edges(self):
		return self._outgoing_edges
		
	"""Get the attribute dictionary
	
	Returns:
		(dict): The attribute dictionary
	"""
	def get_attributes(self):
		return self._attributes
		
	"""Check the value of a given attribute
	
	Args:
		attribute_name (str): The name of the attribute we are searching for
		
	Raises:
		KeyError
	"""
	def check_attribute(self, attribute_name):
		
		return self._attributes[attribute_name]
		
	"""Get an incoming edge based off its position in the array
	
	Args:
		edge_id (array): The position of the edge we are retrieving
		
	Returns:
		The edge at position edge_id in the array
		
	Raises:
		IndexError
	"""			
	def get_incoming_edge_from_id(self, edge_id):
		return self._incoming_edges[edge_id]
		
	"""Get an outgoing edge based off its position in the array
	
	Args:
		edge_id (array): The position of the edge we are retrieving
		
	Returns:
		The edge at position edge_id in the array
		
	Raises:
		IndexError
	"""					
	def get_outgoing_edge_from_id(self, edge_id):
		return self._outgoing_edges[edge_id]

	"""Get the from node based off of the incoming edge name
	
	Args:
		edge_name (Dictionary): The attributes we are searching for
		
	Returns
		(Node): The from node, if it exists, None otherwise
	"""		
	def get_from_node_from_incoming_edge_name(self, edge_name):
		for edge in self._incoming_edges:
			if edge.name_equals(edge_name):
				return edge.get_from_node()
		return None

	"""Get the to node based off of the outgoing edge name
	
	Args:
		edge_name (Dictionary): The attributes we are searching for
		
	Returns
		(Node): The to node, if it exists, None otherwise
	"""				
	def get_to_node_from_outgoing_edge_name(self, edge_name):
		for edge in self._outgoing_edges:
			if edge.name_equals(edge_name):
				return edge.get_to_node()
		return None
	
	def get_indegree(self):
		return len(self._incoming_edges);
		
	def get_outdegree(self):
		return len(self._outgoing_edges);
		
#--------------------------------------------------------------
#	Setters
#--------------------------------------------------------------

	"""Set the name of our node

	Args:
		new_name(str): The new name of the node
	"""
	def set_name(self, new_name):
		self._name = new_name	
					
	"""Modify an Attribute to be a new value
	
	Args:
		attribute_name (str): The name of the attribute we are changing
		new_value (obj): The new value of our attribute
	"""
	def modify_attribute(self, attribute_name, new_value):
		self._attributes[attribute_name] = new_value
		
#--------------------------------------------------------------
#	Edge Additions
#--------------------------------------------------------------

	"""Add a single incoming edge
	
	Args:
		incoming_edge (Edge): The new incoming edge
	"""	
	def add_incoming_edge(self, incoming_edge):
		self._incoming_edges.append(incoming_edge)

	"""Add a single outgoing edge
	
	Args:
		outgoing_edge (Edge): The new outgoing edge
	"""			
	def add_outgoing_edge(self, outgoing_edge):
		self._outgoing_edges.append(outgoing_edge)
	
	"""Add an array of incoming edges
	
	Args:
		incoming_edges (array): An array of new incoming edges
	"""	
	def add_incoming_edge_array(self, incoming_edges):
		self._incoming_edges.extend(incoming_edges)

	"""Add an array of outgoing edges
	
	Args:
		outgoing_edges (array): An array of new outgoing edges
	"""	
	def add_outgoing_edge_array(self, outgoing_edges):
		self._outgoing_edges.extend(outgoing_edges)
		
	"""Add an Attribute to our attributes
	
	Args:
		attribute_name (str): The name of the attribute we are changing
		value (obj): The new value of our attribute
	"""
	def add_attribute(self, attribute_name, value):
		self._attributes[attribute_name] = value
		
#--------------------------------------------------------------
#	Edge Removals
#--------------------------------------------------------------

	"""Remove an outgoing edge
	
	Args:
		edge_to_remove (array): The edge to remove
		
	Raises:
		ValueError
	"""	
	def remove_outgoing_edge(self, edge_to_remove):
		self._outgoing_edges.remove(edge_to_remove)

	"""Remove an incoming edge
	
	Args:
		edge_to_remove (array): The edge to remove
		
	Raises:
		ValueError
	"""		
	def remove_incoming_edge(self, edge_to_remove):
		self._incoming_edges.remove(edge_to_remove)

#--------------------------------------------------------------
#	Check Connections
#--------------------------------------------------------------
	
	"""Check if this node is connected to another node
	
	Args:
		node (Node): The node we are checking against
		
	Returns:
		(Boolean): If we are connected or not
		(Edge): The connecting edge, if it exists, None otherwise
	"""
	def connected_to(self, node):
		edges = []
		found = False
		
		for edge in self._outgoing_edges:
			if edge.get_to_node() == node:
				found = True
				edges.append(edge)
		
		return found, edges
	
	"""Check if this node is connected to another node with a specific edge name
	
	Args:
		node (Node): The node we are checking against
		name: The name of the edge
	Returns:
		(Boolean): If we are connected or not
	"""

	def connected_to_with_name(self, node, name):
		for edge in self._outgoing_edges:
			if edge.get_to_node() == node and edge.name_equals(name):
				return True
		return False
	
	"""Check if this node is connected from another node
	
	Args:
		node (Node): The node we are checking against
		
	Returns:
		(Boolean): If we are connected or not
		(Edge): The connecting edge, if it exists, None otherwise
	"""		
	def connected_from(self, node):
		
		edges = []
		found = False
		
		for edge in self._incoming_edges:
			if edge.get_from_node() == node:
				found = True
				edges.append(edge)
				
		return found, edges
	
	"""Check if this node is connected from another node with a specific edge name
	
	Args:
		node (Node): The node we are checking against
		name: The name of the edge
	Returns:
		(Boolean): If we are connected or not
	"""

	def connected_from_with_name(self, node, name):
		for edge in self._incoming_edges:
			if edge.get_from_node() == node and edge.name_equals(name):
				return True
		return False		
#--------------------------------------------------------------
#	Functions
#--------------------------------------------------------------
	
	def add_edge_special(self, edge, other_node):

		self.add_outgoing_edge(edge)
		other_node.add_incoming_edge(edge)
		
	"""Set all nodes with a certain relation to this node to
	have a certain relation to another node
	
	Args:
		relation_input (str array): The relations to this node we are interested in
		other_node (Node): The node we are modifying
		new_relation (str): The relations the node will receive
		reason (str): The reason for this change
		incoming (Boolean): True if we are looking at incoming edges, false if outgoing
		
	Returns:
		(Edge array): The array of edges which need to be added to the graph
	"""
	def set_node_relations(self, relation_input, other_node, new_relation, reason, incoming):
		
		cause = reason + self._name
		
		if incoming:
			edges = self._incoming_edges
		else:  
			edges = self._outgoing_edges
		
		to_add = []
		
		#Update all the edges
		for edge in edges:
			attribute = edge.get_name()
			
			#If the other player liked or loved this character
			#	they should hate the murderer
			if attribute.keys()[0] in relation_input:
				
				if incoming:
					from_node = edge.get_from_node()
				else:
					from_node = edge.get_to_node()
				
				if not (from_node == other_node):
					new_edge = Edge({new_relation : cause}, from_node, other_node)
					from_node.add_outgoing_edge(new_edge)
					other_node.add_incoming_edge(new_edge)
					to_add.append(new_edge)
				
		return to_add
	
	"""Get all nodes with a certain relation to this node
	
	Args:
		relation_input (str array): The relations to this node we are interested in
		other_node (Node): The node we are modifying
		new_relation (str): The relations the node will receive
		reason (str): The reason for this change
		incoming (Boolean): True if we are looking at incoming edges, false if outgoing
		
	Returns:
		(Edge array): The array of edges which need to be added to the graph
	"""	
	def get_node_relations(self, relation_input, other_node, new_relation, reason, incoming):
		
		cause = reason + self._name
		
		if incoming:
			edges = self._incoming_edges
		else:  
			edges = self._outgoing_edges
		
		Postconditions = []
		Preconditions = []
		#Update all the edges
		for edge in edges:
			attribute = edge.get_name()
			
			#If the other player liked or loved this character
			#	they should hate the murderer
			if attribute.keys()[0] in relation_input:
				
				if incoming:
					from_node = edge.get_from_node()
				else:
					from_node = edge.get_to_node()
				
				if not (from_node == other_node):
					precondition = Condition(False)
					precondition.set_first_object(from_node)
					precondition.set_second_object(self)
					precondition.set_key(edge.get_key())
					precondition.set_value(edge.get_value())
					Preconditions.append(precondition)

					new_condition = Condition(False)
					new_condition.set_first_object(from_node)
					new_condition.set_second_object(other_node)
					new_condition.set_key(new_relation)
					new_condition.set_value(cause)
					Postconditions.append(new_condition)		
		return Preconditions, Postconditions
			
	"""Remove all incoming or outgoing edges
	
	Args:
		incoming (Boolean): True if incoming edges, false if outgoing
	
	Returns:
		(Edge array): List of edges to be removed from the graph
	"""
	def remove_all_edges(self, incoming):
		
		to_remove = []
		
		if incoming:
			for edge in self._incoming_edges:
				from_node = edge.get_from_node()
				from_node.remove_outgoing_edge(edge)
				to_remove.append(edge)
			
			self._incoming_edges = []
			
		else:
			for edge in self._outgoing_edges:
				to_node = edge.get_to_node()
				to_node.remove_incoming_edge(edge)
				to_remove.append(edge)
				
			self._outgoing_edges = []
		
		return to_remove


	"""Check if this node contains another node as a sub node
	
	Args:
		sub_node (Node): The potential sub node we are checking
		
	Returns:
		(Boolean): True if its a sub node, false otherwise
	"""
	def contains_subnode(self, sub_node):
		
		#Start by comparing the attributes
		for attr in sub_node.get_attributes():
			if attr in self._attributes:
				
				#Unless we have "N/A" as an attribute, the attributes must match
				if (not (self._attributes[attr] == "N/A" or sub_node.get_attributes()[attr] == "N/A")) and (not self._attributes[attr] == sub_node.get_attributes()[attr]):
					return False
			else:
				return False
		
		
		found_edges = []
		
		#Compare our incoming edges
		for sub_edge in sub_node.get_incoming_edges():
			has_edge = False
			for edge in self._incoming_edges:
				has_edge = has_edge or ((sub_edge.name_equals(edge.get_name())) and (not edge in found_edges)) 
				if has_edge:
					found_edges.append(edge)
					break
			if has_edge == False:
				return False
				
		found_edges = []
		
		#Finally, compare the outgoing edges
		for sub_edge in sub_node.get_outgoing_edges():
			has_edge = False
			for edge in self._outgoing_edges:
				has_edge = has_edge or ((sub_edge.name_equals(edge.get_name())) and (not edge in found_edges))
				if has_edge:
					found_edges.append(edge)
					break
			if has_edge == False:
				return False
		
		#If we passed all checks, then the node is a sub node
		return True
	
	def convert_all_edges_to_condition(self, incoming):
				
		conditions = []
		
		if incoming:
			for edge in self._incoming_edges:
				conditions.append(edge.edge_to_condition())
		else:
			for edge in self._outgoing_edges:
				conditions.append(edge.edge_to_condition())

		return conditions
		
	def attribute_to_condition(self, key):
		
		if key in self._attributes.keys():
			condition = Condition(True)
			condition.set_first_object(self)
			condition.set_key(key)
			condition.set_value(self._attributes[key])
			return condition
		else:
			return None

	def attribute_to_comparator_condition(self, key):
		
		if key in self._attributes.keys():
			condition = Condition(True, True, "=")
			condition.set_first_object(self)
			condition.set_key(key)
			condition.set_value(self._attributes[key])
			return condition
		else:
			return None
		
	def Copy(self):
		return Node(self._name[:], self._attributes.copy())
