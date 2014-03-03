"""
 A Directed Graph Object
 
 Author: Ben Kybartas
 Student ID: 260477933
 Date: August 17, 2012
"""

from Node import *
from Edge import *

from numpy import *
from itertools import *
import os
class Graph:
	
	"""The initialization function
	
	Args:
		name (str): The name of our graph
		
	"""
	def __init__(self, name, nodes):
		self._name = name
		self._nodes = nodes
		self._nodedictionary = {}
		self._edges = []

		self._adjacency = zeros((len(nodes), len(nodes)))
		
		self._player = None
		self.make_node_dictionary()
	
#--------------------------------------------------------------
#	Getters and Setters
#--------------------------------------------------------------

	"""Get the name of our graph

	Returns:
		(str): The name of the graph
	"""
	def get_name(self):
		return self._name
	
	"""Get the player of the graph
	
	Returns:
		(Node): Returns the player
	"""
	def get_player(self):
		return self._player

	"""Get the edges

	Returns:
		(Edge Array): The array of Edges
	"""		
	def get_edges(self):
		return self._edges

	"""Get the nodes
	
	Returns:
		(Node Array): The array of Nodes
	"""
	def get_nodes(self):
		return self._nodes

	"""Get a specific node from a given id
	
	Args:
		node_id (int): The id of the node
	
	Returns:
		(Node): The node, if it exists
	"""
	def get_node_from_id(self, node_id):
		return self._nodes[node_id]
	
	"""Get a node by its name
	
	Args:
		node_name (str): The name of the node being searched for
		
	Returns:
		(Node): The node if it exists
	"""
	def get_node_from_name(self, node_name):
		if node_name in self._nodedictionary:
			return self._nodedictionary[node_name]
		else:
			return None
		
	"""Get the adjacency of the graph

	Returns:
		(Matrix): The adjacency array
	"""
	def get_adjacency(self):
		return self._adjacency
	
	"""Get the node dictionary
	
	Returns:
		(Dictionary): The node dictionary
	"""
	def get_node_dictionary(self):
		return self._nodedictionary
	
	"""Set the name of our graph

	Args:
		new_name(str): The new name of the graph
	"""
	def set_name(self, new_name):
		self._name = new_name	
	
	"""Set the player of our graph
	
	Args:
		player (Node): The player of our graph
	"""
	def set_player(self, player):
		self._player = player

	"""Check if any nodes exist which have a specific sub_node
	
	Args:
		sub_node (Node): The node we are checking against
		
	Returns:
		(Node): The matching nodes, if any exists
	"""
	def contains_node(self, sub_node):
		
		#Set our array to be initially empty
		return_array = []
		
		#Check all nodes for any matches
		for node in self._nodes:
			if node.contains_subnode(sub_node):
				return_array.append(node)
				
		#Return the array
		return return_array

#--------------------------------------------------------------
#	Node Modifications
#--------------------------------------------------------------

	"""Set the name of a node
	
	Args:
		node (Node): The node we are updating
		new_name (str): The new name of the node
	"""
	def set_node_name(self, node, new_name):
		
		del self._nodedictionary[node.get_name()]
		self._nodedictionary[new_name] = node
		
		node.set_name(new_name)

	"""Set the attributes of a node
	
	Args:
		node (Node): The node we are modifying
		attribute_name (str): The name of the attribute we are modifying
		new_value (object): The new value of the attribute
	"""
	def set_node_attribute(self, node, attribute_name, new_value):
		num = self._nodes.index(node)
		self._nodes[num].modify_attribute(attribute_name, new_value)
	
	"""Add a new node to the graph
	
	Args:
		node (Node): The node to be added
	"""
	def add_node(self, node):
		
		#Add the node
		self._nodes.append(node)
		self._nodedictionary[node.get_name()] = node
		
		#Resize and update the adjacency graph
		self._adjacency = zeros((len(self._nodes), len(self._nodes)))
		self.update_adj()

#--------------------------------------------------------------
#	Dictionary Creation
#--------------------------------------------------------------
	
	"""We are going to make a dictionary
	of our nodes for fast lookup"""
	def make_node_dictionary(self):	
		for node in self._nodes:
			self._nodedictionary[node.get_name()] = node
			
