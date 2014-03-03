from src.ReGEN.Metrics.Metrics import Metrics
from src.ReGEN.Graph.Graph import Graph
from src.ReGEN.Graph.Node import Node
from src.ReGEN.Graph.Edge import Edge
import math

class MetricAnalyzer():
	
	def __init__(self, graph_list, main_preconditions, metrics_to_analyze):
		self._graph_list = graph_list
		self._metrics_to_analyze = metrics_to_analyze
		self._main_preconditions = main_preconditions

	def get_standard_deviation(self, array, average, size):
		
		total = 0.0

		for i in array:
			total += math.pow((i - average),2)
		
		total_mean = total/size
		std_dev = math.sqrt(total_mean)
		return std_dev
		
		for i in range(int(tc)):
			total += math.pow((1 - average),2)
		
		for i in range(int(size - tc)):
			total += math.pow((0 - average), 2)
			
		total_mean = total/size
		std_dev = math.sqrt(total_mean)
		return std_dev
		
	def evaluate_final_graphs(self, graph_list):
		for graph in graph_list:
			graph.set_preconditions([])
			graph.generate_preconditions()
		
		similarity_matrix = []
		for i in range(len(graph_list)):
			similarity_matrix.append([0] * len(graph_list))
		
		for graph in range(len(graph_list)):
			total_preconditions = len(graph_list[graph].get_preconditions())
			for graph_2 in range(len(graph_list)):
				similar_preconditions = 0.0
				for pre_con in graph_list[graph].get_preconditions():
					for pre_con2 in graph_list[graph_2].get_preconditions():
						if pre_con.is_attribute() and pre_con2.is_attribute():
							if pre_con.equals(pre_con2):
								similar_preconditions += 1.0
						if (not pre_con.is_attribute()) and (not pre_con2.is_attribute()):
							if pre_con.equals(pre_con2):
								similar_preconditions += 1.0
				similarity_matrix[graph][graph_2] = similar_preconditions / total_preconditions
		
		total_vals = len(similarity_matrix) * len(similarity_matrix)
		total = 0
		for row in similarity_matrix:
			total += sum(row)
		print "\tNumber of Final Possible Social States : " + str(len(similarity_matrix))
		print "\tAverage Similarity between Final Social Graph Possibilities : " + str(total/total_vals)
		
	def go(self):
				
		total_number_of_nodes = 0
		total_number_of_edges = 0
		total_num_branches = 0
		total_longest_path = 0
		total_shortest_path = 0
		total_lowest_cost = 0
		total_highest_cost = 0
		total_fights = 0
		total_unique_node_types = 0
		total_repetitivity = 0
		total_average_length = 0
		total_average_cost = 0
		total_average_encounters = 0
		total_max_encounters = 0
		total_min_encounters = 0
		total_average_branches = 0
		total_max_branches = 0
		total_min_branches = 0
		total_average_uniqueness = 0
		total_max_uniqueness = 0
		total_min_uniqueness = 0
		total_edge_con = 0
		total_attr_con = 0

		number_of_nodes=[]
		number_of_edges=[]
		num_branches=[]
		longest_path=[]
		shortest_path=[]
		lowest_cost=[]
		highest_cost=[]
		fights=[]
		unique_node_types=[]
		repetitivity=[]
		average_length=[]
		average_cost=[]
		average_encounters=[]
		max_encounters=[]
		min_encounters=[]
		average_branches=[]
		max_branches=[]
		min_branches=[]
		average_uniqueness=[]
		max_uniqueness=[]
		min_uniqueness=[]
		edge_con=[]
		attr_con=[]
		
		all_the_nodes = {}		
		metrics = []
		
		for graph in self._graph_list:
			new_metric = Metrics(graph, self._metrics_to_analyze, self._main_preconditions)
			result = new_metric.printMetrics()
			metrics.append(result)
			
			if 'number_of_nodes' in result:
				total_number_of_nodes += result["number_of_nodes"]
				number_of_nodes.append(result["number_of_nodes"])
				
			if 'number_of_edges' in result:
				total_number_of_edges += result["number_of_edges"]
				number_of_edges.append(result["number_of_edges"])
			
			if 'num_branches' in result:
				total_num_branches += result["num_branches"]
				num_branches.append(result["num_branches"])
			
			if 'longest_path' in result:
				total_longest_path += result["longest_path"][0]
				longest_path.append(result["longest_path"][0])
			
			if 'shortest_path' in result:
				total_shortest_path += result["shortest_path"][0]
				shortest_path.append(result["shortest_path"][0])
			
			if 'highest_cost' in result:
				total_highest_cost += result["highest_cost"][0]
				highest_cost.append(result["highest_cost"][0])
			
			if 'lowest_cost' in result:
				total_lowest_cost += result["lowest_cost"][0]
				lowest_cost.append(result["lowest_cost"][0])
			
			if 'fights' in result:
				total_fights += result["fights"]
				fights.append(result["fights"])
			
			if 'unique_node_types' in result:
				total_unique_node_types += result["unique_node_types"]
				unique_node_types.append(result["unique_node_types"])
			
			if 'repetitivity' in result:
				total_repetitivity += result["repetitivity"]
				repetitivity.append(result["repetitivity"])

			if 'average_length' in result:
				total_average_length += result["average_length"]
				average_length.append(result["average_length"])
			
			if 'average_cost' in result:
				total_average_cost += result["average_cost"]
				average_cost.append(result["average_cost"])
			
			if 'average_encounters' in result:
				total_average_encounters += result["average_encounters"]
				average_encounters.append(result["average_encounters"])
			
			if 'max_encounters' in result:
				total_max_encounters += result["max_encounters"]
				max_encounters.append(result["max_encounters"])
			
			if 'min_encounters' in result:
				total_min_encounters += result["min_encounters"]
				min_encounters.append(result["min_encounters"])

			if 'average_branches' in result:
				total_average_branches += result["average_branches"]
				average_branches.append(result["average_branches"])

			if 'max_branches' in result:
				total_max_branches += result["max_branches"]
				max_branches.append(result["max_branches"])

			if 'min_branches' in result:
				total_min_branches += result["min_branches"]
				min_branches.append(result["min_branches"])

			if 'average_uniqueness' in result:
				total_average_uniqueness += result["average_uniqueness"]
				average_uniqueness.append(result["average_uniqueness"])

			if 'max_uniqueness' in result:
				total_max_uniqueness += result["max_uniqueness"]
				max_uniqueness.append(result["max_uniqueness"])

			if 'min_uniqueness' in result:
				total_min_uniqueness += result["min_uniqueness"]
				min_uniqueness.append(result["min_uniqueness"])
			
			if 'edge_preconditions' in result:
				total_edge_con += result["edge_preconditions"]
				edge_con.append(result["edge_preconditions"])
			
			if 'attr_preconditions' in result:
				total_attr_con += result["attr_preconditions"]
				attr_con.append(result["attr_preconditions"])

			if 'repetition' in result:
				for key in result["repetition"]:
					if key in all_the_nodes:
						all_the_nodes[key] += result["repetition"][key]
					else:
						all_the_nodes[key] = result["repetition"][key]

		number_of_quests = float(len(metrics))

		return_results = {}

		print "----------------------------------- AVERAGES -------------------------"
		print "\n"
	
		if 'number_of_nodes' in result:
			average_number_of_nodes = total_number_of_nodes/number_of_quests
			std_dev_number_of_nodes = self.get_standard_deviation(number_of_nodes, average_number_of_nodes, number_of_quests)
			return_results['average_number_of_nodes'] = average_number_of_nodes
			return_results['std_dev_number_of_nodes'] = std_dev_number_of_nodes
			print "\tAverage Number of Nodes : " + str(average_number_of_nodes)
			print "\tStandard Deviation Number of Nodes : " + str(std_dev_number_of_nodes)			
			print "\tTotal Number of Nodes : " + str(total_number_of_nodes)

		if 'number_of_edges' in result:
			average_number_of_edges = total_number_of_edges/number_of_quests
			std_dev_number_of_edges = self.get_standard_deviation(number_of_edges, average_number_of_edges, number_of_quests)
			return_results['average_number_of_edges'] = average_number_of_edges
			return_results['std_dev_number_of_edges'] = std_dev_number_of_edges
			print "\tAverage Number of Edges : " + str(average_number_of_edges)
			print "\tStandard Deviation Number of Edges : " + str(std_dev_number_of_edges)
			print "\tTotal Number of Edges : " + str(total_number_of_edges)

		if 'num_branches' in result:
			average_num_branches = total_num_branches/number_of_quests
			std_dev_num_branches = self.get_standard_deviation(num_branches, average_num_branches, number_of_quests)
			return_results['average_num_branches'] = average_num_branches
			return_results['std_dev_num_branches'] = std_dev_num_branches			
			print "\tAverage Number of Branches : " + str(average_num_branches)
			print "\tStandard Deviation Number of Branches : " + str(std_dev_num_branches)
			print "\tTotal Number of Branches : " + str(total_num_branches)

		if 'average_branches' in result:
			average_average_branches = total_average_branches/number_of_quests
			std_dev_average_branches = self.get_standard_deviation(average_branches, average_average_branches, number_of_quests)
			return_results['average_average_branches'] = average_average_branches
			return_results['std_dev_average_branches'] = std_dev_average_branches
			print "\tAverage Average Branches : " + str(average_average_branches)
			print "\tStandard Average Branches : " + str(std_dev_average_branches)	

		if 'max_branches' in result:
			average_max_branches = total_max_branches/number_of_quests
			std_dev_max_branches = self.get_standard_deviation(max_branches, average_max_branches, number_of_quests)
			return_results['average_max_branches'] = average_max_branches
			return_results['std_dev_max_branches'] = std_dev_max_branches
			print "\tAverage Max Branches : " + str(average_max_branches)
			print "\tStandard Deviation Max Branches : " + str(std_dev_max_branches)

		if 'min_branches' in result:
			average_min_branches = total_min_branches/number_of_quests
			std_dev_min_branches = self.get_standard_deviation(min_branches, average_min_branches, number_of_quests)
			return_results['average_min_branches'] = average_min_branches
			return_results['std_dev_min_branches'] = std_dev_min_branches
			print "\tAverage Min Branches : " + str(average_min_branches)
			print "\tStandard Deviation Min Branches : " + str(std_dev_min_branches)

		if 'average_length' in result:
			average_average_length = total_average_length/number_of_quests
			std_dev_average_length = self.get_standard_deviation(average_length, average_average_length, number_of_quests)
			return_results['average_average_length'] = average_average_length
			return_results['std_dev_average_length'] = std_dev_average_length
			print "\tAverage Average Path : " + str(average_average_length)
			print "\tStandard Deviation Average Path : " + str(std_dev_average_length)

		if 'longest_path' in result:
			average_longest_path = total_longest_path/number_of_quests
			std_dev_longest_path = self.get_standard_deviation(longest_path, average_longest_path, number_of_quests)
			return_results['average_longest_path'] = average_longest_path
			return_results['std_dev_longest_path'] = std_dev_longest_path
			print "\tAverage Longest Path : " + str(average_longest_path)
			print "\tStandard Deviation Longest Path : " + str(std_dev_longest_path)
		
		if 'shortest_path' in result:
			average_shortest_path = total_shortest_path/number_of_quests
			std_dev_shortest_path = self.get_standard_deviation(shortest_path, average_shortest_path, number_of_quests)
			return_results['average_shortest_path'] = average_shortest_path
			return_results['std_dev_shortest_path'] = std_dev_shortest_path
			print "\tAverage Shortest Path : " + str(average_shortest_path)
			print "\tStandard Deviation Shortest Path : " + str(std_dev_shortest_path)

		if 'average_cost' in result:
			average_average_cost = total_average_cost/number_of_quests
			std_dev_average_cost = self.get_standard_deviation(average_cost, average_average_cost, number_of_quests)
			return_results['average_average_cost'] = average_average_cost
			return_results['std_dev_average_cost'] = std_dev_average_cost
			print "\tAverage Average Cost : " + str(average_average_cost)
			print "\tStandard Deviation Average Cost : " + str(std_dev_average_cost)

		if 'highest_cost' in result:
			average_highest_cost = total_highest_cost/number_of_quests
			std_dev_highest_cost = self.get_standard_deviation(highest_cost, average_highest_cost, number_of_quests)
			return_results['average_highest_cost'] = average_highest_cost
			return_results['std_dev_highest_cost'] = std_dev_highest_cost
			print "\tAverage Highest Cost : " + str(average_highest_cost)
			print "\tStandard Deviation Highest Cost : " + str(std_dev_highest_cost)

		if 'lowest_cost' in result:
			average_lowest_cost = total_lowest_cost/number_of_quests
			std_dev_lowest_cost = self.get_standard_deviation(lowest_cost, average_lowest_cost, number_of_quests)
			return_results['average_lowest_cost'] = average_lowest_cost
			return_results['std_dev_lowest_cost'] = std_dev_lowest_cost
			print "\tAverage Lowest Cost : " + str(average_lowest_cost)
			print "\tStandard Deviation Lowest Cost : " + str(std_dev_lowest_cost)

		if 'fights' in result:
			average_fights = total_fights/number_of_quests
			std_dev_fights = self.get_standard_deviation(fights, average_fights, number_of_quests)
			return_results['average_fights'] = average_fights
			return_results['std_dev_fights'] = std_dev_fights
			print "\tAverage Encounters : " + str(average_fights)
			print "\tStandard Deviation Encounters : " + str(std_dev_fights)
			print "\tTotal Encounters : " + str(total_fights)

		if 'average_encounters' in result:
			average_average_encounters = total_average_encounters/number_of_quests
			std_dev_average_encounters = self.get_standard_deviation(average_encounters, average_average_encounters, number_of_quests)
			return_results['average_average_encounters'] = average_average_encounters
			return_results['std_dev_average_encounters'] = std_dev_average_encounters
			print "\tAverage Average Encounters : " + str(average_average_encounters)
			print "\tStandard Average Encounters : " + str(std_dev_average_encounters)

		if 'max_encounters' in result:
			average_max_encounters = total_max_encounters/number_of_quests
			std_dev_max_encounters = self.get_standard_deviation(max_encounters, average_max_encounters, number_of_quests)
			return_results['average_max_encounters'] = average_max_encounters
			return_results['std_dev_max_encounters'] = std_dev_max_encounters			
			print "\tAverage Max Encounters : " + str(average_max_encounters)
			print "\tStandard Deviation Max Encounters : " + str(std_dev_max_encounters)

		if 'min_encounters' in result:
			average_min_encounters = total_min_encounters/number_of_quests
			std_dev_min_encounters = self.get_standard_deviation(min_encounters, average_min_encounters, number_of_quests)
			return_results['average_min_encounters'] = average_min_encounters
			return_results['std_dev_min_encounters'] = std_dev_min_encounters			
			print "\tAverage Min Encounters : " + str(average_min_encounters)
			print "\tStandard Deviation Min Encounters : " + str(std_dev_min_encounters)
		
		if 'repetitivity' in result:
			average_repetitivity = total_repetitivity/number_of_quests
			std_dev_repetitivity = self.get_standard_deviation(repetitivity, average_repetitivity, number_of_quests)
			return_results['average_repetitivity'] = average_repetitivity
			return_results['std_dev_repetitivity'] = std_dev_repetitivity		
			print "\tAverage 'Uniqueness' : " + str(average_repetitivity)
			print "\tStandard Deviation Uniqueness : " + str(std_dev_repetitivity)
		
		if 'repetition' in result:
			unique_node_types_total = len(all_the_nodes.keys())
			repetivity = float(unique_node_types_total)/total_number_of_nodes
			return_results['repetivity'] = repetivity
			print "\tTotal Uniqueness : " + str(repetivity)

		if 'unique_node_types' in result:
			average_unique_node_types = total_unique_node_types/number_of_quests
			std_dev_unique_node_types = self.get_standard_deviation(unique_node_types, average_unique_node_types, number_of_quests)
			return_results['average_unique_node_types'] = average_unique_node_types
			return_results['std_dev_unique_node_types'] = std_dev_unique_node_types
			print "\tAverage Unique Node Types : " + str(average_unique_node_types)
			print "\tStandard Deviation Unique Node Types : " + str(std_dev_unique_node_types)
			print "\tTotal Unique Node Types : " + str(total_unique_node_types)

		if 'average_uniqueness' in result:
			average_average_uniqueness = total_average_uniqueness/number_of_quests
			std_dev_average_uniqueness = self.get_standard_deviation(average_uniqueness, average_average_uniqueness, number_of_quests)
			return_results['average_average_uniqueness'] = average_average_uniqueness
			return_results['std_dev_average_uniqueness'] = std_dev_average_uniqueness
			print "\tAverage Average Uniqueness : " + str(average_average_uniqueness)
			print "\tStandard Deviation Average Uniqueness : " + str(std_dev_average_uniqueness)

		if 'max_uniqueness' in result:
			average_max_uniqueness = total_max_uniqueness/number_of_quests
			std_dev_max_uniqueness = self.get_standard_deviation(max_uniqueness, average_max_uniqueness, number_of_quests)
			return_results['average_max_uniqueness'] = average_max_uniqueness
			return_results['std_dev_max_uniqueness'] = std_dev_max_uniqueness
			print "\tAverage Max Uniqueness : " + str(average_max_uniqueness)
			print "\tStandard Deviation Max Uniqueness : " + str(std_dev_max_uniqueness)

		if 'min_uniqueness' in result:
			average_min_uniqueness = total_min_uniqueness/number_of_quests
			std_dev_min_uniqueness = self.get_standard_deviation(min_uniqueness, average_min_uniqueness, number_of_quests)
			return_results['average_min_uniqueness'] = average_min_uniqueness
			return_results['std_dev_min_uniqueness'] = std_dev_min_uniqueness
			print "\tAverage Min Uniqueness : " + str(average_min_uniqueness)
			print "\tStandard Deviation Min Uniqueness : " + str(std_dev_min_uniqueness)

		if 'edge_preconditions' in result:
			average_edge_con = total_edge_con/number_of_quests
			std_dev_edge_con = self.get_standard_deviation(edge_con, average_edge_con, number_of_quests)
			return_results['average_edge_con'] = average_edge_con
			return_results['std_dev_edge_con'] = std_dev_edge_con
			print "\tAverage Influence of Narratives on Edge Preconditions : " + str(average_edge_con)
			print "\tStandard Deviation Influence of Narratives on Edge Preconditions : " + str(std_dev_edge_con)

		if 'attr_preconditions' in result:
			average_attr_con = total_attr_con/number_of_quests
			std_dev_attr_con = self.get_standard_deviation(attr_con, average_attr_con, number_of_quests)
			return_results['average_attr_con'] = average_attr_con
			return_results['std_dev_attr_con'] = std_dev_attr_con
			print "\tAverage Influence of Narratives on Attribute Preconditions : " + str(average_attr_con)
			print "\tStandard Deviation Influence of Narratives on Attribute Preconditions : " + str(std_dev_attr_con)

		return return_results