'''
Created on 2012-11-24

@author: bkybar
'''
'''
Created on 2012-11-24

@author: bkybar
'''
import xml.etree.ElementTree as ET
from src.ReGEN.IO.XMLModificationReader import XMLModificationReader
from src.ReGEN.Graph.StoryGraph import StoryGraph
from src.ReGEN.Graph.StoryNode import StoryNode

class XMLStoryGraphReader():
    
    #------------------------------------
    # Initialize our reader, the filename
    # is set to the default social graph
    #
    # Note that we need a graph in order to set the targets
    #------------------------------------
    def __init__(self, graph, path, name):
        self._filename = path + name
        self._path = path
        self._graph = graph
        
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
            
            story_node_name = node.attrib['name']
            node_attributes = {}
            
            #Get the target
            node_target = node.find('target').text

            #Get the node type
            node_attributes['Node_Type'] = node.find('nodetype').text
              
            #Get the attributes
            for attribute in node.findall('attr'):
                attribute_type = attribute.attrib.get('type')
                attribute_name = attribute.attrib.get('name')
                attribute_value = attribute.find('value').text
                if attribute_type == 'bool':
                    node_attributes[attribute_name] = (attribute_value == "True")
                elif attribute_type == 'int':
                    node_attributes[attribute_name] = int(attribute_value)
                elif attribute_type == 'float':
                    node_attributes[attribute_name] = float(attribute_value)
                else:
                    node_attributes[attribute_name] = attribute_value
                    
            new_node = StoryNode(story_node_name, node_attributes, self._graph.get_node_from_name(node_target))
           
            if not node.attrib['modification'] == 'None':
                modification_filename = self._path + "Modifications/" + node.attrib['modification']
                modification_reader = XMLModificationReader(modification_filename)
                modification = modification_reader.readModification()        
                new_node.set_modification(modification)

            node_list.append(new_node)
            
        #Create the Return Graph
        returnGraph = StoryGraph(graph_name, node_list)
        
        #Begin Making the connections
        for connection in root.iter('connection'):
            connect_from = connection.attrib.get('from')
            from_node = returnGraph.get_node_from_name(connect_from)
            
            connect_to = connection.attrib.get('to')
            to_node= returnGraph.get_node_from_name(connect_to)
            
            relation = connection.find('relation').attrib
            
            if relation.keys()[0] == "none":
                relation = {}
                
            returnGraph.connect(from_node, relation, to_node)
        
        return returnGraph