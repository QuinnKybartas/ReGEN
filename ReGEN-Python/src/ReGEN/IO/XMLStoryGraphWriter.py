'''
Created on 2012-11-24

@author: bkybar
'''
import xml.etree.ElementTree as ET
from src.ReGEN.IO.XMLModificationWriter import XMLModificationWriter

class XMLStoryGraphWriter():
    
    """
    Initialize our Social Graph Writer
    """
    def __init__(self, path, name, graph):
        self._filename= path + name
        self._path = path
        self._graph = graph
    
    """
    Write our graph to the file
    """
    def writeGraph(self):
        
        #Write our root head
        root = ET.Element('graph')
        root.attrib['name'] = self._graph.get_name()
        root.attrib['type'] = "Story_Graph"
        #Write our nodes
        nodes = ET.SubElement(root, 'nodes')
        for node in self._graph.get_nodes():
            new_node = ET.SubElement(nodes, 'node')
            new_node.attrib['name'] = node.get_name()
            
            #Write the target
            target = ET.SubElement(new_node, 'target')
            target.text = node.get_target().get_name()

            #Write the attributes
            for attribute in node.get_attributes():
                
                #A Special Case for Node_Type
                if attribute == "Node_Type":
                    nodetype = ET.SubElement(new_node, 'nodetype')
                    nodetype.text = node.get_attributes()[attribute]
                else:
                    attr = ET.SubElement(new_node, 'attr')
                    attr.attrib['name'] = attribute
                    attr.attrib['type'] = type(node.get_attributes()[attribute]).__name__
                    
                    value = ET.SubElement(attr, 'value')
                    value.text = str(node.get_attributes()[attribute])
            
            #Check for modifications
            if not node.get_modification() == None:
                modification_name = node.get_name() + "_Modification.xml"
                modification_filename = self._path + "/Modifications/" + modification_name
                new_node.attrib['modification'] = modification_name
                modification_writer = XMLModificationWriter(modification_filename, node.get_modification())
                modification_writer.writeModification()
            else:
                new_node.attrib['modification'] = 'None'
                
        #Write our connections
        connections = ET.SubElement(root, 'connections')
        for edge in self._graph.get_edges():
            
            #Make the connection
            connection = ET.SubElement(connections, 'connection')
            connection.attrib['from'] = edge.get_from_node().get_name()
            connection.attrib['to'] = edge.get_to_node().get_name()
            
            #Set the relation
            relation = ET.SubElement(connection, 'relation')
            
            if edge.get_key() == None:
                relation.attrib["none"] = "none"
            else:
                relation.attrib[edge.get_key()] = edge.get_value()
            
        #Write our xml to a file
        tree = ET.ElementTree(root)
        tree.write(self._filename + ".xml")
        