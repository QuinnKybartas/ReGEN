"""
 A object node within our relations graph, inherits from Node 
 
 Author: Ben Kybartas
 Student ID: 260477933
 Date: August 23, 2012
"""

from Node import *
from Condition import Condition
#This class will contain numerous modifications which occur due to story events
class SocialNode(Node):
	
	def __init__(self, name, attributes):
		
		self._name = name
		self._attributes = attributes
		self._incoming_edges = []
		self._outgoing_edges = []
		
		self._condition_only = False
		
		self._function_dict = {"murder" : SocialNode.murder,
				"die" : SocialNode.die,
				"set_other_nodes_relations" : SocialNode.set_other_nodes_relations,
				"move_player" : SocialNode.move_player,
				"move_player_to_node" : SocialNode.move_player_to_node,
				"killed_enemy" : SocialNode.killed_enemy,
				"new_owner": SocialNode.new_owner,
				"add_edge" : SocialNode.add_edge
				}
		
		self._reverse_function_dict = {str(SocialNode.murder) : "murder",
				str(SocialNode.die) : "die",
				str(SocialNode.set_other_nodes_relations) : "set_other_nodes_relations",
				str(SocialNode.move_player) : "move_player",
				str(SocialNode.move_player_to_node) : "move_player_to_node",
				str(SocialNode.killed_enemy) : "killed_enemy",
				str(SocialNode.new_owner) : "new_owner",
				str(SocialNode.add_edge) : "add_edge"}
	
	def get_name_from_function(self, function):
		return self._reverse_function_dict[str(function)]
	
	def get_function_from_name(self, function_name):
		return self._function_dict[function_name]
	
	def get_condition_only(self):
		return self._condition_only
	
	def set_condition_only(self, condition):
		self._condition_only = condition
		
	"""
	Returns:
		(Dictionary): All possible functions and values (values as keys)
	"""
	def get_function_dictionary(self):
		return self._function_dict
	
	"""
	Returns:
		(Dictionary): All possible functions and values(functions as keys)
	"""
	def get_reverse_function_dictionary(self):
		return self._reverse_function_dict
	
	"""A specific function which updates all relations according
		to the rules of a murder
		
	Args:
		murder (Array of 1 Node): The murderer of this node
		
	Returns:
		(Edge array): The removed edges
		(Edge array): The added edges
	"""
	def murder(self, murder):
		
		if not self._condition_only:
			murderer = murder[0]
			
			to_remove = self.remove_all_edges(False)		
			
			#Add the new edges based of other nodes response to the murder
			to_add = []
			
			to_add.extend(self.set_node_relations(["Loves", "Friends"], murderer, "Hates", "Murder_of_", True))
			to_add.extend(self.set_node_relations(["Hates", "Enemies"], murderer, "Friends", "Murder_of_", True))
			
			#return the removed and added 		
			return to_remove, to_add
		else:
			murderer = murder[0]
			
			pre_conditions = []
			new_conditions = []
			lost_conditions = []
			
			"""
			precondition = Condition(False)
			precondition.set_first_object(murderer)
			where = self.get_to_node_from_outgoing_edge_name({"Lives" : "N/A"})
			precondition.set_second_object(where)
			precondition.set_key("Currently_In")
			precondition.set_value("N/A")
			pre_conditions.append(precondition)
			"""
			preconditions, postconditions = self.get_node_relations(["Loves", "Friends"], murderer, "Hates", "Murder_of_", True)
			pre_conditions.extend(preconditions)
			new_conditions.extend(postconditions)
			
			preconditions, postconditions = self.get_node_relations(["Hates", "Enemies"], murderer, "Friends", "Murder_of_", True)
			pre_conditions.extend(preconditions)
			new_conditions.extend(postconditions)

			lost_conditions.extend(self.convert_all_edges_to_condition(False))
			
			return pre_conditions, new_conditions, lost_conditions
		
	"""Used if a character dies (or object is removed from world
	
	Returns:
	
		(Edge array): The removed edges
		(Edge array): The added edges
	"""
	def die(self):
		if not self._condition_only:
			to_remove = self.remove_all_edges(False)
		
			return to_remove, []
		else:
			lost_conditions = []
			lost_conditions.extend(self.convert_all_edges_to_condition(False))
			return [], [], lost_conditions

	"""Set the other nodes relations in relation to this character
	
	Args:
		method_array (Array):
			original_relations (Array): The relations to this node
			new_relation (String): The new array for those nodes
			ref_node (Node): The node we are referencing
			reason (str): The reason for the new edge

	Returns:
		(Edge array): The removed edges
		(Edge array): The added edges		
	"""
	def set_other_nodes_relations(self, method_array):
		if not self._condition_only:
			original_relations = method_array[0]
			new_relation = method_array[1]
			ref_node = method_array[2]
			reason = method_array[3]
			
			to_add = self.set_node_relations(original_relations, ref_node, new_relation, reason, True)
		
			return [], to_add
		else:
			original_relations = method_array[0]
			new_relation = method_array[1]
			ref_node = method_array[2]
			reason = method_array[3]
			
			Preconditions, Conditions = self.get_node_relations(original_relations, ref_node, new_relation, reason, True)
			return Preconditions, Conditions, []
			
	"""Move the Player
	
	Args:
		Where (Node): Where the player is moving
	
	Returns:
		(Edge array): The removed edges
		(Edge array): The added edges
	"""
	def move_player(self, where):
		if not self._condition_only:
			self.get_outgoing_edges()[0].set_to_node(where)
			
			return [], []
		else:
			lost_condition = self.get_outgoing_edges()[0].edge_to_condition()
			
			condition = Condition(False)
			condition.set_first_object(self)
			condition.set_second_object(where)
			condition.set_key(self.get_outgoing_edges()[0].get_key())
			condition.set_value(self.get_outgoing_edges()[0].get_value())
			
			return [], [condition], [lost_condition]

	"""Add an Edge
	
	Args:
		Where (Node): Where the player is moving
	
	Returns:
		(Edge array): The added edge
	"""
	def add_edge(self, method_array):
			
		to_node = method_array[0]
		key = method_array[1]
		value = method_array[2]

		if not self._condition_only:
			new_edge = Edge({key : value}, self, to_node)
			self.add_edge_special(new_edge, to_node)
			return [], [new_edge]
		
		else:
			condition = Condition(False)
			condition.set_first_object(self)
			condition.set_second_object(to_node)
			condition.set_key(key)
			condition.set_value(value)
			
			return [], [condition], []

	"""Move the Player to a specific node's location
	
	Args:
		who (Node): To whom the player is moving
	
	Returns:
		(Edge array): The removed edges
		(Edge array): The added edges
	"""
	def move_player_to_node(self, who):
		if not self._condition_only:
			who = who[0]
		
			where = who.get_to_node_from_outgoing_edge_name({"Lives" : "N/A"})
			self.get_outgoing_edges()[0].set_to_node(where)
		
			return [], []	
		else:
			who = who[0]
			where = who.get_to_node_from_outgoing_edge_name({"Lives" : "N/A"})
			
			lost_condition = self.get_outgoing_edges()[0].edge_to_condition()
			
			condition = Condition(False)
			condition.set_first_object(self)
			condition.set_second_object(where)
			condition.set_key(self.get_outgoing_edges()[0].get_key())
			condition.set_value(self.get_outgoing_edges()[0].get_value())
			
			return [], [condition], [lost_condition]
		
	"""Kill an Enemy (non-NPC character)
	
	Args:
		enemy:
			enemy (Node): The dead enemy
	Returns:
		(Edge array): The removed edges
		(Edge array): The added edges		
	"""	
	def killed_enemy(self, enemy):
		if not self._condition_only:
			enemy = enemy[0]
			if enemy.get_attributes()["number"] <= 1:
				enemy.get_attributes()["number"] = 0
				enemy.get_attributes()["type"] = "Defeated_Enemy"
			else:
				enemy.get_attributes()["number"] -= 1
			return [], []
		else:
			enemy = enemy[0]
			pre_conditions = []
			new_conditions = []
			lost_conditions = []
			
			precondition = Condition(True, True, ">")
			precondition.set_first_object(enemy)
			precondition.set_key("number")
			precondition.set_value(0)
			pre_conditions.append(precondition)
			
