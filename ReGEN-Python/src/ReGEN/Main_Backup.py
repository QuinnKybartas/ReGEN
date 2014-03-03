from src.ReGEN.Graph.Edge import * #@UnusedWildImport
from src.ReGEN.Graph.Graph import * #@UnusedWildImport
from src.ReGEN.Graph.Node import * #@UnusedWildImport
from src.ReGEN.Graph.StoryNode import * #@UnusedWildImport
from src.ReGEN.Graph.SocialNode import * #@UnusedWildImport
from src.ReGEN.Graph.SocialGraph import * #@UnusedWildImport
from src.ReGEN.Graph.StoryGraph import * #@UnusedWildImport
from src.ReGEN.Graph.RewriteRule import * #@UnusedWildImport
from src.ReGEN.Graph.Condition import * #@UnusedWildImport

from src.ReGEN.Metrics.Metrics import * #@UnusedWildImport
from src.ReGEN.Metrics.MetricAnalyzer import * #@UnusedWildImport

from src.ReGEN.IO.XMLSocialGraphReader import * #@UnusedWildImport

from Scheduler import * #@UnusedWildImport

#---------------------------------------------------------------------
#	Relation Graph Creation
#---------------------------------------------------------------------

reader = XMLSocialGraphReader('../../Data/SocialGraphs/default.xml')
main_graph = reader.readGraph()

#---------------------------------------------------------------------
#	Skeleton Generation
#---------------------------------------------------------------------

#Initialize an array of our rules
story_initialization_rules = []

#----------------------------------------------------
# Assassination Attempt Skeleton
#----------------------------------------------------

#----------------------------------
# Social Condition
#----------------------------------
A = SocialNode("Assassin", {"type" : "NPC", "alive" : True})
B = SocialNode("Player", {"type" : "Player"})
C = SocialNode("Location", {"type" : "Location"})

Assassination = Graph("Assassination", [A, B, C])
Assassination.connect(A, {"Hates" : "N/A"}, B)
Assassination.connect(A, {"Lives" : "N/A"}, C)
Assassination.connect(B, {"Currently_In" : "N/A"}, C)

#----------------------------------
# Social Outcomes
#----------------------------------

# Kill Victim
mod_1 = {"Method" : {"name" : SocialNode.murder, "self" : {"ref" : "Assassin"}, "args" : [{"ref" : "Player"}]}}
mod_2 = {"Attribute" : {"name" : {"ref" : "Assassin"}, "key" : "alive", "value" : False}}

Assassination_Modification = [mod_1, mod_2]

#----------------------------------
# Story Results
#----------------------------------
One = StoryNode("Encounter_NPC", {"Node_Type" : "Info"}, A)
Two = StoryNode("Attacked_by_NPC", {"Node_Type" : "Attack"}, A)
Three = StoryNode("Kill_NPC", {"Node_Type" : "Murder"}, A)
Three.set_modification(Assassination_Modification)

Assassination_Story = StoryGraph("Murder_Story", [One, Two, Three])
Assassination_Story.connect(One, {}, Two)
Assassination_Story.connect(Two, {}, Three)

Assassination_Rule = RewriteRule(None, Assassination, Assassination_Story, None)

#----------------------------------------------------
# Murder Skeleton
#----------------------------------------------------

#----------------------------------
# Social Condition
#----------------------------------
A = SocialNode("Invoker", {"type" : "NPC", "alive" : True})
B = SocialNode("Victim", {"type" : "NPC", "alive" : True})

Murder = Graph("Murder", [A, B])
Murder.connect(A, {"Hates" : "N/A"}, B)

#----------------------------------
# Social Outcomes
#----------------------------------

# Player Movement
mod_a = {"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Invoker"}]}}
Move_1 = [mod_a]

mod_a = {"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Victim"}]}}
Move_2 = [mod_a]

