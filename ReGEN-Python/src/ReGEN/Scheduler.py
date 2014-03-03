"""
 The main scheduler, which finds the patterns and makes the corresponding changes 
 
 Author: Ben Kybartas
 Student ID: 260477933
 Date: August 17, 2012
"""

from src.ReGEN.Graph.Node import Node
from src.ReGEN.Graph.Edge import Edge
from src.ReGEN.Graph.Graph import Graph
from src.ReGEN.Graph.StoryGraph import StoryGraph
from src.ReGEN.Graph.StoryNode import StoryNode
from src.ReGEN.Graph.SocialGraph import SocialGraph
from src.ReGEN.Graph.Condition import Condition
from src.ReGEN.Metrics.Metrics import Metrics
from random import *
from random import choice
import time

from src.ReGEN.Metrics.Metrics import Metrics
from src.ReGEN.Metrics.MetricAnalyzer import MetricAnalyzer

import os

class Scheduler:
	
	"""The initialization function
	
	Args:
		social_graph (Graph): The main relation graph for our game
		story_initialization_rules (RewriteRule Array): The story generation rules
		rewrite_rules (RewriteRule Array): The story modification rules
	"""
	def __init__(self, social_graph, story_initialization_rules, rewrite_rules, metrics_to_optimize, max_number_of_rewrites, stats_output, verbose=True):
		self._social_graph = social_graph
		self._story_init_rules = story_initialization_rules
		self._rewrite_rules = rewrite_rules
		self._num_applications = {}
		self._verbose = verbose
		self._stats_output = stats_output
		self._divider = "--------------------------------------"
		self._valids = 0
		self._invalids = 0
		self._metrics_to_optimize = metrics_to_optimize
		
		self._metrics_to_optimize_name_only = []

		for metric in self._metrics_to_optimize:
			self._metrics_to_optimize_name_only.append(metric[0])
			
		self._use_metric_rewriting = (not len(metrics_to_optimize) == 0)

		self._max_number_of_rewrites = max_number_of_rewrites

		self._start_rewriting_time = 0
		self._end_rewriting_time = 0
		self._start_validation_time = 0
		self._end_validation_time = 0

		# Here we define a number of applications, refering to the number
		# of times each rule has been used, this allows us to 
		# set restrictions on the number of times each rule can be applied
		self.reset_num_applications()
	
	def get_valids(self):
		return self._valids

	def get_invalids(self):
		return self._invalids
#--------------------------------------------------------------
#	Functions for the Number of Applications Dictionary
#--------------------------------------------------------------

	""" Reset our number of applications dictionary
	"""
	def reset_num_applications(self):
		
		#Set all of our entries to zero, ie. no applications
		for rule in self._rewrite_rules:
			self._num_applications[rule.get_story_modification().get_name()] = 0
		
	"""Get the number of applications of a specific rule
	
	Args:
		rule (RewriteRule): The rule to be searched for in the num_applications dictionary
	"""
	def get_num_applications(self, rule):
		#Return the number of applications of that specific rule
		return self._num_applications[rule.get_story_modification().get_name()]
		
	"""Increment the number of applications of a specific rule
	
	Args:
		rule (RewriteRule): The rule we are incrementing, most likely due to its application
	"""	
	def inc_num_applications(self, rule):
		self._num_applications[rule.get_story_modification().get_name()] += 1
	
	"""Check if we are allowed to apply a specific rule
	
	Args:
		rule (RewriteRule): The rule we are checking
		
	Returns:
		(Boolean): True if we can still apply this rule
	"""
	def is_allowed(self, rule):
		
		if rule.get_apply_once():
			if self.get_num_applications(rule) > 0:
				return False
			else:
				return True
		else:
			return True
			
#--------------------------------------------------------------
#	Getters and Setters
#--------------------------------------------------------------

	"""Get our social graph
	
	Returns:
		(SocialGraph): The graph we are using
	"""
	def get_social_graph(self):
		return self._social_graph