#			precondition2 = Condition(False)
#			precondition2.set_first_object(self)
#			where = enemy.get_to_node_from_outgoing_edge_name({"Lives" : "N/A"})
#			precondition2.set_second_object(where)
#			precondition2.set_key("Currently_In")
#			precondition2.set_value("N/A")
#			pre_conditions.append(precondition2)
			
			if enemy.get_attributes()["number"] <= 1:

				lost_conditions.append(enemy.attribute_to_comparator_condition('number'))
				lost_conditions.append(enemy.attribute_to_condition('type'))
				
				condition = Condition(True, True, "=")
				condition.set_first_object(enemy)
				condition.set_key("number")
				condition.set_value(0)
				new_conditions.append(condition)
				
				condition2 = Condition(True)
				condition2.set_first_object(enemy)
				condition2.set_key("type")
				condition2.set_value("Defeated_Enemy")
				new_conditions.append(condition2)
				
			else:
				
				lost_conditions.append(enemy.attribute_to_comparator_condition('number'))
				
				condition = Condition(True, True, "=")
				condition.set_first_object(enemy)
				condition.set_key("number")
				condition.set_value(-1)
				#condition.set_value(enemy.get_attributes()["number"] - 1)
				
				new_conditions.append(condition)
				
			return pre_conditions, new_conditions, lost_conditions		
	"""For an owned object, switch ownership
	
	Args:
		input_array:
			new_owner (Node): The new owner of the object
			status (str): The new status of the object
			own_reason (str): The reason the object is owned
	Returns:
		(Edge array): The removed edges
		(Edge array): The added edges		
	"""	
	def new_owner(self, input_array):
		if not self._condition_only:
			new_owner = input_array[0]
			status = input_array[1]
			own_reason = input_array[2]
			
			#Make the changes
			self._attributes['status'] = status
			edge  = Edge({'Owns' : own_reason}, new_owner, self)
			
			#Set up our return arrays
			to_add = [edge]
			to_remove = self.remove_all_edges(True)
			
			#Add the new edges to their respective node
			new_owner.add_outgoing_edge(edge)
			self.add_incoming_edge(edge)
			
			return to_remove, to_add
		else:
			new_owner = input_array[0]
			status = input_array[1]
			own_reason = input_array[2]
			
			pre_conditions = []
			new_conditions = []
			lost_conditions = []
			
			precondition = Condition(False)
			precondition.set_first_object(self)
			who = self.get_from_node_from_incoming_edge_name({"Owns" : "N/A"})
			where = who.get_to_node_from_outgoing_edge_name({"Lives" : "N/A"})
			precondition.set_second_object(where)
			precondition.set_key("Currently_In")
			precondition.set_value("N/A")
			pre_conditions.append(precondition)

			lost_conditions.append(self.attribute_to_condition('status'))
			lost_conditions.extend(self.convert_all_edges_to_condition(True))
			
			condition = Condition(True)
			condition.set_first_object(self)
			condition.set_key('status')
			condition.set_value(status)			
			new_conditions.append(condition)
			
			condition2 = Condition(False)
			condition2.set_first_object(new_owner)
			condition2.set_second_object(self)
			condition2.set_key('Owns')
			condition2.set_value(own_reason)	
			new_conditions.append(condition2)
			
			return pre_conditions, new_conditions, lost_conditions
	
	def give_Item(self, input_array):
		if not self._condition_only:
			print "Give item from one owner (self) to another"
			new_owner = input_array[0]
			item = input_array[1]
			own_reason = input_array[2]
			
			#Make the changes
			edge  = Edge({'Owns' : own_reason}, new_owner, item)
			
			#Set up our return arrays
			to_add = [edge]
			to_remove = item.remove_all_edges(True)
			
			#Add the new edges to their respective node
			new_owner.add_outgoing_edge(edge)
			item.add_incoming_edge(edge)
			
			return to_remove, to_add
		else:
			print "Give"
			new_owner = input_array[0]
			item = input_array[1]
			own_reason = input_array[2]
			
			pre_conditions = []
			new_conditions = []
			lost_conditions = []
			
			precondition = Condition(False)
			precondition.set_first_object(self)
			where = new_owner.get_to_node_from_outgoing_edge_name({"Lives" : "N/A"})
			precondition.set_second_object(where)
			precondition.set_key("Currently_In")
			precondition.set_value("N/A")
			pre_conditions.append(precondition)

			lost_conditions.extend(item.convert_all_edges_to_condition(True))
			
			condition2 = Condition(False)
			condition2.set_first_object(new_owner)
			condition2.set_second_object(item)
			condition2.set_key('Owns')
			condition2.set_value(own_reason)	
			new_conditions.append(condition2)
			
			return pre_conditions, new_conditions, lost_conditions
		
	def take_Item(self, input_array):
		if not self._condition_only:
			print "Receive or take an item"
			old_owner = input_array[0]
			item = input_array[1]
			own_reason = input_array[2]
			
			#Make the changes
			edge  = Edge({'Owns' : own_reason}, self, item)
			
			#Set up our return arrays
			to_add = [edge]
			to_remove = item.remove_all_edges(True)
			
			#Add the new edges to their respective node
			self.add_outgoing_edge(edge)
			item.add_incoming_edge(edge)
			
			return to_remove, to_add
		else:
			print "Receive"
			old_owner = input_array[0]
			item = input_array[1]
			own_reason = input_array[2]
			
			pre_conditions = []
			new_conditions = []
			lost_conditions = []
			
			precondition = Condition(False)
			precondition.set_first_object(self)
			where = old_owner.get_to_node_from_outgoing_edge_name({"Lives" : "N/A"})
			precondition.set_second_object(where)
			precondition.set_key("Currently_In")
			precondition.set_value("N/A")
			pre_conditions.append(precondition)

			lost_conditions.extend(item.convert_all_edges_to_condition(True))
			
			condition2 = Condition(False)
			condition2.set_first_object(self)
			condition2.set_second_object(item)
			condition2.set_key('Owns')
			condition2.set_value(own_reason)	
			new_conditions.append(condition2)
			
			return pre_conditions, new_conditions, lost_conditions
			
	def talk(self, input_array):
		if not self._condition_only:
			return [], []
		else:
			other_person = input_array[0]
			where = other_person.get_to_node_from_outgoing_edge_name({"Lives" : "N/A"})
						
			condition = Condition(False)
			condition.set_first_object(self)
			condition.set_second_object(where)
			condition.set_key("Currently_In")
			condition.set_value("N/A")
			
			print [condition], [], []
			
	"""The Copy Function
	"""
	def Copy_Social(self):
		return SocialNode(self._name[:], self._attributes.copy())
