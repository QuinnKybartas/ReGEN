"""
 The main graph showing entities and relations between entities 
 
 Author: Ben Kybartas
 Student ID: 260477933
 Date: August 17, 2012
"""

from Node import *
from SocialNode import SocialNode
from Edge import *
from Graph import *
from Condition import *

class SocialGraph(Graph):
	
	"""Our defined graph will have preconditions
	"""
	def initialize(self):
		self._preconditions = []
	
	
	"""Add a precondition to our graph
	
	Args:
		precondition (Condition): The condition to be added
	"""
	def add_precondition(self, precondition):
		self._preconditions.append(precondition)

	"""Get the preconditions for our graph
	
	Returns:
		(Condition Array): The conditions at the start of the social graph
	"""
	def get_preconditions(self):
		return self._preconditions

	def set_preconditions(self, preconditions):
		self._preconditions = preconditions
		
	"""Generate the preconditions automatically
	"""
	def generate_preconditions(self):
		
		#Generate the attribute conditions first
		for node in self._nodes:
			
			for key in node.get_attributes():
				
				condition = Condition(True)

				condition.set_first_object(node)
				condition.set_key(key)
				condition.set_value(node.get_attributes()[key])

				self._preconditions.append(condition)

		#Following this we can generate the edge conditions
		for edge in self._edges:
			
			condition = Condition(False)

			condition.set_first_object(edge.get_from_node())
			condition.set_second_object(edge.get_to_node())
			condition.set_key(edge.get_name().keys()[0])
			condition.set_value(edge.get_name()[edge.get_name().keys()[0]])

			self._preconditions.append(condition)
			
	def modify_according_to_path(self, path, story):
		self.update_cast(story)
		for node in path:
			self.modify(node.get_modification(), story)
	
	def update_cast(self, story):
		cast = story.get_cast()
		for key in cast:
			if not isinstance(cast[key], str):
				for node in self._nodes:
					if node.get_name() == cast[key].get_name():
						cast[key] = node
			else:
				for node in self._nodes:
					if node.get_name() == cast[key]:
						cast[key] = node
				 
	"""Modify the graph according to a relation modification
	
	Args:
		modification (Graph): The relation graph
	"""
	def modify(self, modification, story):
		
		#If we have a modification, we should apply it
		if not modification == None:
			for mod in modification:
				
				#If our modification is actually a function of the social node
				if mod.keys()[0] == "Method":
					method = mod["Method"]
					
					#Replace any references with the node they are referencing
					if isinstance(method["self"], dict):
						method_self = story.get_cast()[method["self"]["ref"]]
					else:
						method_self = method["self"]
					
					#We will make an argument list with our arguments, fixing any
					#references as we go
					arg_list = []
					for arg in method["args"]:
						if isinstance(arg, dict):
							arg_list.append(story.get_cast()[arg["ref"]])
						else:
							arg_list.append(arg)
					
					#Get the modified edges from the method
					new_method = method_self.get_function_from_name(str(method["name"]))

					to_remove, to_add = new_method(method_self, arg_list)
					
					#We now we want to add all new edges as postconditions to our narrative
					#for edge in to_add:
					#	condition = Condition(False)
					#	condition.set_first_object(edge.get_from_node())
					#	condition.set_second_object(edge.get_to_node())
					#	condition.set_key(edge.get_name().keys()[0])
					#	condition.set_value(edge.get_name()[edge.get_name().keys()[0]])
						
					#	story.add_postcondition(condition)

					#Remove and add the edges as necessary
					self.delete_edges(to_remove)
					self.add_edges(to_add)
					self.update_adj()
					
				#If our modification is an attribute switch
				elif mod.keys()[0] == "Attribute":
					attribute = mod["Attribute"]
					
					#Replace the name, if it is a reference
					if isinstance(attribute["name"], dict):
						attr_name = story.get_cast()[attribute["name"]["ref"]]
					else:
						attr_name = attribute["name"]

					#condition = Condition(True)
					
					#Add the condition as a postcondition to our narrative
					#condition.set_first_object(attr_name)
					#condition.set_key(attribute["key"])
					#condition.set_value(attribute["value"])
					
					#story.add_postcondition(condition)

					#Modify the attribute
					attr_name.modify_attribute(attribute["key"], attribute["value"])

				else:
					print "Modification Error"

	def make_node_postconditions(self, story):
		self.update_cast(story)
		for node in story.get_nodes():
			self.make_postcondition(node, story)	
	
	def make_postcondition(self, node, story):
		#If we have a modification, we should apply it
		
		modification = node.get_modification()

		if not modification == None:
			for mod in modification:
				
				#If our modification is actually a function of the social node
				if mod.keys()[0] == "Method":
					method = mod["Method"]
					
					#Replace any references with the node they are referencing
					if isinstance(method["self"], dict):
						method_self = story.get_cast()[method["self"]["ref"]]
					else:
						method_self = method["self"]
					
					#We will make an argument list with our arguments, fixing any
					#references as we go
					arg_list = []
					for arg in method["args"]:
						if isinstance(arg, dict):
							arg_list.append(story.get_cast()[arg["ref"]])
						else:
							arg_list.append(arg)
							
					method_self.set_condition_only(True)
					
					#Get the modified edges from the method
					new_method = method_self.get_function_from_name(str(method["name"]))

					pre_conditions, new_conditions, lost_conditions = new_method(method_self, arg_list)
					method_self.set_condition_only(False)
						
					node.add_preconditions(pre_conditions)
					node.add_postconditions(new_conditions)
					node.add_lostconditions(lost_conditions)
					
				#If our modification is an attribute switch
				elif mod.keys()[0] == "Attribute":
					attribute = mod["Attribute"]
					
					#Replace the name, if it is a reference
					if isinstance(attribute["name"], dict):
						attr_name = story.get_cast()[attribute["name"]["ref"]]
					else:
						attr_name = attribute["name"]

					condition = Condition(True)
					
					#Add the condition as a postcondition to our narrative
					condition.set_first_object(attr_name)
					condition.set_key(attribute["key"])
					condition.set_value(attribute["value"])
					
					node.add_postcondition(condition)

				else:
					print "Modification Error"

	def Copy_Social(self):
		
		self.fix_graph()
		
		copied_nodes = []
		copied_edges = []
		player_node = None
		
		for node in self._nodes:
			new_node = node.Copy_Social()
			copied_nodes.append(new_node)
			if node == self.get_player():
				player_node = new_node
				
		for edge in self._edges:
			
			new_edge = edge.Copy()
			
			from_index = self._nodes.index(edge.get_from_node())
			new_edge.set_from_node(copied_nodes[from_index])
			copied_nodes[from_index].add_outgoing_edge(new_edge)
			
			to_index = self._nodes.index(edge.get_to_node())
			new_edge.set_to_node(copied_nodes[to_index])
			copied_nodes[to_index].add_incoming_edge(new_edge)
			
			copied_edges.append(new_edge)
		
		new_graph = SocialGraph(self._name[:], copied_nodes)
		
		for edge in copied_edges:
			new_graph.add_edge(edge)
			
		new_graph.set_preconditions(list(self._preconditions))
		new_graph.set_player(player_node)
		return new_graph
