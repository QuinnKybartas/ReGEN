'''
Read a rewrite rule from an XML file
Created on 2012-12-05

@author: bkybartas
'''

import xml.etree.ElementTree as ET
from src.ReGEN.IO.XMLSocialGraphReader import XMLSocialGraphReader
from src.ReGEN.IO.XMLStoryGraphReader import XMLStoryGraphReader
from src.ReGEN.Graph.RewriteRule import RewriteRule

class XMLRewriteRuleReader():
    
    """
    Initialize our Initialization Rule Reader
    
    """
    def __init__(self, path, filename):
        self._path = path
        self._filename = filename
        
        
    def readRule(self):
        
        tree = ET.parse(self._path + self._filename)
        root = tree.getroot()
              
        #Get our rewrite rule name
        ruleName = root.attrib.get('name')
        applyonce = (root.attrib.get('applyonce') == "true")
        
        socialConditionFilename = root.find('socialcondition').text + ".xml"
        socialConditionLoader = XMLSocialGraphReader(self._path + socialConditionFilename)
        socialCondition = socialConditionLoader.readGraph()
        
        storyConditionFilename = root.find('storycondition').text + ".xml"
        storyConditionLoader = XMLStoryGraphReader(socialCondition, self._path, storyConditionFilename)
        storyCondition = storyConditionLoader.readGraph()
        
        storyModificationFilename = root.find('storymodification').text + ".xml"
        storyModificationLoader = XMLStoryGraphReader(socialCondition, self._path, storyModificationFilename)
        storyModification = storyModificationLoader.readGraph()
        
        return RewriteRule(storyCondition, socialCondition, storyModification, None, ruleName, applyonce)