"""
 A specific node within a story, inherits from Node 
 
 Author: Ben Kybartas
 Student ID: 260477933
 Date: August 17, 2012
"""

from Node import Node
from Condition import Condition
class StoryNode(Node):

	"""The initialization function
	
	Args:
		name (str): The name of the story node
		attributes (Dictionary): The attributes of the node
		target (Node): The target of the action within the node
	"""
	def __init__(self, name, attributes, target):
		
		self._name = name
		self._attributes = attributes
		self._incoming_edges = []
		self._outgoing_edges = []
		
		#For Story-Nodes only
		self._linked_to_node = None
		self._target = target
		
		self._social_modification = None
		
		#Preconditions and Postconditions of the node
		self._preconditions = []
		self._postconditions = []
		self._lostconditions = []
		
		#Flags used for our new condition based rewriting
		self._permanent_no_use = False
		self._temp_no_use = False
		self._coming_in = False
		self._going_out = False
		
		#Flags used for validation
		self._valid = True
	
	"""Get if a node is valid
	
	Returns:
		(Bool): Whether the node is valid or not
	"""
	def get_valid(self):
		return self._valid
	
	"""Set if a node is valid
	
	Args:
		valid (Boolean): The new value
	"""
	def set_valid(self, valid):
		self._valid = valid
	
	"""Get the target of the node
	
	Returns:
		(Node): The target
	"""
	def get_target(self):
		return self._target
	
	"""Set the target of the node
	
	Args:
		node (Node): The target node
	"""
	def set_target(self, node):
		self._target = node
	
	"""Get the social modification of the node
	
	Returns:
		(Graph): The modification of the graph
	"""
	def get_modification(self):
		return self._social_modification
		
	"""Set the social modification of the node
	
	Args:
		modification (Graph): The modification of the graph
	"""
	def set_modification(self, modification):
		self._social_modification = modification

	"""Get the node the story node is linked to
	
	Returns:
		(Node): The linked to node
	"""
	def get_linked_to_node(self):
		return self._linked_to_node

	"""Set the node the story node is linked to
	
	Args:
		node (Node): The linked to node
	"""
	def set_linked_to_node(self, node):
		self._linked_to_node = node

	def get_preconditions(self):
		return self._preconditions

	def set_preconditions(self, preconditions):
		self._preconditions = preconditions
		
	def add_precondition(self, precondition):
		self._preconditions.append(precondition)
	
	def add_preconditions(self, preconditions):
		self._preconditions.extend(preconditions)

	def get_postconditions(self):
		return self._postconditions

	def set_postconditions(self, postconditions):
		self._postconditions = postconditions
			
	def add_postcondition(self, postcondition):
		self._postconditions.append(postcondition)
	
	def add_postconditions(self, postconditions):
		self._postconditions.extend(postconditions)
	
	def get_lostconditions(self):
		return self._lostconditions
	
	def set_lostconditions(self, lostconditions):
		self._lostconditions = lostconditions
		
	def add_lostcondition(self, lostcondition):
		self._lostconditions.append(lostcondition)
	
	def add_lostconditions(self, lostconditions):
		self._lostconditions.extend(lostconditions)
	
	def exists_conflict(self, condition, check_against):
		for cond in check_against:
			if condition.conflicts(cond):
				return True, cond
		return False, None

	def refine(self, conditions):

		#The First step is to check and resolve conflicts between previous node's postconditions
		#and lost conditions
		for condition in conditions:
			exists, to_replace = self.exists_conflict(condition, self._lostconditions) 
			if exists:
				self._lostconditions.remove(to_replace)
				self._lostconditions.append(condition)
		
		#The second step is to check and resolve conflicts between the current node's postconditions
		#and lost conditions (we ONLY do this for numerical resolutions)
		for condition in self._postconditions:
			if type(condition.get_value()).__name__ == "int":
				exists, conflicted_conditions = self.exists_conflict(condition, self._lostconditions)
				if exists:
					condition.set_value(condition.get_value() + conflicted_conditions.get_value())
		#The last step is to prepare the postconditions to carry down by only taking unconflicting
		#conditions
		temp_postconditions = []
		for condition in conditions:
			exists, conflicted_condition = self.exists_conflict(condition, self._postconditions)
			if not exists:
				temp_postconditions.append(condition)
		
		temp_postconditions.extend(self._postconditions)
		#for condition in conditions:
			
		for edge in self._outgoing_edges:
			edge.get_to_node().refine(temp_postconditions)

	def validate(self, preconditions_to_check, valid):
		
		print "Validating Conditions for: " + self._name
		self._valid = valid and self._valid
		
		
		for pre_condition in preconditions_to_check:
			for post_condition in self._postconditions:
				if pre_condition.conflicts(post_condition):
					print "Invalid"
					print pre_condition
					print post_condition
					self._valid = False
		
		new_preconditions = []
		
		for precon in preconditions_to_check:
			
			keep = True

			for postcon in self._postconditions:
				if postcon.equals(precon):
					keep = False
			
			if keep:
				new_preconditions.append(precon)
				
		new_preconditions.extend(self._preconditions)
		
		for edge in self._incoming_edges:
			edge.get_from_node().validate(new_preconditions, self._valid == True)
			
	def Copy_Story_Node(self):
		new_node = StoryNode(self._name[:], self._attributes.copy(), self._target)
		new_node.set_modification(self._social_modification)
		new_node.set_linked_to_node(self._linked_to_node)
		new_node.add_attribute("Target", self._linked_to_node)
		return new_node
