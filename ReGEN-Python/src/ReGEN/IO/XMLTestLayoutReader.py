'''
Created on 2012-12-14

@author: bkybar
'''

import xml.etree.ElementTree as ET
from src.ReGEN.Test.TestLayout import TestLayout
from src.ReGEN.IO.XMLInitializationRuleReader import XMLInitializationRuleReader
from src.ReGEN.IO.XMLRewriteRuleReader import XMLRewriteRuleReader
from src.ReGEN.IO.XMLSocialGraphReader import XMLSocialGraphReader

class XMLTestLayoutReader(object):


    def __init__(self, path_to_data, filename):
        self._filename = path_to_data + "TestLayout/"+ filename + ".xml"
        self._path_to_data = path_to_data
        
    def readTestLayout(self):
        
        layout = TestLayout()
        
        tree = ET.parse(self._filename)
        root = tree.getroot()
        
        layout.set_name(root.attrib.get('name'))
        layout.set_save_output(root.attrib['save_output'] == 'True')
        
        socialgraph = root.find('socialgraph').text
        filename = self._path_to_data + "SocialGraphs/" + socialgraph + '.xml'
        reader = XMLSocialGraphReader(filename)
        layout.set_social_graph(reader.readGraph())
        
        initializationrules = root.find('initializationrules')
        
        for rule in initializationrules.iter('initializationrule'):
            name = rule.text
            filename = self._path_to_data + "Rules/InitializationRules/" + name + "/"
            reader = XMLInitializationRuleReader(filename, name + ".xml")
            layout.add_initialization_rule(reader.readInitRule())
        
        rewriterules = root.find('rewriterules')
        
        for rule in rewriterules.iter('rewriterule'):
            name = rule.text
            filename = self._path_to_data + "Rules/RewriteRules/" + name + "/"
            reader = XMLRewriteRuleReader(filename, name + ".xml")
            layout.add_rewrite_rule(reader.readRule())
        
        analyze_metrics = root.find('metricstoanalyze')
        
        for metric in analyze_metrics.iter('metric'):
            layout.add_metric_to_analyze(metric.attrib.get('name'))
            
        optimize_metrics = root.find('metricstooptimize')
        
        for metric in optimize_metrics.iter('metric'):
            layout.add_metric_to_optimize([metric.attrib.get('name'), int(metric.attrib.get('weight'))])

        layout.set_number_of_stories_to_generate(int(root.find('numstoriestogenerate').text))
        layout.set_max_number_of_rewrites(int(root.find('maxnumberofrewrites').text))

        return layout