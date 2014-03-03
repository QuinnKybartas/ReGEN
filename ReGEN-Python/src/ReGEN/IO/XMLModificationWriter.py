'''
Write a Node Modification to a file
Created on 2013-01-07

@author: bkybartas
'''

import xml.etree.ElementTree as ET
from src.ReGEN.Graph.SocialNode import SocialNode

class XMLModificationWriter():


    def __init__(self, filename, modification_array):
        self._filename = filename
        self._modification_array = modification_array
        
    def writeModification(self):
        self._root =  ET.Element('Modification')
        for modification in self._modification_array:
            if modification.keys()[0] == "Attribute":
                self.writeAttributeModification(modification["Attribute"])
            else:
                self.writeMethodModification(modification["Method"])
        
        #Write our xml to a file
        tree = ET.ElementTree(self._root)
        tree.write(self._filename)
        
    """
    Write an Attribute modification to a file
    """            
    def writeAttributeModification(self, modification):
        attr_mod = ET.SubElement(self._root, 'Attribute')
        attr_mod.attrib["name"] = modification["name"]["ref"]
        attr_mod.attrib["type"] = type(modification["value"]).__name__
        attr_mod.attrib["key"] = modification["key"]
        attr_mod.attrib["value"] = str(modification["value"])
    
    """
    Write a method modification to a file
    """
    def writeMethodModification(self, modification):
        
        attr_mod = ET.SubElement(self._root, 'Method')
        
        #We store a dictionary of functions to string in our social node
        blankNode = SocialNode(None, None)
        function_name = blankNode.get_name_from_function(modification["name"])

        attr_mod.attrib["name"] = function_name
        attr_mod.attrib["self"] = modification["self"]["ref"]
        
        #Process the argument array
        self.process_array(modification["args"], attr_mod, 'args')
        
    def process_array(self, array, current_element, array_name):
        
        new_element = ET.SubElement(current_element, array_name)
        
        for value in array:
            
            value_type = type(value).__name__
            
            if value_type == 'dict':
                dict_element = ET.SubElement(new_element, 'dict')
                for key in value.keys():
                    dict_key_element = ET.SubElement(dict_element, 'dict_element')
                    dict_key_element.attrib["key"] = key
                    dict_key_element.attrib["value"] = str(value[key])
                    dict_key_element.attrib['type'] = type(value[key]).__name__
            
            elif value_type == 'list':
                self.process_array(value, new_element, 'array')
            
            elif value_type == 'float':
                float_element = ET.SubElement(new_element, 'float')
                float_element.attrib["value"] = str(value)
            
            elif value_type == 'int':
                int_element = ET.SubElement(new_element, 'int')
                int_element.attrib["value"] = str(value)
            
            elif value_type == 'bool':
                bool_element = ET.SubElement(new_element, 'bool')
                bool_element.attrib["value"] = str(value)
            
            else:
                str_element = ET.SubElement(new_element, 'str')
                str_element.attrib["value"] = value