#--------------------------------------------------------------
#	Scheduler Helper Functions
#--------------------------------------------------------------

	"""The call to make for getting all possible rules from the list of possible
	available rules
	"""
	def get_possible_rules(self, ruleset, graph):
				
		possible_rules = []
		
		#Check each of our rewrite rules
		for rule in ruleset:
			print rule.get_name()
			#Get the story condition
			if isinstance(graph, StoryGraph):
				condition = rule.get_story_condition()
			else:
				condition = rule.get_social_condition()
				
			#Get the results
			results = graph.contains_subgraph(condition)
			
			#If we have this story condition and can still rewrite, make the modification
			#if cur_node.contains_subnode(story_condition) and refinements_remaining > 0:
			if len(results) > 0:
				if self.is_allowed(rule):	
					possible_rules.append([results, rule])		
		return possible_rules
		
	"""Check the social condition for the narrative
	"""
	def get_social_results(self, chosen_rule, narrative):
		#Prepare our social condition for checking using a subgraph check
		#by assigning any of the necessary cast names to the node to refine
		#the graph search
		social_condition = chosen_rule.get_social_condition()
		
		num_matches = 0
		for node in social_condition.get_nodes():
			if node.get_name() in narrative.get_cast():
				new_name = narrative.get_cast()[node.get_name()].get_name()
				node.add_attribute("name", new_name)
				num_matches += 1

		if num_matches > 0:
			return self._social_graph.contains_subgraph(social_condition)
		else:
			return []		
		
	""" Apply a given rule to a graph
	
	Args:
		chosen_results([story_nodes, rule]): An array containing both the rule, and the corresponding story nodes
		social_results (Array): An array of possible social situations
		narrative: The narrative we are applying the rule to
	"""
	def applyRule(self, chosen_results, social_results, narrative):
		
		#Get the rule from our chosen results
		chosen_rule = chosen_results[1]

		#Get the new story nodes from our results
		resulting_story_nodes = choice(chosen_results[0])
		
		#Get the resulting story nodes for our rewrite
		result = choice(social_results)

		#Get the social condition from our rule
		social_condition = chosen_rule.get_social_condition()
		
		#Add any new cast members necessary
		for i in range(len(result)):
			if not social_condition.get_nodes()[i].get_name() in narrative.get_cast():
				narrative.add_cast(social_condition.get_nodes()[i].get_name(), result[i])
				
		story_modification = chosen_rule.get_story_modification()

		#Make our new graph
		nodes = []
		for node in story_modification.get_nodes():
			target = narrative.get_cast()[node.get_target().get_name()]
			new_node = node.Copy_Story_Node()
			new_node.set_linked_to_node(target)
			new_node.add_attribute("Target", target.get_name())
			nodes.append(new_node)

		new_graph = Graph("Temp", nodes)
		
		adj = story_modification.get_adjacency()
		for row in range(len(adj)):
			for col in range(len(adj)):
				if adj[row][col] == 1:
					adj[col][row] = 0
					new_graph.connect(nodes[row], {}, nodes[col])
		
		backup_narrative = narrative.Copy()
								
		narrative.replace_node_with_new(narrative.get_node_from_name(resulting_story_nodes[0].get_name()), new_graph)

		narrative.fix_graph()
		self._social_graph.make_node_postconditions(narrative)
		narrative.initialize_conditions()
		narrative.refine_lost_conditions()
		
		print "Validating Final Story\n"

		if self._verbose:
			print self._divider
			for node in narrative.get_nodes():
				
				print "Preconditions for " + node.get_name()
				for con in node.get_preconditions():
					print con
				print "\nPostconditions for " + node.get_name()
				for con in node.get_postconditions():
					print con
				print "\nLost Conditions for " + node.get_name()
				for con in node.get_lostconditions():
					print con	
				print "\n" + self._divider	
		
		valid = narrative.validate_story()
		if not valid:
			print "INVALID STORY"
			self._invalids += 1
			print "VALIDS = " + str(self._valids)
			print "INVALIDS = " + str(self._invalids)
			return backup_narrative
		else:
			print "VALID STORY"
			self._valids += 1
			print "VALIDS = " + str(self._valids)
			print "INVALIDS = " + str(self._invalids)
			return narrative
			