#--------------------------------------------------------------
#	Edge Modifications
#--------------------------------------------------------------

	"""Add a new edge to the graph
	
	Args:
		edge (Edge): The edge to be added
	"""
	def add_edge(self, edge):
		self._edges.append(edge)
	
	"""Modify the name of an edge
	
	Args:
		from_node (Node): The node from which the edge emerges
		to_node (Node): The node to which the edge leads
		new_edge (str): The name of the new edge
	"""
	def modify_edge(self, from_node, to_node, new_edge):
		
		#Check if an edge exists
		exists, edge = from_node.connected_to(to_node)

		#If so, modify the name
		if exists:
			edge.set_name(new_edge)
	
	"""Delete any number of edges
		
	Args:
		edges (Edge Array): The array of edges we want removed
	"""
	def delete_edges(self, edges):
		
		#Remove the edges
		for edge in edges:
			self._edges.remove(edge)
			
		#Update the adjacency graph
		self.update_adj()
	
	"""Delete a node
	
	Args:
		node(Node): The node we want removed
	"""
	def delete_node(self, node):
		
		#Remove the outgoing edges
		for edge in node.get_outgoing_edges():
			edge.get_to_node().remove_incoming_edge(edge)
		
		#Remove the incoming edges
		for edge in node.get_incoming_edges():
			edge.get_from_node().remove_outgoing_edge(edge)
			
		#Remove the node itself
		del self._nodedictionary[node.get_name()]
		self._nodes.remove(node)
		
	"""Add any number of edges
		
	Args:
		edges (Edge Array): The array of edges we want added
	"""			
	def add_edges(self, edges):
		
		#Add the edges
		self._edges.extend(edges)
		
		#Update the adjacency graph
		self.update_adj()
		
#--------------------------------------------------------------
#	Adjacency Modifications
#--------------------------------------------------------------

	"""Set the adjacency between two nodes
	
	Args:
		from_node (Node): The node from which the adjacency is occuring
		to_node (Node): The node to which the adjacency leads
	"""
	def setAdj(self, from_node, to_node):
		i = self._nodes.index(from_node)
		j = self._nodes.index(to_node)
		self._adjacency[i][j] = 1

	"""
		Update the adjacency matrix (if new nodes or edges are added/destroyed)
	"""
	def update_adj(self):
		self._adjacency = zeros((len(self._nodes), len(self._nodes)))
		for row in range(len(self._adjacency)):
			for col in range(len(self._adjacency)):
				connected, edge = self._nodes[row].connected_to(self._nodes[col])
				if connected:
					self.setAdj(self._nodes[row], self._nodes[col])
					self.setAdj(self._nodes[col], self._nodes[row])
	"""Find a path, used for get_all_paths
	"""

#--------------------------------------------------------------
#	Find all Paths function
#--------------------------------------------------------------	
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
		
		if len(self._nodes) == 1:
			return [[self._nodes[0]]]
		for node in self._nodes:
			if len(node.get_incoming_edges()) == 0:
				starting_nodes.append(node)

		for start in starting_nodes:
			self.find_path(start, [start])
		
		return self._paths
					
#--------------------------------------------------------------
#	Connection Methods
#--------------------------------------------------------------

	"""Connect two nodes with an edge
	
	Args:
		from_node (Node): The node from which the edge is generated
		edge_name (Dictionary): The dictionary which describes the edge
		to_node (Node): The node to which the edge leads
	"""	
	def connect(self, from_node, edge_name, to_node):
		
		#Make a new edge
		new_edge = Edge(edge_name, from_node, to_node)
		
		#Update the nodes
		from_node.add_outgoing_edge(new_edge)
		to_node.add_incoming_edge(new_edge)
		
		#Update the edges array
		self._edges.append(new_edge)
		
		#Set the adjacency
		self.setAdj(from_node, to_node)
		self.setAdj(to_node, from_node)
		
	"""Double-connect two nodes with an edge
	
	Args:
		node_1 (Node): The first node
		edge_name (Dictionary): The dictionary which describes the edge
		node_2 (Node): The second node
	"""	
	def doubleconnect(self, node_1, edge_name, node_2):
		
		#Make the first edge and update
		edge_1 = Edge(edge_name, node_1, node_2)
		node_1.add_outgoing_edge(edge_1)
		node_2.add_incoming_edge(edge_1)
		self._edges.append(edge_1)
		
		#Make the second edge and update
		edge_2 = Edge(edge_name, node_2, node_1)
		node_2.add_outgoing_edge(edge_2)
		node_1.add_incoming_edge(edge_2)
		self._edges.append(edge_2)
		
		#Set the adjacencies
		self.setAdj(node_1, node_2)
		self.setAdj(node_2, node_1)

