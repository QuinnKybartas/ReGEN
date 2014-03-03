'''
Created on 2012-11-24

@author: bkybar
'''
import os
import xml.dom.minidom
import xml.etree.ElementTree as ET

class XMLTestResultWriter():
    
    def __init__(self, result, path, results_dictionary):
        self._result = result        
        self._path = path
        self._result_dict = results_dictionary
        
    def writeResults(self):
        
        #Make our new result folder, should none exist
        if not os.path.isdir(self._path):
            os.mkdir(self._path)
        
        """
        Write our base XML file for the Initialization Rule
        """
        #Write our root head
        root = ET.Element('statistics')
        for key in self._result_dict.keys():
            root.attrib[key] = str(self._result_dict[key])   
        
        #Write our xml to a file
        tree = ET.ElementTree(root)
        tree.write(self._path + self._result + ".xml")
        result_xml = xml.dom.minidom.parse(self._path + self._result + ".xml")
        pretty_xml = result_xml.toprettyxml()

        f = open(self._path + self._result + ".xml", "w")
        f.write(pretty_xml)