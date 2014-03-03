'''
Created on 2012-12-14

@author: bkybar
'''

class TestLayout():

    def __init__(self):
        self._name = ""
        self._social_graph = None
        self._save_output = True
        self._initialization_rules = []
        self._rewrite_rules = []
        self._metrics_to_analyze = []
        self._metrics_to_optimize = []
        self._number_of_stories_to_generate = 0
        self._max_number_of_rewrites = 0
    
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name
        
    def get_save_output(self):
        return self._save_output
           
    def set_save_output(self, save):
        self._save_output = save
        
    def get_social_graph(self):
        return self._social_graph
    
    def set_social_graph(self, graph):
        self._social_graph = graph
        
    def get_initialization_rules(self):
        return self._initialization_rules
    
    def set_initialization_rules(self, init_rules):
        self._initialization_rules = init_rules
        
    def  add_initialization_rule(self, rule):
        self._initialization_rules.append(rule)
        
    def get_rewrite_rules(self):
        return self._rewrite_rules
    
    def set_rewrite_rules(self, rewrite_rules):
        self._rewrite_rules = rewrite_rules
        
    def add_rewrite_rule(self, rule):
        self._rewrite_rules.append(rule)
        
    def get_metrics_to_analyze(self):
        return self._metrics_to_analyze
    
    def set_metrics_to_analyze(self, analy_metric):
        self._metrics_to_analyze = analy_metric
        
    def add_metric_to_analyze(self, metric):
        self._metrics_to_analyze.append(metric)
        
    def get_metrics_to_optimize(self):
        return self._metrics_to_optimize
    
    def set_metrics_to_optimize(self, opt_metric):
        self._metrics_to_optimize = opt_metric
        
    def add_metric_to_optimize(self, metric):
        self._metrics_to_optimize.append(metric)
        
    def get_number_of_stories_to_generate(self):
        return self._number_of_stories_to_generate
    
    def set_number_of_stories_to_generate(self, num_stories):
        self._number_of_stories_to_generate = num_stories
        
    def get_max_number_of_rewrites(self):
        return self._max_number_of_rewrites
    
    def set_max_number_of_rewrites(self, max_rewrites):
        self._max_number_of_rewrites = max_rewrites
        
    def print_description(self):
        
        print "Data for Test: " + self._name
        print "-------------------------------------------\n"
        print "Social Graph Used: " + str(self._social_graph.get_name())
        print "Number of Stories to Generate: " + str(self._number_of_stories_to_generate)
        print "Max Number of Story Rewrites: " + str(self._max_number_of_rewrites)
        print "Initialization Rules:"
        for rule in self._initialization_rules:
            print "\t" + rule.get_name()
        print "Rewrite Rules:"
        for rule in self._rewrite_rules:
            print "\t" + rule.get_name()
        print "Metrics To Analyze:"
        for metric in self._metrics_to_analyze:
            print "\t" + metric
        print "Metrics To Optimize:"
        for metric in self._metrics_to_optimize:
            print "\t" + metric[0] + ", Weight: " + str(metric[1])
        print '\n'