#--------------------------------------------------------------
#	Ullman Algorithm
#--------------------------------------------------------------

		
	def copy_matrix(self, matrix, copy_to):
		for row in range(self._p_a):
			for col in range(self._p_b):
				copy_to[row][col] = matrix[row][col]
				
	"""The main function for calling the ullman algorithm
	
	Args:
		s_graph (Graph): The sub graph that we want to check for isomorphism
	"""
	def contains_subgraph(self, s_graph):
		
		#Start by getting all matching graphs
		self.get_matching_graphs(s_graph)
		
		#Add our matches to a return array
		return_array = []
		
		for match in self._matches:
			new_array = []
			for row in range(self._p_a):
				for col in range(self._p_b):
					if match[row][col] == 1:
						new_array.append(self._nodes[col])
			return_array.append(new_array)
		
		#Refine our return array
		finalized_return_array = []
		
		for array in return_array:
			
			#Assume the array is good initially
			Good = True
			
			for node in range(len(array) - 1):
				
				#Check that all the connections are viable by making sure the edges correspond
				connected, edges = s_graph.get_nodes()[node].connected_to(s_graph.get_nodes()[node + 1])
				if connected:
					for edge in edges:
						if not array[node].connected_to_with_name(array[node + 1], edge.get_name()):
							Good = False
							
				connected, edges = s_graph.get_nodes()[node].connected_from(s_graph.get_nodes()[node + 1])
				if connected:
					for edge in edges:
						if not array[node].connected_from_with_name(array[node + 1], edge.get_name()):
							Good = False
			
			if len(s_graph.get_nodes()) > 1:
				#We may also need to check the last node against the first
				connected, edges = s_graph.get_nodes()[node + 1].connected_to(s_graph.get_nodes()[0])
				if connected:
					for edge in edges:
						if not array[node + 1].connected_to_with_name(array[0], edge.get_name()):
							Good = False
				connected, edges = s_graph.get_nodes()[node + 1].connected_from(s_graph.get_nodes()[0])
				if connected:
					for edge in edges:
						if not array[node + 1].connected_from_with_name(array[0], edge.get_name()):
							Good = False
			if Good:
				finalized_return_array.append(array)

		return finalized_return_array

	"""
	Get all matching graphs in a sub graph
	
	Args:
		s_graph (Graph): The sub graph we are searching for
	"""
	def get_matching_graphs(self, s_graph):
		
		#Start by getting the edges and nodes
		s_graph_edges = s_graph.get_edges()
		s_graph_nodes = s_graph.get_nodes()
		
		#Initialize our array of matches
		self._matches = []
		
		#Our rows equal the number of nodes in the sub graph
		#and our columns equal the number of nodes in the graph
		self._p_a = len(s_graph_nodes)
		self._p_b = len(self._nodes)
		self.update_adj()
		#Get our adjacency graph
		self._a = s_graph.get_adjacency()
		
		#We are going to create the M_0 graph from the ullman algorithm
		self._M = zeros((self._p_a, self._p_b))
		
		for row in range(self._p_a):
			for col in range(self._p_b):
				if (self._nodes[col].get_indegree() >= s_graph_nodes[row].get_indegree()) and (self._nodes[col].get_outdegree() >= s_graph_nodes[row].get_outdegree()) and self._nodes[col].contains_subnode(s_graph_nodes[row]):
					self._M[row][col] = 1
		
		#We know want to find all locations of all the ones in our M_0 graph
		locations = []
		
		#Make arrays for each of the rows
		for i in range(self._p_a):
			locations.append([])
			
		#Find the locations of all the ones and store them
		for row in range(self._p_a):
			for col in range(self._p_b):
				if self._M[row][col] == 1:
					locations[row].append(col)
		
		#Now we want to create arrays of all possible combinations of nodes
		possibilities = locations[0]
		
		#Get all the cartesian products
		for i in range(self._p_a - 1):
			possibilities = product(possibilities, locations[i+1])
		
		#Convert these possibilities into arrays
		#From the format given above
		arrays = []
		cur_array = -1
		
		for i in possibilities:
			arrays.append([])
			cur_array += 1
			temp = i
			for j in range(self._p_a - 1):
				arrays[cur_array].append(temp[1])
				temp = temp[0]
			arrays[cur_array].append(temp)
			arrays[cur_array].reverse()
		
		#Remove any arrays where there are two repeated nodes
		to_remove = []
		for array in arrays:
			if len(array) != len(set(array)):
				to_remove.append(array)
		
		for r_array in to_remove:
			arrays.remove(r_array)
		
		#Finally, make all these into arrays
		ullmann_arrays = []
		cur_array = -1
		
		for i in range(len(arrays)):
			ullmann_arrays.append(zeros((self._p_a, self._p_b)))
			cur_array += 1
			for row in range(len(arrays[i])):
				ullmann_arrays[cur_array][row][arrays[i][row]] = 1

		
		#Now we want to check all our arrays for potential matches
		for array in ullmann_arrays:
		
			isomorphism = True
		
			#We will use the ullmann test for isomorphism
			B = dot(array,self._adjacency)
			B = B.transpose()
		
			C = dot(array,B)
			C = C.transpose()
		
			for i in range(self._p_a):
				for j in range(self._p_a):
					if self._a[i][j] == 1:
						if not C[i][j] == 1:
							isomorphism = False
			
			#If its a match, add it to our matches list
			if isomorphism:
				iso = zeros((self._p_a, self._p_b))
				self.copy_matrix(array, iso)
				self._matches.append(iso)		

	"""Fix some wierd errors in the graph"""
	def fix_graph(self):
		for node in self._nodes:
			for edge in node.get_incoming_edges():
				if not edge.get_from_node() in self._nodes:
					node.remove_incoming_edge(edge)
			for edge in node.get_outgoing_edges():
				if not edge.get_to_node() in self._nodes:
					node.remove_outgoing_edge(edge)
	
	def fix_node_names(self):
		for node in self._nodes:
			for node_2 in self._nodes:
				if not node==node_2:
					if node.get_name() == node_2.get_name():
						node_2.set_name(node_2.get_name() + "_")
						
	def remove_unnecessary_nodes(self):
		to_remove = []
		for node in self._nodes:
			if node.get_attributes()["Node_Type"] == "Start" or node.get_attributes()["Node_Type"] == "End":
				to_remove.append(node)
		
		for node in to_remove:
			for edge in node.get_outgoing_edges():
				edge.get_to_node().remove_incoming_edge(edge)

			for edge in node.get_incoming_edges():
				edge.get_from_node().remove_outgoing_edge(edge)

			self.delete_edges(node.get_outgoing_edges())
			self.delete_edges(node.get_incoming_edges())

			self._nodes.remove(node)
			
