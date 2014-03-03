'''
Created on 2013-01-28

@author: beky
'''

from src.ReGEN.IO.XMLTestLayoutReader import XMLTestLayoutReader
from src.ReGEN.IO.XMLTestResultWriter import XMLTestResultWriter
from src.ReGEN.Metrics.MetricAnalyzer import MetricAnalyzer
from src.ReGEN.Scheduler import Scheduler
import os
import time

class Test():
    
    def __init__(self, test_name, save_output):
        
        #---------------------------------------------------------------------
        #    Load Test Layout
        #---------------------------------------------------------------------
        
        test_reader = XMLTestLayoutReader("Data/", test_name)
        
        self._test = test_reader.readTestLayout()
        self._test.print_description()
        #self._save_output = self._test.get_save_output()
        self._save_output = save_output

        self._output_path = 'Output/' + self._test.get_name() + '/'
        self._final_graph_output = self._output_path + 'Final_Game_States/'
        self._story_output = self._output_path + 'Generated_Narratives/'
        self._stats_output = self._output_path + 'Statistics/'
        self._invalid = 0
        self._valid = 0
        if not os.path.isdir(self._output_path):
            os.mkdir(self._output_path)
        if not os.path.isdir(self._final_graph_output):
            os.mkdir(self._final_graph_output)
        if not os.path.isdir(self._story_output):
            os.mkdir(self._story_output)
        if not os.path.isdir(self._stats_output):
            os.mkdir(self._stats_output)
                
    def run(self):

        start = time.time()
        self.get_narratives()
        end = time.time()
        self.analyze_narratives()
        f = open(self._stats_output + 'total_time.txt', 'w')
        f.write("Narrative Generation Completed in : " + str(end - start) + " seconds")
        
    def get_narratives(self):
        main_graph = self._test.get_social_graph()
        main_graph.initialize()
        
        if self._save_output:
            main_graph.plot(self._output_path + 'Initial_Gamestate')
        
        story_initialization_rules = self._test.get_initialization_rules()
        story_rewrite_rules = self._test.get_rewrite_rules()
        metrics_to_analyze = self._test.get_metrics_to_analyze()
        metrics_to_optimize = self._test.get_metrics_to_optimize()
        max_number_of_rewrites = self._test.get_max_number_of_rewrites()

        main_graph.generate_preconditions()
        self._initial_preconditions = main_graph.get_preconditions()
        sched = Scheduler(main_graph, story_initialization_rules, story_rewrite_rules, metrics_to_optimize, max_number_of_rewrites, self._stats_output)
              
        schedulers = []
        schedulers.append(sched)
        
        final_graphs = []
        failed_to_find_stories = []
        stories = []
        num_stories = 0
        num_scheds = 0
        num_iters = 0
        run = True

        f = open(self._stats_output + 'general_time_stats.txt', 'w')
        f.write("totaltime;inittime;writetime;\n")

        f = open(self._stats_output + 'detailed_time_stats.txt', 'w')
        f.write("metric_rewriting;validation;\n")
        
        while num_stories < self._test.get_number_of_stories_to_generate() and run == True:
            final_graphs = []
            to_append = []
            to_remove = []
            
            for sched in schedulers:
                start_full_narrative = time.time()
                success = sched.initialize_narrative()
                end_init_narrative = time.time()
                if success:
                    num_stories += 1
                    
                    start_write_narrative = time.time()
                    story = sched.write_narrative()
                    end_full_narrative = time.time()

                    f = open(self._stats_output + 'general_time_stats.txt', 'a')
                    f.write(str(end_full_narrative - start_full_narrative) + ';' + str(end_init_narrative - start_full_narrative) + ';' + str(end_full_narrative - start_write_narrative) + ';\n')                   
                    
                    if self._save_output:
                        story.plot_story_graph(self._story_output + 'narrative_' + str(num_stories))
                     
                    to_remove.append(sched)
                    
                    new_paths = story.get_all_paths()
                        
                    for path in new_paths:
                        num_scheds += 1
                        
                        new_graph = sched.get_social_graph().Copy_Social()

                        new_graph.modify_according_to_path(path, story)
                        final_graphs.append(new_graph)

                        if self._save_output:
                            new_graph.plot_social_graph(self._final_graph_output + 'Final_Gamestate_' + str(len(final_graphs)))
                                                      
                        new_sched = Scheduler(new_graph, story_initialization_rules, story_rewrite_rules, metrics_to_optimize, max_number_of_rewrites, self._stats_output)
                        to_append.append(new_sched)
                        
                    stories.append(story)
                else:
                    to_remove.append(sched)
                    self._valid += sched.get_valids()
                    self._invalid += sched.get_invalids()
                    failed_to_find_stories.append(sched.get_social_graph())
                    run = False
            
            for schedule in to_remove:
                schedulers.remove(schedule)
            for schedule in to_append:
                schedulers.append(schedule)
                
            num_iters += 1
        
        for sched in schedulers:
            print sched.get_valids()
            print sched.get_invalids()
            self._valid += sched.get_valids()
            self._invalid += sched.get_invalids()
        print "VALIDDDDD" + str(self._valid)
        print "INVALIDDDD" + str(self._invalid)
        self._stories = stories
        self._final_graphs = final_graphs
        
    def analyze_narratives(self):
        Metric = MetricAnalyzer(self._stories, self._initial_preconditions, self._test.get_metrics_to_analyze())
        results = Metric.go()
        writer = XMLTestResultWriter('Statistics', self._stats_output, results)
        writer.writeResults()
        #Metric.evaluate_final_graphs(self._final_graphs)