#--------------------------------------------------------------
#	Scheduler Functions
#--------------------------------------------------------------
		
	"""Initialize our narrative
	
	Returns:
		(Boolean): True if a narrative has been created, false otherwise
	"""
	
	def initialize_narrative(self):
		
		#-----------------------------------
		# Create the Beginning Narrative Format
		#-----------------------------------
				
		#Create the starting node and ending node
		start_node = StoryNode("Start_Quest", {"Node_Type" : "Start"}, "N/A")
		end_node = StoryNode("End_Quest", {"Node_Type" : "End"}, "N/A")

		#Initialize our narrative
		self._narrative = StoryGraph("New_Quest", [start_node, end_node])
		self._narrative.initialize()
		
		print "Creating Initial Narrative"
		#-----------------------------------
		#We will go throughout all our rules and find matching results
		#-----------------------------------
		print "Searching for Possible Narrative Rules..."
		matching_rules = self.get_possible_rules(self._story_init_rules, self._social_graph)

		print "Found " + str(len(matching_rules)) + " possible rules"
		if len(matching_rules) <= 0:
			print "ERROR - No Matching Rules found, No more stories may be created"
			return False
			
		#Rules for picking the matching narrative
		#At the moment it is a random choice

		if self._verbose:
			print "Found the Following Matching Initialization Rules: "
			for rule in matching_rules:
				print "\t" + rule[1].get_name()

		resultant = choice(matching_rules)
		resulting_rule = resultant[1]

		#Rules for picking the matching group
		#At the moment it is a random choice
		resulting_group = choice(resultant[0])
		#-----------------------------------
		#Now we set the cast for our narrative
		#-----------------------------------
		cast = {}
		
		#The cast is stored as a dictionary where the name in the condition narrative
		#is the key for the node it relates to
		for i in range(len(resulting_group)):
			cast[resulting_rule.get_social_condition().get_nodes()[i].get_name()] = resulting_group[i]
		
		#The player always participates in the narrative by default
		cast["Player"] = self._social_graph.get_player()
		
		self._narrative.set_cast(cast)
		
		#-----------------------------------
		#Now we set the preconditions for our narrative
		#-----------------------------------
		
		#We will convert the original social condition into a set of preconditions
		for i in range(len(resulting_group)):
			cur_node = resulting_rule.get_social_condition().get_nodes()[i]
			cur_attr = cur_node.get_attributes()
			
			#First we will create all of the attribute preconditions
			for key in cur_attr.keys():
				condition = Condition(True)
				
				condition.set_first_object(resulting_group[i])
				condition.set_key(key)
				condition.set_value(cur_attr[key])
				
				self._narrative.add_precondition(condition)
			
			#Following this, we will create all of the edge preconditions
			for edge in cur_node.get_outgoing_edges():

				condition = Condition(False)

				condition.set_first_object(resulting_group[i])
				condition.set_second_object(cast[edge.get_to_node().get_name()])
				condition.set_key(edge.get_name().keys()[0])
				condition.set_value(edge.get_name()[edge.get_name().keys()[0]])

				self._narrative.add_precondition(condition)
		
		#-----------------------------------
		#Now we construct our narrative skeleton using this modification
		#-----------------------------------
		story_modification = resulting_rule.get_story_modification()
		
		#Set up our nodes
		for node in story_modification.get_nodes():
			
			#Get the index of the story node
			index = resulting_rule.get_social_condition().get_nodes().index(node.get_target())
			
			#We can then pick the actual target from our group
			target = resulting_group[index]
			
			#Also, add the target as an attribute
			node.add_attribute("Target", target.get_name())

			#And link the story node to this target
			node.set_linked_to_node(target)
			
			#Finally, add the node to the story
			self._narrative.add_node(node)
		
		#Edges are currently empty for narratives
		for edge in story_modification.get_edges():
			self._narrative.add_edge(edge)
		
		return True

	"""The process of writing our narrative. It involves generating a narrative to write to and
	applying the set of rewrites
	
	Returns (StoryGraph): The final narrative
	"""
	def write_narrative(self):
		
		#Create the final narrative
		self._final_narrative = self._narrative.Copy()
		
		#Connect the starting and ending node where appropriate
		for cur_node in self._final_narrative.get_nodes():	
			
			#Starting Node
			if (len(cur_node.get_incoming_edges()) == 0) and (not cur_node == self._final_narrative.get_start_node()) and (not cur_node == self._final_narrative.get_end_node()):
				self._final_narrative.connect(self._final_narrative.get_start_node(), {}, cur_node)
									
			#Ending Node
			if (len(cur_node.get_outgoing_edges()) == 0) and (not cur_node == self._final_narrative.get_start_node()) and (not cur_node == self._final_narrative.get_end_node()):
				self._final_narrative.connect(cur_node, {}, self._final_narrative.get_end_node())
		
		self._social_graph.make_node_postconditions(self._final_narrative)
		self._final_narrative.initialize_conditions()
		self._final_narrative.refine_lost_conditions()
		
		print "-------------------------------------------------\n"
		for node in self._final_narrative.get_nodes():
			
			print "Preconditions for " + node.get_name()
			for con in node.get_preconditions():
				print con
			print "\nPostconditions for " + node.get_name()
			for con in node.get_postconditions():
				print con
			print "\nLost Conditions for " + node.get_name()
			for con in node.get_lostconditions():
				print con	
			print "\n-------------------------------"		
		
		#-----------------------------------
		#Begin the process of rewriting the narrative
		#-----------------------------------
		
		#Make sure we have a reset number of applications dictionary
		self.reset_num_applications()

		#This monitors if we have any rewrites possible
		can_rewrite = True
		
		#This monitors our total number of rewrites
		num_rewrites = 0
		
		#-----------------------------------
		# Start applying the rewrite rules
		#-----------------------------------
		#While we can, attempt to apply rewrite rules to the narrative
		while can_rewrite and (num_rewrites < self._max_number_of_rewrites):
			
			#Get all rules which could possibly be applied
			possible_rules = self.get_possible_rules(self._rewrite_rules, self._final_narrative)
			
			#If we have no possible rules, then we have rewritten the story as much as possible
			if len(possible_rules) > 0:
				#---------------------------
				# WIP WIP WIP
				# Here we can cycle between whether
				# we want to rewrite stories according to
				# metrics or not
				# WIP WIP WIP
				#---------------------------
				self._start_rewriting_time = time.time()
				if self._use_metric_rewriting:
					self.metric_rewrite(possible_rules, self._final_narrative)
				else:
					self.non_metric_rewrite(possible_rules, self._final_narrative)
			
			else:
				can_rewrite = False
			
			#After each iteration, update our number of rewrites
			num_rewrites += 1
		
		return self._final_narrative
			
	"""Perform a Graph Rewrite without using metrics
	"""
	def non_metric_rewrite(self, possible_rules, narrative):
		
		#Pick our rule, and its result randomly for a non metric re-write
		result_rule_pair = choice(possible_rules)
		
		#Get our chosen rule from the pair
		chosen_rule = result_rule_pair[1]
	
		#Increment that rule, since we are now applying it
		self.inc_num_applications(chosen_rule)
		
		#Get the social results for our narrative and rule
		social_results = self.get_social_results(chosen_rule, narrative)
		
		#If we have a result, apply the rule
		if len(social_results) > 0:	
			self.applyRule(result_rule_pair, social_results, narrative)

	"""Do a Metric Enhanced Rewrite
	"""
	def metric_rewrite(self, possible_rules, narrative):
		
		candidate_narratives = []
		candidate_rules = []
		
		#Check all possible rules
		for result_rule_pair in possible_rules:
			
			#Make a new candidate narrative
			candidate_narrative = narrative.Copy()
			
			#Get a new candidate rule
			candidate_rule = result_rule_pair[1]
			
			#Check if the rule has social results
			social_results = self.get_social_results(candidate_rule, candidate_narrative)
			
			#If so we have a potential narrative/rule
			if len(social_results) > 0:
				result_candidate = self.applyRule(result_rule_pair, social_results, candidate_narrative)
				candidate_narratives.append(result_candidate)
				candidate_rules.append(candidate_rule)
				
		#If we have potential rules, we can now pick the best narrative
		#based off of metrics		
		if len(candidate_narratives) > 0:
			
			#First gather all the metrics
			metric_results = []
			
			for candidate_narrative in candidate_narratives:
				metrics = Metrics(candidate_narrative.Copy(), self._metrics_to_optimize_name_only, self._social_graph.get_preconditions())
				metric_results.append(metrics.getMetrics(True))

			#Now, using these results and our weights, pick the best metric
			optimal_narrative = self.pick_optimal_narrative(metric_results)
			
			#Increment the number of applications
			self.inc_num_applications(candidate_rules[optimal_narrative])
			#Set the new narrative
			self._final_narrative = candidate_narratives[optimal_narrative]
			
	"""Used in Metric Rewrite, get optimal narrative
	"""
	def pick_optimal_narrative(self, metric_results):
		
		scores = []
		for i in metric_results:
			scores.append(0)
			
		for optimize in self._metrics_to_optimize:
			metric_name = optimize[0]
			metric_weight = optimize[1]

			results = []
			for result in metric_results:
				results.append(result[metric_name])
				
			max_value = float(max(results))
			
			for i in range(len(results)):
				if not max_value == 0:
					scores[i] += (results[i]/max_value) * metric_weight
		
		score_results, score_indices = self.sort_with_indexes(scores)
		
		final_possibilities = []
		for i in range(len(score_results)):
			if score_results[i] == max(score_results):
				final_possibilities.append(score_indices[i])
				
		optimal_narrative = choice(final_possibilities)
		return optimal_narrative
	
	def sort_with_indexes(self, data):
		sorted_data = sorted(enumerate(data), key=lambda key: key[1], reverse=True)
		indexes = range(len(data))
		indexes.sort(key=lambda key: sorted_data[key][0])
		return [i[1] for i in sorted_data], indexes