# Kill Victim
mod_1 = {"Method" : {"name" : SocialNode.murder, "self" : {"ref" : "Victim"}, "args" : [{"ref" : "Player"}]}}
mod_2 = {"Attribute" : {"name" : {"ref" : "Victim"}, "key" : "alive", "value" : False}}
mod_3 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Friends", "Loves"], "Hates", {"ref" : "Invoker"}, "Murder_of_"]}}
mod_4 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Hates", "Enemies"], "Friends", {"ref" : "Invoker"}, "Murder_of_"]}}

Kill_Modification = [mod_1, mod_2, mod_3, mod_4]

#----------------------------------
# Story Results
#----------------------------------
One = StoryNode("Murder_Request_from_Invoker", {"Node_Type" : "Info"}, A)
One.set_modification(Move_1)
Two = StoryNode("Go_To_Victim", {"Node_Type" : "Go_To"}, B)
Two.set_modification(Move_2)
Three = StoryNode("Kill_Victim", {"Node_Type" : "Murder"}, B)
Three.set_modification(Kill_Modification)
Four = StoryNode("Return_to_Invoker", {"Node_Type" : "Return"}, A)
Four.set_modification(Move_1)

Murder_Story = StoryGraph("Murder_Story", [One, Two, Three, Four])
Murder_Story.connect(One, {}, Two)
Murder_Story.connect(Two, {}, Three)
Murder_Story.connect(Three, {}, Four)

Murder_Rule = RewriteRule(None, Murder, Murder_Story, None)


#----------------------------------------------------
# Uprising Skeleton
#----------------------------------------------------

#----------------------------------
# Social Condition
#----------------------------------
A = SocialNode("Invoker", {"type" : "NPC", "alive" : True})
B = SocialNode("Accomplice_1", {"type" : "NPC", "alive" : True})
C = SocialNode("Accomplice_2", {"type" : "NPC", "alive" : True})
D = SocialNode("Victim", {"type" : "NPC", "alive" : True})

Rebel = Graph("Overthrow_Oppresion", [A, B, C, D])
Rebel.connect(A, {"Hates" : "Oppression"}, D)
Rebel.connect(B, {"Hates" : "Oppression"}, D)
Rebel.connect(C, {"Hates" : "Oppression"}, D)

#----------------------------------
# Social Outcomes
#----------------------------------
# Player Movement
mod_a = {"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Invoker"}]}}
Move_1 = [mod_a]

# Kill Victim
mod_1 = {"Method" : {"name" : SocialNode.murder, "self" : {"ref" : "Victim"}, "args" : [{"ref" : "Player"}]}}
mod_2 = {"Attribute" : {"name" : {"ref" : "Victim"}, "key" : "alive", "value" : False}}
mod_3 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Friends", "Loves"], "Hates", {"ref" : "Invoker"}, "Murder_of_"]}}
mod_4 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Friends", "Loves"], "Hates", {"ref" : "Accomplice_1"}, "Murder_of_"]}}
mod_5 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Friends", "Loves"], "Hates", {"ref" : "Accomplice_2"}, "Murder_of_"]}}
mod_6 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Hates", "Enemies"], "Friends", {"ref" : "Invoker"}, "Murder_of_"]}}
mod_7 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Hates", "Enemies"], "Friends", {"ref" : "Accomplice_1"}, "Murder_of_"]}}
mod_8 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Hates", "Enemies"], "Friends", {"ref" : "Accomplice_2"}, "Murder_of_"]}}

Uprising_Modification = [mod_1, mod_2, mod_3, mod_4, mod_5, mod_6, mod_7, mod_8]

#----------------------------------
# Story Results
#----------------------------------
One = StoryNode("Meet_Leader", {"Node_Type" : "Info"}, A)
Two = StoryNode("Plot_to_Destroy", {"Node_Type" : "Info"}, A)
Three = StoryNode("Attack_Victim", {"Node_Type" : "Battle"}, D)
Four = StoryNode("Kill_Victim", {"Node_Type" : "Murder"}, D)
Three.set_modification(Uprising_Modification)
Five = StoryNode("Return_to_Invoker", {"Node_Type" : "Return"}, A)

