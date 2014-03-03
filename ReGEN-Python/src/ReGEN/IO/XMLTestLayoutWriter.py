'''
Created on 2012-12-14

@author: bkybar
'''
import xml.etree.ElementTree as ET

class XMLTestLayoutWriter(object):

    def __init__(self, filename, test_layout):
        self._filename = filename
        self._test_layout = test_layout
        
    def writeTest(self):
        root = ET.Element("Test")
        root.attrib["name"] = self._test_layout.get_name()
        root.attrib['save_output'] = str(self._test_layout.get_save_output())
        
        social_graph = ET.SubElement(root, "socialgraph")
        social_graph.text = self._test_layout.get_social_graph().get_name()
        
        initialization_rules = ET.SubElement(root, "initializationrules")
        
        for init_rule in self._test_layout.get_initialization_rules():
            initialization_rule = ET.SubElement(initialization_rules, "initializationrule")
            initialization_rule.text = init_rule.get_name()
            
        rewrite_rules = ET.SubElement(root, "rewriterules")
           
        for rew_rule in self._test_layout.get_rewrite_rules():
            rewrite_rule = ET.SubElement(rewrite_rules, "rewriterule")
            rewrite_rule.text = rew_rule.get_name()
            
        optimize_metrics = ET.SubElement(root, "metricstooptimize")
        
        for opt_met in self._test_layout.get_metrics_to_optimize():
            optimize_metric = ET.SubElement(optimize_metrics, "metric")
            optimize_metric.attrib["name"] = opt_met[0]
            optimize_metric.attrib["weight"] = str(opt_met[1])
            
        analyze_metrics = ET.SubElement(root, "metricstoanalyze")

        for an_met in self._test_layout.get_metrics_to_analyze():
            analyze_metric = ET.SubElement(analyze_metrics, "metric")
            analyze_metric.attrib["name"] = an_met
                    
        num_stories = ET.SubElement(root, "numstoriestogenerate")
        num_stories.text = str(self._test_layout.get_number_of_stories_to_generate())
        
        num_rewrites = ET.SubElement(root, "maxnumberofrewrites")
        num_rewrites.text = str(self._test_layout.get_max_number_of_rewrites())
        
        #Write our xml to a file
        tree = ET.ElementTree(root)
        tree.write(self._filename)