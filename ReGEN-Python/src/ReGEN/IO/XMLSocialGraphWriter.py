'''
Created on 2012-11-24

@author: bkybar
'''
import xml.etree.ElementTree as ET

class XMLSocialGraphWriter():
    
    """
    Initialize our Social Graph Writer
    """
    def __init__(self, filename, graph):
        self._filename= filename
        self._graph = graph
    
    """
    Write our graph to the file
    """
    def writeGraph(self):
        
        #Write our root head
        root = ET.Element('graph')
        root.attrib['name'] = self._graph.get_name()
        root.attrib['type'] = "Social_Graph"
        #Write our nodes
        nodes = ET.SubElement(root, 'nodes')
        for node in self._graph.get_nodes():
            new_node = ET.SubElement(nodes, 'node')
            new_node.attrib['name'] = node.get_name()
            
            for attribute in node.get_attributes():
                
                attr = ET.SubElement(new_node, 'attr')
                attr.attrib['name'] = attribute
                attr.attrib['type'] = type(node.get_attributes()[attribute]).__name__
                
                value = ET.SubElement(attr, 'value')
                value.text = str(node.get_attributes()[attribute])
        
        #Write our connections
        connections = ET.SubElement(root, 'connections')
        for edge in self._graph.get_edges():
            
            #Make the connection
            connection = ET.SubElement(connections, 'connection')
            connection.attrib['from'] = edge.get_from_node().get_name()
            connection.attrib['to'] = edge.get_to_node().get_name()
            
            #Set the relation
            relation = ET.SubElement(connection, 'relation')
            relation.attrib[edge.get_key()] = edge.get_value()
        #Write our xml to a file
        tree = ET.ElementTree(root)
        tree.write(self._filename + ".xml")