Rebel_Story = StoryGraph("Murder_Story", [One, Two, Three, Four, Five])
Rebel_Story.connect(One, {}, Two)
Rebel_Story.connect(Two, {}, Three)
Rebel_Story.connect(Three, {}, Four)
Rebel_Story.connect(Four, {}, Five)
Oppression_Rule = RewriteRule(None, Rebel, Rebel_Story, None)



#----------------------------------------------------
# Stealing Skeleton
#----------------------------------------------------

#----------------------------------
# Social Condition
#----------------------------------
A = SocialNode("Thief", {"type" : "NPC", "alive" : True})
B = SocialNode("Owner", {"type" : "NPC", "alive" : True})
C = SocialNode("Object", {"type" : "Object", "value" : "Worthless"})

Steal = Graph("Steal", [A, B, C])
#Steal.connect(A, {"Hates": "N/A"}, B)
Steal.connect(B, {"Owns": "N/A"}, C)

#----------------------------------
# Social Outcomes
#----------------------------------

#Player Movement
Move_1 = [{"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Thief"}]}}]
Move_2 = [{"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Owner"}]}}]

# Exchange the stolen object
stealing_modification = [{"Method" : {"name" : SocialNode.new_owner, "self" : {"ref" : "Object"}, "args" : [{"ref" : "Thief"}, "Stolen", "Stolen"]}}]

#----------------------------------
# Story Results
#----------------------------------
One = StoryNode("Stealing_Request", {"Node_Type" : "Info"}, A)
One.set_modification(Move_1)
Two = StoryNode("Go_To_Owner", {"Node_Type" : "Go_To"}, B)
Two.set_modification(Move_2)
Three = StoryNode("Steal_Item", {"Node_Type" : "Steal"}, C)
Three.set_modification(Move_1)
Four = StoryNode("Return_Item", {"Node_Type" : "Return"}, A)
Four.set_modification(stealing_modification)

Steal_Story = StoryGraph("Steal Story", [One, Two, Three, Four])
Steal_Story.connect(One, {}, Two)
Steal_Story.connect(Two, {}, Three)
Steal_Story.connect(Three, {}, Four)
Steal_Rule = RewriteRule(None, Steal, Steal_Story, None)

#----------------------------------------------------
# Fight the Monsters Skeleton
#----------------------------------------------------

#----------------------------------
# Social Condition
#----------------------------------
Monster = SocialNode("Monster", {"type" : "Enemy"})
Innocent = SocialNode("Innocent", {"type" : "NPC", "alive" : True})
Fight = Graph("Fight", [Monster, Innocent])

#----------------------------------
# Social Outcomes
#----------------------------------