#--------------------------------------------------------------
#	Plotting Algorithm
#--------------------------------------------------------------	
	"""Plot our graph using dot
	
	Args:
		file_name (str): The name of the output file
	"""
	def plot(self, file_name):
		output_file = open(file_name + ".dot", "w")
		output_file.write("digraph " + self._name + " {\n")
		output_file.write("\tnode [ shape = \"record\"]\n")
		
		self.fix_node_names()
		
		#Define our nodes
		for node in self._nodes:
			output_file.write("\t" + node.get_name() + " [ label = \"{ " + node.get_name() + " | ")
			
			attr = node.get_attributes()
			if not attr == None:
				for i in attr.keys():
					output_file.write(i + " = " + str(attr[i]) + "\\l")
			output_file.write(" }\" ]\n")
			
		#Write our edges
		for edge in self._edges:
			output_file.write("\t" + edge.get_from_node().get_name() + " -> " + edge.get_to_node().get_name() + " [label=\"" + str(edge.get_name()) + "\"]\n")
		output_file.write("}\n")
		output_file.close()
		
		command = "dot -Tpng " + file_name + ".dot -o " + file_name + ".png"
		os.system(command)

	"""Plot our graph using dot
	
	Args:
		file_name (str): The name of the output file
	"""
	def plot_story_graph(self, file_name):
		output_file = open(file_name + ".dot", "w")
		output_file.write("digraph " + self._name + " {\n")
		output_file.write("\tnode [ shape = \"record\"]\n")
		
		self.fix_node_names()
		
		#Define our nodes
		for node in self._nodes:
			output_file.write("\t" + node.get_name() + " [ label = \"{ " + node.get_name() + " | ")
			
			attr = node.get_attributes()
			if not attr == None:
				for i in attr.keys():
					output_file.write(i + " = " + str(attr[i]) + "\\l")
			output_file.write(" }\" ]")
			output_file.write(" [color = ivory4 style = filled fillcolor=ivory1 fontcolor=ivory4]")
			output_file.write("\n")
			
		#Write our edges
		for edge in self._edges:
			output_file.write("\t" + edge.get_from_node().get_name() + " -> " + edge.get_to_node().get_name())
			output_file.write(" [color = ivory4 fontcolor=ivory4]")
			output_file.write("\n")
		output_file.write("}\n")
		output_file.close()
		
		command = "dot -Tpng " + file_name + ".dot -o " + file_name + ".png"
		os.system(command)	

	"""Plot our graph using dot
	
	Args:
		file_name (str): The name of the output file
	"""
	def plot_social_graph(self, file_name):
		output_file = open(file_name + ".dot", "w")
		output_file.write("digraph " + self._name + " {\n")
		output_file.write("overlap=false;\n")
		#output_file.write("\tlabelloc=\"t\";\n\tlabel=\"Game World Graph for " + self._name + ".xml\";\n\tfontsize=40;\n\tfontcolor=grey45;\n")
		output_file.write("\tnode [ shape = \"record\"]\n")

		self.fix_node_names()

		#Define our nodes
		for node in self._nodes:
			output_file.write("\t" + node.get_name() + " [ label = \"{ " + node.get_name() + " | ")
			
			attr = node.get_attributes()
			if not attr == None:
				for i in attr.keys():
					output_file.write(i + " = " + str(attr[i]) + "\\l")
			output_file.write(" }\" ]")

			if not 'type' in node.get_attributes():
				output_file.write(" [color = lightblue4 style = filled fillcolor=lightblue1 fontcolor=lightblue4]")
			else:
				if node.get_attributes()['type'] == "NPC":
					output_file.write(" [color = lightblue4 style = filled fillcolor=lightblue1 fontcolor=lightblue4]")
				elif node.get_attributes()['type'] == "Location":
					output_file.write(" [color = darkseagreen4 style = filled fillcolor=darkseagreen1 fontcolor=darkseagreen4 penwidth = 2]")
				elif node.get_attributes()['type'] == "Object":
					output_file.write(" [color = coral4 style = filled fillcolor=coral1 fontcolor=coral4]")
				elif node.get_attributes()['type'] == "Player":
					output_file.write(" [color = lightpink4 style = filled fillcolor=lightpink1 fontcolor=lightpink4]")
				elif node.get_attributes()['type'] == "Enemy" or node.get_attributes()['type'] == "Boss":
					output_file.write(" [color = lightgoldenrod4 style = filled fillcolor=lightgoldenrod1 fontcolor=lightgoldenrod4]")
			
			output_file.write("\n")
		
		non_location_edges = []
		location_edges = []

		for edge in self._edges:
			if "Connects" in edge.get_name():
				location_edges.append(edge)
			else:
				non_location_edges.append(edge)

		output_file.write("\tsubgraph cluster0 {")
		output_file.write("\t\tlabel=\"Location Layout\";\n")
		output_file.write("\t\tstyle=\"filled, dotted\";\n")
		output_file.write("\t\tfillcolor=honeydew1;\n")
		output_file.write("\t\tcolor=honeydew3;\n")
		output_file.write("\t\tfontcolor=darkseagreen4;\n")
		for edge in location_edges:
			output_file.write("\t\t" + edge.get_from_node().get_name() + " -> " + edge.get_to_node().get_name() + " [label=\"" + str(edge.get_name()) + "\"]")
			output_file.write(" [color = darkseagreen4 fontcolor=darkseagreen4]")
			output_file.write("\n")
		output_file.write("\t}")

		#Write our edges
		for edge in non_location_edges:
			output_file.write("\t" + edge.get_from_node().get_name() + " -> " + edge.get_to_node().get_name() + " [label=\"" + str(edge.get_name()) + "\"]")
			if "Targets" in edge.get_name() or "Follows" in edge.get_name():
				output_file.write(" [color = lightgoldenrod4 fontcolor=lightgoldenrod4]")
			elif "Owns" in edge.get_name():
				output_file.write(" [color = coral4 fontcolor=coral4]")
			elif "Currently_In" in edge.get_name():
				output_file.write(" [color = lightpink4 fontcolor=lightpink4]")
			elif "Lives" in edge.get_name():
				output_file.write(" [color = darkseagreen4 fontcolor=darkseagreen4]")
			else:
				output_file.write(" [color = lightblue4 fontcolor=lightblue4 penwidth=2]")
			output_file.write("\n")
		output_file.write("} [pos=\"0, 0!\"]\n")
		output_file.close()
		
		command = "dot -Tpng " + file_name + ".dot -o " + file_name + ".png"
		os.system(command)

	def Copy(self):
		
		self.fix_graph()
		
		copied_nodes = []
		copied_edges = []
		
		for node in self._nodes:
			copied_nodes.append(node.Copy())
		
		for edge in self._edges:
			new_edge = edge.Copy()
			
			from_index = self._nodes.index(edge.get_from_node())
			new_edge.set_from_node(copied_nodes[from_index])
			
			to_index = self._nodes.index(edge.get_to_node())
			new_edge.set_to_node(copied_nodes[to_index])
		
			copied_edges.append(new_edge)
		
		new_graph = Graph(self._name[:], copied_nodes)
		
		for edge in copied_edges:
			new_graph.add_edge(edge)
			
		return new_graph
