'''
Created on 2012-11-24

@author: bkybar
'''
import xml.etree.ElementTree as ET
from src.ReGEN.Graph.SocialGraph import SocialGraph
from src.ReGEN.Graph.SocialNode import SocialNode

class XMLSocialGraphReader():
	
	#------------------------------------
	# Initialize our reader, the filename
	# is set to the default social graph
	#------------------------------------
	def __init__(self, filename):
		self._filename = filename
		
	#----------------------------------
	# Read our graph from XML
	#----------------------------------
	def readGraph(self):
		
		tree = ET.parse(self._filename)
		root = tree.getroot()
		
		#Get our graph name
		graph_name = root.attrib.get('name')
		
		#Process the nodes
		node_list = []
		for node in root.iter('node'):
			social_node_name = node.attrib['name']
			social_node_attributes = {}
			for attribute in node:
				attribute_type = attribute.attrib.get('type')
				attribute_name = attribute.attrib.get('name')
				attribute_value = attribute.find('value').text
				if attribute_type == 'bool':
					social_node_attributes[attribute_name] = (attribute_value == "True")
				elif attribute_type == 'int':
					social_node_attributes[attribute_name] = int(attribute_value)
				elif attribute_type == 'float':
					social_node_attributes[attribute_name] = float(attribute_value)
				else:
					social_node_attributes[attribute_name] = attribute_value
					
			node_list.append(SocialNode(social_node_name, social_node_attributes))
				
		#Create the Return Graph
		returnGraph = SocialGraph(graph_name, node_list)
		returnGraph.set_player(returnGraph.get_node_from_name("Player"))
		
		#Begin Making the connections
		for connection in root.iter('connection'):
			connect_from = connection.attrib.get('from')
			from_node = returnGraph.get_node_from_name(connect_from)
			
			connect_to = connection.attrib.get('to')
			to_node= returnGraph.get_node_from_name(connect_to)
			
			relation = connection.find('relation').attrib
			
			returnGraph.connect(from_node, relation, to_node)
		
		return returnGraph