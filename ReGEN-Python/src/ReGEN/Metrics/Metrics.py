from src.ReGEN.Graph.Graph import Graph
from src.ReGEN.Graph.Node import Node
from src.ReGEN.Graph.Edge import Edge

class Metrics():

	def __init__(self, graph, metrics_to_analyze, preconditions):
		self._graph = graph		
		self._att_precons = []
		self._edge_precons = []
		self._metrics_to_analyze = metrics_to_analyze

		for precon in preconditions:
			if precon.is_attribute():
				self._att_precons.append(precon)
			else:
				self._edge_precons.append(precon)		

	def getTopologicallySortedGraph(self, graph):
		node_set = graph.get_nodes()[:]
		self._sorted_set = []
	
		for node in node_set:
			node.add_attribute("visited", False)

		for node in node_set:
			self.visitNode(node)
			
		return self._sorted_set
		
	def visitNode(self, node):
		if node.get_attributes()["visited"] == False:
			node.modify_attribute("visited", True)
			for edge in node.get_incoming_edges():
				self.visitNode(edge.get_from_node())
			self._sorted_set.append(node)

	def getLongestPath(self, graph, topo_sorted):
			
		length_to = [0] * len(topo_sorted)
		longest_path = [[]] * len(topo_sorted)
		
		for node in range(len(topo_sorted)):
			for edge in range(len(graph.get_edges())):
				if graph.get_edges()[edge].get_from_node() == topo_sorted[node]:
					other_node = topo_sorted.index(graph.get_edges()[edge].get_to_node())
					if length_to[other_node] < length_to[node] + 1:
						length_to[other_node] = length_to[node] + 1
						longest_path[other_node] = longest_path[node][:]
						longest_path[other_node].append(node)
		
		final_path = []
		total_length = len(longest_path[length_to.index(max(length_to))]) + 1
		for num in longest_path[length_to.index(max(length_to))]:
			final_path.append(topo_sorted[num])
		
		final_path.append(topo_sorted[length_to.index(max(length_to))])
		
		return [total_length, final_path]
	
	def getShortestPath(self, graph, topo_sorted):
		
		Q = topo_sorted[:]
		
		starting_nodes = []
		ending_nodes = []
		
		for node in Q:
			node.add_attribute("parent", None)
			if len(node.get_outgoing_edges()) == 0:
				ending_nodes.append(node)
			if len(node.get_incoming_edges()) == 0:
				starting_nodes.append(node)
				
		distances = [float("inf")] * len(Q)
		
		for node in starting_nodes:
			distances[Q.index(node)] = 0
			
		while len(Q) > 0:
			cur_node = Q.pop(distances.index(min(distances)))
			cur_dist = distances.pop(distances.index(min(distances)))

			cur_node.add_attribute("cost", cur_dist)
			
			if cur_dist == float("inf"):
				break;
			
			for edge in cur_node.get_outgoing_edges():
				if edge.get_to_node() in Q:
					node_index = Q.index(edge.get_to_node())
					new_dist = cur_dist + 1
					if new_dist < distances[node_index]:
						distances[node_index] = new_dist
						Q[node_index].modify_attribute("parent", cur_node)
		
		cur_min = float("inf")
		min_ending = None
		for node in ending_nodes:
			
			if node.get_attributes()["cost"] < cur_min:
				cur_min = node.get_attributes()["cost"]
				min_ending = node

		final_path = []
		total_length = 0
		
		path = min_ending
		while not path == None:
			final_path.append(path)
			total_length += 1
			path = path.get_attributes()["parent"]
		
		final_path.reverse()
		return [total_length, final_path]
			
	def getLowestCost(self, graph, topo_sorted):			
		Q = topo_sorted[:]
		
		starting_nodes = []
		ending_nodes = []
		
		for node in Q:
			node.add_attribute("parent", None)
			if len(node.get_outgoing_edges()) == 0:
				ending_nodes.append(node)
			if len(node.get_incoming_edges()) == 0:
				starting_nodes.append(node)
				
		distances = [float("inf")] * len(Q)
		
		for node in starting_nodes:
			distances[Q.index(node)] = 0
			
		while len(Q) > 0:
			cur_node = Q.pop(distances.index(min(distances)))
			cur_dist = distances.pop(distances.index(min(distances)))

			cur_node.add_attribute("cost", cur_dist)
			
			if cur_dist == float("inf"):
				break;
			
			for edge in cur_node.get_outgoing_edges():
				if edge.get_to_node() in Q:
					node_index = Q.index(edge.get_to_node())
					
					if cur_node.get_attributes()["Node_Type"] == "Murder":
						new_dist = cur_dist + 1
					else:
						new_dist = cur_dist
						
					if new_dist < distances[node_index]:
						distances[node_index] = new_dist
						Q[node_index].modify_attribute("parent", cur_node)
		
		cur_min = float("inf")
		min_ending = None
		for node in ending_nodes:
			
			if node.get_attributes()["cost"] < cur_min:
				cur_min = node.get_attributes()["cost"]
				min_ending = node
		
		if min_ending.get_attributes()["Node_Type"] == "Murder":
			total_length = min_ending.get_attributes()["cost"] + 1
		else:
			total_length = min_ending.get_attributes()["cost"]

		final_path = []			
		path = min_ending
		while not path == None:
			final_path.append(path)
			path = path.get_attributes()["parent"]
		
		final_path.reverse()
		
		return [total_length, final_path]
		
	def getHighestCost(self, graph, topo_sorted):
			
		length_to = [0] * len(topo_sorted)
		longest_path = [[]] * len(topo_sorted)
		
		for node in range(len(topo_sorted)):
			for edge in range(len(graph.get_edges())):
				if graph.get_edges()[edge].get_from_node() == topo_sorted[node]:
					other_node = topo_sorted.index(graph.get_edges()[edge].get_to_node())
					
					if topo_sorted[node].get_attributes()["Node_Type"] == "Murder":
						modification = 1
					else:
						modification = 0
						
					if length_to[other_node] < length_to[node] + modification:
						length_to[other_node] = length_to[node] + modification
						longest_path[other_node] = longest_path[node][:]
						longest_path[other_node].append(node)
		
		for node in range(len(length_to)):
			if topo_sorted[node].get_attributes()["Node_Type"] == "Murder":
				length_to[node] += 1
				
		final_path = []
		total_length = max(length_to)
		for num in longest_path[length_to.index(max(length_to))]:
			final_path.append(topo_sorted[num])
		
		final_path.append(topo_sorted[length_to.index(max(length_to))])
		
		return [total_length, final_path]
	
	def number_of_unique_preconditions(self):
		
		total_attr_conds = 0.0
		total_edge_conds = 0.0
		old_attr_conds = 0.0
		old_edge_conds = 0.0

		for condition in self._graph.get_preconditions():
			if condition.is_attribute():
				total_attr_conds += 1
				for attr_cond in self._att_precons:
					if attr_cond.equals(condition):
						old_attr_conds += 1
			else:
				total_edge_conds += 1
				for edge_cond in self._edge_precons:
					if edge_cond.equals(condition):
						old_edge_conds += 1
		
		if total_edge_conds > 0:
			new_edge_conds = 1.0 - (old_edge_conds/total_edge_conds)
		else:
			new_edge_conds = 0.0
		if total_attr_conds > 0:
			new_attr_conds = 1.0 - (old_attr_conds/total_attr_conds)
		else:
			new_attr_conds = 0.0
			
		return [new_attr_conds, new_edge_conds]
			
	def getMetrics(self, num_only):
		
		metrics = {}
		
		#Fix the potential issues with the graph
		self._graph.fix_graph()
		self._graph.remove_unnecessary_nodes()
		
		results = self.number_of_unique_preconditions()

		#Path analysis
		max_branches = 0
		min_branches = 100000
		average_branches = 0.0
		
		average_cost = 0.0
		
		max_encounters = 0
		min_encounters = 100000
		average_encounters = 0.0
	
		max_uniqueness = 0
		min_uniqueness = 100000
		average_uniqueness = 0.0
			
		paths = self._graph.get_all_paths()

		if 'attr_preconditions' in self._metrics_to_analyze:
			new_attr_cond = results[0]
			metrics["attr_preconditions"] = new_attr_cond
		
		if 'edge_preconditions' in self._metrics_to_analyze:
			new_edge_cond = results[1]
			metrics["edge_preconditions"] = new_edge_cond
		
		sorted_graph = self.getTopologicallySortedGraph(self._graph)

		#Get the longest path
		if 'longest_path' in self._metrics_to_analyze:
			longest_path = self.getLongestPath(self._graph, sorted_graph)
			
			if num_only:
				metrics["longest_path"] = longest_path[0]
			else:
				metrics["longest_path"] = longest_path
		
		#Get the shortest path
		if 'shortest_path' in self._metrics_to_analyze:
			shortest_path  = self.getShortestPath(self._graph, sorted_graph)
			
			if num_only:
				metrics["shortest_path"] = shortest_path[0]
			else:
				metrics["shortest_path"] = shortest_path
		
		#Get the average path
		if 'average_path' in self._metrics_to_analyze:
			average_length = 0.0

			for path in paths:
				average_length += len(path)

			average_length = average_length / len(paths)
			metrics["average_path"] = average_length

		#Get the highest cost
		if 'highest_cost' in self._metrics_to_analyze:
			highest_cost = self.getHighestCost(self._graph, sorted_graph)
			
			if num_only:
				metrics["highest_cost"] = highest_cost[0]
			else:
				metrics["highest_cost"] = highest_cost
				
		#Get the lowest cost
		if 'lowest_cost' in self._metrics_to_analyze:
			lowest_cost = self.getLowestCost(self._graph, sorted_graph)
			metrics["lowest_cost"] = lowest_cost
		
			if num_only:
				metrics["lowest_cost"] = lowest_cost[0]
			else:
				metrics["lowest_cost"] = lowest_cost
		
		#Get the average cost
		if 'average_cost' in self._metrics_to_analyze:
			average_cost = 0.0

			for path in paths:
				path_cost = 0
				for node in path:
					if node.get_attributes()["Node_Type"] == "Murder":
						path_cost += 1					
				average_cost += path_cost
			
			average_cost = average_cost / len(paths)
			metrics['average_cost'] = average_cost

		#Get the number of nodes
		if 'number_of_nodes' in self._metrics_to_analyze:
			number_of_nodes = len(self._graph.get_nodes())
			metrics["number_of_nodes"] = number_of_nodes
		
		#Get the number of edges
		if 'number_of_edges' in self._metrics_to_analyze:
			number_of_edges = len(self._graph.get_edges())
			metrics["number_of_edges"] = number_of_edges
		
		#Get the number of branches
		if 'num_branches' in self._metrics_to_analyze:
			num_branches = 0
			for node in self._graph.get_nodes():
				if len(node.get_outgoing_edges()) > 1:
					num_branches += 1
			metrics["num_branches"] = num_branches

		#Get the per path analysis for number of branches
		if 'per_path_branch_metrics' in self._metrics_to_analyze:
			max_branches = 0
			min_branches = 100000
			average_branches = 0.0

			for path in paths:
				branches = 0

				for node in path:
					if len(node.get_outgoing_edges()) > 1:
						branches += 1

				if branches > max_branches:
					max_branches = branches
					
				if branches < min_branches:
					min_branches = branches

				average_branches += branches

			average_branches = average_branches / len(paths)

			metrics['average_branches'] = average_branches
			metrics['max_branches'] = max_branches
			metrics['min_branches'] = min_branches

		#Get the number of fights
		if 'fights' in self._metrics_to_analyze:
			fights = 0		
			for node in self._graph.get_nodes():
				if node.get_attributes()["Node_Type"] == "Fight":
					fights += 1
			metrics["fights"] = fights

		#Get the per path analysis for encounters
		if 'per_path_encounter_metrics' in self._metrics_to_analyze:
			max_encounters = 0
			min_encounters = 100000
			average_encounters = 0.0

			for path in paths:
				encounters = 0

				for node in path:
					if node.get_attributes()["Node_Type"] == "Fight":
						encounters += 1

				if encounters > max_encounters:
					max_encounters = encounters
					
				if encounters < min_encounters:
					min_encounters = encounters

				average_encounters += encounters

			average_encounters = average_encounters / len(paths)

			metrics['average_encounters'] = average_encounters
			metrics['max_encounters'] = max_encounters
			metrics['min_encounters'] = min_encounters

		if 'repetition' in self._metrics_to_analyze or 'repetitivity' in self._metrics_to_analyze:
			repetition = {}
			for node in self._graph.get_nodes():
				if node.get_attributes()["Node_Type"] in repetition.keys():
					repetition[node.get_attributes()["Node_Type"]] += 1
				else:
					repetition[node.get_attributes()["Node_Type"]] = 1
			metrics["repetition"] = repetition
		
		if 'unique_node_types' in self._metrics_to_analyze:

			unique_node_types = len(repetition.keys())
			metrics["unique_node_types"] = unique_node_types

		
		if 'repetitivity' in self._metrics_to_analyze:
			repetitivity = float(len(repetition.keys())) / len(self._graph.get_nodes())
			metrics["repetitivity"] = repetitivity

		#Get the per path analysis for encounters
		if 'per_path_uniqueness_metrics' in self._metrics_to_analyze:
			max_uniqueness = 0
			min_uniqueness = 100000
			average_uniqueness = 0.0

			for path in paths:
				repetition_path = {}

				for node in path:
					if node.get_attributes()["Node_Type"] in repetition_path.keys():
						repetition_path[node.get_attributes()["Node_Type"]] += 1
					else:
						repetition_path[node.get_attributes()["Node_Type"]] = 1

				uniqueness = float(len(repetition_path.keys())) / len(path)

				if uniqueness > max_uniqueness:
					max_uniqueness = uniqueness
					
				if uniqueness < min_uniqueness:
					min_uniqueness = uniqueness

				average_uniqueness += uniqueness

			average_uniqueness = average_uniqueness / len(paths)

			metrics['average_uniqueness'] = average_uniqueness
			metrics['max_uniqueness'] = max_uniqueness
			metrics['min_uniqueness'] = min_uniqueness

		return metrics
		
	def printMetrics(self):
		
		metrics = self.getMetrics(False)
		
		print "----------------------- Metrics --------------------\n"		
		
		if 'unique_node_types' in metrics:
			print "\tNumber of Unique Node Types: " + str(metrics['unique_node_types'])
		
		if 'repetitivity' in metrics:
			print "\tUnique Node Types vs. Total Number of Nodes: " + str(metrics['repetitivity'])
		
		if 'number_of_nodes' in metrics:
			print "\tLength of Story (Number of Nodes): " + str(metrics['number_of_nodes'])
		
		if 'number_of_edges' in metrics:	
			print "\tNumber of Edges: " + str(metrics['number_of_edges']) + "\n"
		
		if 'num_branches' in metrics:
			print "\tNumber of Branches: " + str(metrics['num_branches'])  
		
		if 'per_path_branch_metrics' in self._metrics_to_analyze:
			print "\tAverage Number of Branches: " + str(metrics['average_branches'])
			print "\tMaximum Number of Branches: " + str(metrics['max_branches'])
			print "\tMinimum Number of Branches: " + str(metrics['min_branches']) + "\n"

		if 'average_path' in metrics:
			print "\tAverage Path Length: " + str(metrics['average_path']) + "\n"

		if 'shortest_path' in metrics:	
			print "\t\tShortest Path Length: " + str(metrics['shortest_path'][0]) + "\n"
			print "\t\t\tShortest Path: \n"
			for node in metrics['shortest_path'][1]:
				print "\t\t\t\t" + node.get_name()
			print "\n"
		
		if 'longest_path' in metrics:
			print "\t\tLongest Path Length: " + str(metrics['longest_path'][0]) + "\n"
			print "\t\t\tLongest Path: \n"
			for node in metrics['longest_path'][1]:
				print "\t\t\t\t" + node.get_name()
			print "\n"
		
		if 'average_cost' in metrics:
			print "\tAverage Cost of Story: " + str(metrics['average_cost']) + "\n"

		if 'highest_cost' in metrics:
			print "\tMaximum Cost of Story: " + str(metrics['highest_cost'][0]) + "\n"
			print "\t\tPath Segment with Maximum Cost: \n" 
			for node in metrics['highest_cost'][1]:
				print "\t\t\t\t" + node.get_name()
			print "\n"
		
		if 'lowest_cost' in metrics:
			print "\tLowest Cost of Story: " + str(metrics['lowest_cost'][0]) + "\n"
			print "\t\tPath with Lowest Cost: \n" 
			for node in metrics['lowest_cost'][1]:
				print "\t\t\t\t" + node.get_name()
			print "\n"
		
		if 'fights' in metrics:
			print "\tEncounters in Quest: " + str(metrics['fights']) + "\n"	

		if 'per_path_encounter_metrics' in self._metrics_to_analyze:
			print "\tAverage Number of Encounters: " + str(metrics['average_encounters'])
			print "\tMaximum Number of Encounters: " + str(metrics['max_encounters'])
			print "\tMinimum Number of Encounters: " + str(metrics['min_encounters']) + "\n"	

		if 'repetition' in metrics:
			print "\tNode Types and their occurence: "
			for key in metrics['repetition'].keys():
				print ""
				print "\t\tNode Type : " + key
				print "\t\tNumber of Occurences : " + str(metrics['repetition'][key])

		if 'per_path_uniqueness_metrics' in self._metrics_to_analyze:
			print "\tAverage Number of Uniqueness: " + str(metrics['average_uniqueness'])
			print "\tMaximum Number of Uniqueness: " + str(metrics['max_uniqueness'])
			print "\tMinimum Number of Uniqueness: " + str(metrics['min_uniqueness']) + "\n"	

		if 'attr_preconditions' in metrics:
			print "\tPercentage of Attribute Preconditions generated by Previous Quests : " + str(metrics['attr_preconditions'])
		
		if 'edge_preconditions' in metrics:
			print "\tPercentage of Edge Preconditions generated by Previous Quests : " + str(metrics['edge_preconditions'])
			
		print "\n"
		
		return metrics

