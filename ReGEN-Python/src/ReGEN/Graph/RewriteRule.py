"""
 A Class Representing a Rewrite Rule
 
 Author: Ben Kybartas
 Student ID: 260477933
 Date: August 17, 2012
"""

from Node import *
from Edge import *
from Graph import *

class RewriteRule:

	"""The initialization function
	
	Args:
		story_condition (Graph): The condition of the story
		social_condition (Graph): The condition of the relation graph
		story_modification (Graph): The modification to the story
		social_modification (Graph): The modification to the relation graph
	"""
	def __init__(self, story_condition, social_condition, story_modification, social_modification, name="", applyonce=False):
		self._rule_name = name
		self._story_condition = story_condition
		self._social_condition = social_condition
		self._story_modification = story_modification
		self._social_modification = social_modification
		self._applyonce = applyonce

#--------------------------------------------------------------
#	Getters
#--------------------------------------------------------------

	"""Get the story condition

	Returns:
		(Graph): The story condition graph
	"""
	def get_story_condition(self):
		return self._story_condition

	"""Get the social condition

	Returns:
		(Graph): The social condition graph
	"""
	def get_social_condition(self):
		return self._social_condition

	"""Get if we have an apply once rule
	
	Returns:
		(Bool): If we need to apply once only
	"""
	def get_apply_once(self):
		return self._applyonce
		
	"""Get the story modification

	Returns:
		(Graph): The story modification graph
	"""
	def get_story_modification(self):
		return self._story_modification

	"""Get the social modification

	Returns:
		(Graph): The social modification graph
	"""
	def get_social_modification(self):
		return self._social_modification
	
	"""Get the name
	
	Returns:
		(String): The name of the rule
	"""
	def get_name(self):
		return self._rule_name