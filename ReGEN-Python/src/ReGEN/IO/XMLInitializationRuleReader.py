'''
Read an Initialization Rule from an XML File
Created on 2012-11-24

@author: bkybar
'''

import xml.etree.ElementTree as ET
from src.ReGEN.IO.XMLSocialGraphReader import XMLSocialGraphReader
from src.ReGEN.IO.XMLStoryGraphReader import XMLStoryGraphReader
from src.ReGEN.Graph.RewriteRule import RewriteRule

class XMLInitializationRuleReader():
    
    """
    Initialize our Initialization Rule Reader
    
    """
    def __init__(self, path, filename):
        self._path = path
        self._filename = filename
        
        
    def readInitRule(self):
        
        tree = ET.parse(self._path + self._filename)
        root = tree.getroot()
        
        #Get our rewrite rule name
        ruleName = root.attrib.get('name')
        
        socialConditionFilename = root.find('socialcondition').text + ".xml"
        socialConditionLoader = XMLSocialGraphReader(self._path + socialConditionFilename)
        socialCondition = socialConditionLoader.readGraph()
        
        storyModificationFilename = root.find('storymodification').text + ".xml"
        storyModificationLoader = XMLStoryGraphReader(socialCondition, self._path, storyModificationFilename)
        storyModification = storyModificationLoader.readGraph()
        
        return RewriteRule(None, socialCondition, storyModification, None, ruleName)