Move_1 = [{"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Innocent"}]}}]
Move_2 = [{"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Monster"}]}}]
fighting_modification = [{"Method" : {"name" : SocialNode.killed_enemy, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Monster"}]}}]

#----------------------------------
# Story Results
#----------------------------------

One = StoryNode("Receive_Request", {"Node_Type" : "Info"}, Innocent)
One.set_modification(Move_1)

Two = StoryNode("Go_To_Lair", {"Node_Type" : "Go_To"}, Monster)
Two.set_modification(Move_2)

Three = StoryNode("Fight_Monster", {"Node_Type" : "Fight"}, Monster)
Three.set_modification(fighting_modification)

Four = StoryNode("Return_To_Invoker", {"Node_Type" : "Return"}, Innocent)
Four.set_modification(Move_1)
 
Fight_Story = StoryGraph("Fight_Story", [One, Two, Three, Four])
Fight_Story.connect(One, {}, Two)
Fight_Story.connect(Two, {}, Three)
Fight_Story.connect(Three, {}, Four)

Fight_Rule = RewriteRule(None, Fight, Fight_Story, None)

#---------------------------------------------------------------------
#	Narrative Refinements
#---------------------------------------------------------------------

story_rewrite_rules = []

#----------------------------------------------------
# Ambush Skeleton
#----------------------------------------------------

#----------------------------------
# Social Condition
#----------------------------------
Lover = SocialNode("Lover", {"alive" : True})
Target = SocialNode("Owner", {"alive" : True})

Ambush_Social_Condition = Graph("Ambush_Social_Condition", [Target, Lover])
Ambush_Social_Condition.connect(Lover, {"Loves" : "N/A"}, Target)

#----------------------------------
# Social Modification
#----------------------------------
mod_1 = {"Method" : {"name" : SocialNode.murder, "self" : {"ref" : "Lover"}, "args" : [{"ref" : "Player"}]}}
mod_2 = {"Attribute" : {"name" : {"ref" : "Lover"}, "key" : "alive", "value" : False}}

Ambush_Modification = [mod_1, mod_2]

#----------------------------------
# Story Condition
#----------------------------------
Murder = StoryNode("Kill_Victim", {"Node_Type" : "Murder"}, Target)
Ambush_Story_Condition = StoryGraph("Ambush_Story_Condition", [Murder])

#----------------------------------
# Story Outcome
#----------------------------------
Ambush = StoryNode("Ambush_By_Lover", {"Node_Type" : "Murder", "Additional" : "Branched_Node"}, Lover)
Spare = StoryNode("Spare", {"Node_Type" : "Sympathy", "Additional" : "Branched_Node"}, Target)
Ambush.set_modification(Ambush_Modification)
Ambush_Story_Outcome = StoryGraph("Ambush_Story_Outcome", [Murder, Ambush, Spare])
Ambush_Story_Outcome.connect(Murder, {}, Ambush)
Ambush_Rule = RewriteRule(Ambush_Story_Condition, Ambush_Social_Condition, Ambush_Story_Outcome, None)

#----------------------------------------------------
# Caught Skeleton
#----------------------------------------------------

#----------------------------------
# Social Condition
#----------------------------------
Object = SocialNode("Object", {"type" : "Object"})
Owner = SocialNode("Owner", {"type" : "NPC", "alive" : True})
Steal_Social_Condition = Graph("Steal_Social_Condition", [Owner, Object])
Steal_Social_Condition.connect(Owner, {"Owns": "N/A"}, Object)

#----------------------------------
# Story Condition
#----------------------------------
Steal_Item = StoryNode("Steal_Item", {"Node_Type" : "Steal"}, Object)
Steal_Story_Condition = StoryGraph("Steal_Story_Condition", [Steal_Item])

#----------------------------------
# Social Modification
#----------------------------------
mod_1 = {"Method" : {"name" : SocialNode.murder, "self" : {"ref" : "Owner"}, "args" : [{"ref" : "Player"}]}}
mod_2 = {"Attribute" : {"name" : {"ref" : "Owner"}, "key" : "alive", "value" : False}}

Caught_Modification = [mod_1, mod_2]

#----------------------------------
# Story Outcome
#----------------------------------
Caught = StoryNode("Caught_by_Owner", {"Node_Type" : "Caught", "Additional" : "Branched_Node"}, Owner)
Kill = StoryNode("Murder_Owner", {"Node_Type" : "Murder", "Additional" : "Branched_Node"}, Owner)
Kill.set_modification(Caught_Modification)
Steal_Story_Outcome = StoryGraph("Steal_Story_Outcome", [Steal_Item, Caught, Kill])
Steal_Story_Outcome.connect(Caught, {}, Kill)
Caught_Rule = RewriteRule(Steal_Story_Condition, Steal_Social_Condition, Steal_Story_Outcome, None, True)

#----------------------------------------------------
# Stealth Kill Skeleton
#----------------------------------------------------
#----------------------------------
# Social Condition
#----------------------------------
Monster = SocialNode("Monster", {"type" : "Enemy"})
StKill_Social_Condition = Graph("StKill_Condition", [Monster])

#----------------------------------
# Story Condition
#----------------------------------
Fight = StoryNode("Fight_Monster", {"Node_Type" : "Fight"}, Monster)
StKill_Story_Condition = StoryGraph("StKill_Story_Condition", [Fight])

#----------------------------------
# Social Modification
#----------------------------------
StKill_Modification = [{"Method" : {"name" : SocialNode.killed_enemy, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Monster"}]}}]

#----------------------------------
# Story Outcome
#----------------------------------
Kill = StoryNode("Stealth_Kill", {"Node_Type" : "Stealth", "Additional" : "Branched_Node"}, Monster)
Loot = StoryNode("Loot_Corpse", {"Node_Type" : "Acquire", "Additional" : "Branched_Node"}, Monster)
Kill.set_modification(StKill_Modification)
StKill_Story_Outcome = StoryGraph("StKill_Story_Outcome", [Fight, Kill, Loot])
StKill_Story_Outcome.connect(Fight, {}, Loot)
StKill_Story_Outcome.connect(Kill, {}, Loot)
StKill_Rule = RewriteRule(StKill_Story_Condition, StKill_Social_Condition, StKill_Story_Outcome, None)

# ------------------------------------------ #
#      INITIALIZE OUR RELATION GRAPH         #
# ------------------------------------------ #

main_graph.initialize()

# ------------------------------------------ #
#           INITIALIZE OUR RULES             #
# ------------------------------------------ #

story_initialization_rules.append(Fight_Rule)
#story_initialization_rules.append(Steal_Rule)
#story_initialization_rules.append(Oppression_Rule)
story_initialization_rules.append(Murder_Rule)
#story_initialization_rules.append(Assassination_Rule)

# ------------------------------------------ #
#      INITIALIZE OUR REWRITE RULES          #
# ------------------------------------------ #
story_rewrite_rules.append(Ambush_Rule)
story_rewrite_rules.append(Caught_Rule)
story_rewrite_rules.append(StKill_Rule)
# ------------------------------------------ #
#           GENERATE A NARRATIVE             #
# ------------------------------------------ #

main_graph.plot('output_initial')
#~ command = "dot -Tpng output_initial.dot -o Initial_Graph.png"
#~ os.system(command)

sched = Scheduler(main_graph, story_initialization_rules, story_rewrite_rules, True, None)

main_graph.generate_preconditions()
initial_preconditions = main_graph.get_preconditions()
#~ 
schedulers = []
schedulers.append(sched)

final_graphs = []
failed_to_find_stories = []
stories = []
num_stories = 0
num_scheds = 0
num_iters = 0
run = True

while num_stories < 1 and run == True:

	final_graphs = []
	to_append = []
	to_remove = []

	for sched in schedulers:
		success = sched.initialize_narrative()
		if success:
			num_stories += 1
			
			story = sched.write_narrative()
			to_remove.append(sched)
			
			new_paths = story.get_all_paths()
				
			for path in new_paths:
				num_scheds += 1
				
				new_graph = main_graph.Copy_Social()
				new_graph.modify_according_to_path(path, story)
				final_graphs.append(new_graph)
				
				#new_graph.plot('output')
				#command = "dot -Tpng output.dot -o Final_Graph" + str(num_scheds) + ".png"
				#os.system(command)
				
				new_sched = Scheduler(new_graph, story_initialization_rules, story_rewrite_rules, True, None)
				to_append.append(new_sched)
				
			stories.append(story)
			#~ command = "dot -Tpng Story.dot -o Narrative_" + str(num_stories) + ".png"
			#~ os.system(command)
						
		else:
			to_remove.append(sched)
			failed_to_find_stories.append(sched.get_social_graph())
			run = False
	
	for sched in to_remove:
		schedulers.remove(sched)
	for sched in to_append:
		schedulers.append(sched)
		
	num_iters += 1

final_graphs.extend(failed_to_find_stories)

Metric = MetricAnalyzer(stories, initial_preconditions)
Metric.go()
#Metric.evaluate_final_graphs(final_graphs)
