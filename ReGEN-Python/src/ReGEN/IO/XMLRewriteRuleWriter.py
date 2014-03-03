'''
Write a Rewrite Rule to an XML file
Created on 2012-12-05

@author: bkybartas
'''
import os
import xml.etree.ElementTree as ET
from src.ReGEN.IO.XMLSocialGraphWriter import XMLSocialGraphWriter
from src.ReGEN.IO.XMLStoryGraphWriter import XMLStoryGraphWriter

class XMLRewriteRuleWriter():
    
    def __init__(self, rule, path):
        self._rule = rule        
        self._path = path + rule.get_name()
        
    def writeRule(self):
        
        #Make our new rule folder, should none exist
        if not os.path.isdir(self._path):
            os.mkdir(self._path)
        
        modificationspath = self._path + "/Modifications/"

        if not os.path.isdir(modificationspath):
            os.mkdir(modificationspath)
        
        """
        Write our base XML file for the Rewrite Rule
        """
        #Write our root head
        root = ET.Element('rule')
        root.attrib['name'] = self._rule.get_name()
        root.attrib['type'] = "Rewrite_Rule"

        if (self._rule.get_apply_once()):
            root.attrib['applyonce'] = 'true'
        else:
            root.attrib['applyonce'] = 'false'
            
        social_condition_name = self._rule.get_name() + "_Social_Condition"
        social_condition = ET.SubElement(root, 'socialcondition')
        social_condition.text = str(social_condition_name)
        
        story_condition_name = self._rule.get_name() + "_Story_Condition"
        story_condition = ET.SubElement(root, 'storycondition')
        story_condition.text = str(story_condition_name)
        
        story_modification_name = self._rule.get_name() + "_Story_Modification"
        story_modification = ET.SubElement(root, 'storymodification')
        story_modification.text = str(story_modification_name)
        
        
        #Write our xml to a file
        tree = ET.ElementTree(root)
        tree.write(self._path + "/" + self._rule.get_name() + ".xml")
        
        #Write the social graph
        social_condition_writer = XMLSocialGraphWriter(self._path + "/" + social_condition_name, self._rule.get_social_condition())
        social_condition_writer.writeGraph()
        
        story_condition_writer = XMLStoryGraphWriter(self._path + "/", story_condition_name, self._rule.get_story_condition())
        story_condition_writer.writeGraph()
        
        story_modification_writer = XMLStoryGraphWriter(self._path + "/", story_modification_name, self._rule.get_story_modification())
        story_modification_writer.writeGraph()