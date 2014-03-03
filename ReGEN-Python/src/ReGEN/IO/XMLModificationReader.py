'''
Created on 2013-01-07

@author: bkybartas
'''
import xml.etree.ElementTree as ET
class XMLModificationReader(object):
    
    """
    Initialize the Modification Reader
    """
    def __init__(self, filename):
        self._filename = filename
        
    """
    Read the Modification
    """
    def readModification(self):
        tree = ET.parse(self._filename)
        root = tree.getroot()
        
        final_modification = []
        
        for modification in root:
            if modification.tag == 'Attribute':
                self.readAttribute(modification, final_modification)
            else:
                self.readMethod(modification, final_modification)
        
        return final_modification
    
    def convertType(self, attribute_value, attribute_type):
        if attribute_type == 'bool':
            return (attribute_value == "True")
        elif attribute_type == 'int':
            return int(attribute_value)
        elif attribute_type == 'float':
            return float(attribute_value)
        else:
            return attribute_value
        
    def readAttribute(self, modification, write_to):
        new_modification = {}
        new_modification["name"] = {"ref" : modification.attrib["name"]}
        new_modification["key"] = modification.attrib["key"]
        converted_value = self.convertType(modification.attrib["value"], modification.attrib["type"])
        new_modification["value"] = converted_value
        write_to.append({"Attribute" : new_modification})
        
    def readMethod(self, modification, write_to):
        new_modification = {}
        
        new_modification["name"] = modification.attrib["name"]
        new_modification["self"] = {"ref" : modification.attrib["self"]}
        arg_array = self.readArray(modification.find("args"))
        new_modification["args"] = arg_array
        write_to.append({"Method" : new_modification})
        
    def readArray(self, array):
        return_array = []
        for element in array:
            if element.tag == 'array':
                new_array = self.readArray(element)
                return_array.append(new_array)
            elif element.tag == 'dict':
                new_dict = {}
                for dict_element in element:
                    converted_value = self.convertType(dict_element.attrib["value"], dict_element.attrib["type"])
                    new_dict[dict_element.attrib["key"]] = converted_value
                return_array.append(new_dict)
            else:
                return_array.append(self.convertType(element.attrib["value"], element.tag))
        return return_array