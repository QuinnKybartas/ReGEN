"""
 Represents either a pre or post-condition within a story that
 can be compared for metric analysis
 
 Author: Ben Kybartas
 Student ID: 260477933
 Date: August 28, 2012
"""

class Condition():
	
	"""Initialization Function
	
	Args:
		is_attribute(Boolean):  True if we are dealing with an attribute condition
								False if we are dealing with an edge condition
	"""
	def __init__(self, is_attribute, is_comparator=False, comparator=None):
		
		self._is_attribute = is_attribute
		
		self._is_comparator = is_comparator
		self._comparator = comparator
		
		self._first_object = None
		self._second_object = None

		self._key = None
		self._value = None

	"""Pretty printing
	"""
	def __str__(self):
		text = self._first_object.get_name() + "_" + self._key + "_"
		
		if self._is_comparator:
			text += self._comparator + "_"
		
		text += str(self._value)
		
		if not self._is_attribute:
			text += "_" + self._second_object.get_name()
		
		return text

	#---------------------------------------------------
	# Getters
	#---------------------------------------------------
	"""Check if an attribute
	
	Returns:
		(Boolean): True if an attribute
	"""
	def is_attribute(self):
		return self._is_attribute

	"""Check if using a comparator
	
	Returns:
		(Boolean): True if using comparator
	"""
	def is_comparator(self):
		return self._is_comparator
		
	"""If using comparator, use this
	function to compare
	
	Returns:
		(Boolean): True if compares correctly
	"""
	def compare(self, value1, value2):
		if self._comparator == ">":
			return (value1 > value2)
		elif self._comparator == "<":
			return (value1 < value2)
		elif self._comparator == "=":
			return (value1 == value2)
		elif self._comparator == "!=":
			return (not value1 == value2)
		return None

	"""If using comparator, use this
	function to compare to self
	
	Returns:
		(Boolean): True if compares correctly
	"""	
	def compare_against_self(self, value):
		if self._comparator == ">":
			return (value > self._value)
		elif self._comparator == "<":
			return (value < self._value)
		elif self._comparator == "=":
			return (value == self._value)
		elif self._comparator == "!=":
			return (not value == self._value)
		return None

	"""Get the first object in the condition
	
	Returns:
		The node representing the first object
	"""
	def get_first_object(self):
		return self._first_object

	"""Get the second object in the condition, Note that
	the second object does not exist if we have an attribute condition
	
	Returns:
		(Node): The node representing the first object
	"""
	def get_second_object(self):
		return self._second_object
		
	"""Get the key of the condition
	
	Returns:
		(str): The attribute key for an attribute condition
		(str): The edge key for an edge condition
	"""
	def get_key(self):
		return self._key
	

	"""Get the value of the condition
	
	Returns:
		(str): The attribute value for an attribute condition
		(stt): The edge value for an edge condition
	"""
	def get_value(self):
		return self._value
	
	"""Get the comparator of a compare condition
	
	Returns:
		(str): The comparator
	"""
	def get_comparator(self):
		return self._comparator
	
	#---------------------------------------------------
	# Setters
	#---------------------------------------------------

	"""Set the first object in the condition
	
	Args:
		first_object(Node): The node representing the first object
	"""
	def set_first_object(self, first_object):
		self._first_object = first_object

	"""Set the second object in the condition, Note that
	the second object does not exist if we have an attribute condition
	
	Args:
		second_object(Node): The node representing the first object
	"""
	def set_second_object(self, second_object):
		self._second_object = second_object

	"""Set the key of the condition
	
	Args:
		key(str): The attribute key for an attribute condition
				  The edge key for an edge condition
	"""
	def set_key(self, key):
		self._key = key
	

	"""Set the value of the condition
	
	Args:
		key(str): The attribute value for an attribute condition
				  The edge value for an edge condition
	"""
	def set_value(self, value):
		self._value = value

	#-------------------------------------------------------
	# Compare Conditions
	#-------------------------------------------------------
	"""Returns true if two conditions are the same
	
	Args:
		other_condtion (Condition): The condition we are comparing against
	"""
	def equals(self, other_condition):
		
		#The should both either be True or False
		if not (self._is_comparator == other_condition.is_comparator()):
			return False
		
		#The Comparators should match
		if self._is_comparator:
			if not self._comparator == other_condition.get_comparator():
				return False
			
		#The first objects must be the same
		if not self._first_object.get_name() == other_condition.get_first_object().get_name():
			return False
				
		#In an edge condition, the second object must be the same
		if not self._is_attribute:
			if not self._second_object.get_name() == other_condition.get_second_object().get_name():
				return False

		#The key must be the same
		if not self._key == other_condition.get_key():
			return False	

		#The value must be the same (or one is "N/A")
		if not self._value == other_condition.get_value():
			if not ((self._value == "N/A") or (other_condition.get_value() == "N/A")):
				return False
				
		return True

	def conflicts(self, other_condition):
		
		#Check that types match
		if not self._is_attribute == other_condition.is_attribute():
			return False
		
		#Check that the comparator values march
		if not self._is_comparator == other_condition.is_comparator():
			return False
		
		#Check the first object
		if not self._first_object.get_name() == other_condition.get_first_object().get_name():
			return False
		
		#The check if we are dealing with a comparator
		if self._is_comparator:
			
			#Check that the keys match
			if not self._key == other_condition.get_key():
					return False
			
			#Perform the comparison
			if not self.compare_against_self(other_condition.get_value()):
				return True
			else:
				return False
			
		#If an edge condition, the second object must be the same
		if not self._is_attribute:
			
			#Bow before the hacks of this solution
			one_edge_exists_only = ["Lives", "Currently_In"]
			
			if not self._key in one_edge_exists_only:
				if not self._second_object.get_name() == other_condition.get_second_object().get_name():
					return False
				if self._key == other_condition.get_key():
					return False
				#If we are here, it implies that the first object, and second object are the same
				#but the key is different. Hence a conflict
				return True
			else:
				if not self._key == other_condition.get_key():
					return False
				
				if self._second_object.get_name() == other_condition.get_second_object().get_name():
					return False
				
				#If we are here, the keys are the same but the objects are different. Hence a conflict
				return True
		#If an attribute condition the key should be the same but the value different
		else:
			if not self._key == other_condition.get_key():
				return False
			
			#Lastly check the value
			if self._value == other_condition.get_value():
				return False
			
			#If we are here, it implies that the first object and key are the same but
			#the value is different. Hence a conflict
			return True
