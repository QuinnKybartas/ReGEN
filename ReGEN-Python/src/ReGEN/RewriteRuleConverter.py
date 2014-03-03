'''
    Created on 2012-12-14
    
    @author: bkybar
'''

from src.ReGEN.Graph.SocialNode import SocialNode
from src.ReGEN.Graph.StoryNode import StoryNode
from src.ReGEN.Graph.Graph import Graph
from src.ReGEN.Graph.StoryGraph import StoryGraph
from src.ReGEN.Graph.RewriteRule import RewriteRule
from src.ReGEN.IO.XMLRewriteRuleWriter import XMLRewriteRuleWriter

#---------------------------------------------------------------------
#    Narrative Refinements
#---------------------------------------------------------------------

story_rewrite_rules = []

##Double Fight Skeleton
#
##Social Condition
#Target = SocialNode("Monster", {"type" : "Enemy"})
#More_Fight_Social_Condition = Graph("More_Fight_Social_Condition", [Target])
#
##Social Mod
#fighting_modification = [{"Method" : {"name" : SocialNode.killed_enemy, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Monster"}]}}]
#
##Story Condition
#Fight = StoryNode("Fight", {"Node_Type" : "Fight"}, Target)
#More_Fight_Story_Condition = StoryGraph("More_Fight_Story_Condition", [Fight])
#
##Story Modification
#Fight.set_modification(fighting_modification)
#
#Second_Fight = StoryNode("Fight_2", {"Node_Type" : "Fight"}, Target)
#Second_Fight.set_modification(fighting_modification)
#
#More_Fight_Story_Outcome = StoryGraph("More_Fight_Story_Condition", [Fight, Second_Fight])
#More_Fight_Story_Outcome.connect(Fight, {}, Second_Fight)
#
#More_Fight =  RewriteRule(More_Fight_Story_Condition, More_Fight_Social_Condition, More_Fight_Story_Outcome, None, "More_Fight")

#Random Encounter Skeleton

#Social Condition
#Monster = SocialNode("Monster_", {"type" : "Enemy"})
#Invoker = SocialNode("Invoker", {"type" : "NPC"})
#Player = SocialNode("Player", {"name" : "Player"})
#Location = SocialNode("Location", {"type" : "Location"})
#Encounter_Social_Condition = Graph("Encounter_Social_Condition", [Monster, Invoker, Player, Location])
#Encounter_Social_Condition.connect(Player, {"Currently_In" : "N/A"}, Location)
#Encounter_Social_Condition.connect(Monster, {"Targets" : "N/A"}, Location)
#
##Social Mod
#fighting_modification = [{"Method" : {"name" : SocialNode.killed_enemy, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Monster_"}]}}]
#move_player = [{"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Invoker"}]}}]
#
##Story Condition
#Goto = StoryNode("Go_To", {"Node_Type" : "Go_To"}, Invoker)
#Encounter_Story_Condition = StoryGraph("Encounter_Story_Condition", [Goto])
#
##Story Modification
#Goto.set_modification(move_player)
#
#Fight = StoryNode("Encounter", {"Node_Type" : "Fight"}, Monster)
#Fight.set_modification(fighting_modification)
#
#Encounter_Story_Outcome = StoryGraph("Encounter_Story_Condition", [Fight, Goto])
#Encounter_Story_Outcome.connect(Fight, {}, Goto)
#
#Encounter =  RewriteRule(Encounter_Story_Condition, Encounter_Social_Condition, Encounter_Story_Outcome, None, "Encounter")
##----------------------------------------------------
## Ambush Skeleton
##----------------------------------------------------
#
##----------------------------------
## Social Condition
##----------------------------------
#Hater = SocialNode("Hater", {"alive" : True})
#Target = SocialNode("Victim", {"alive" : True})
#
#Ambush_Social_Condition = Graph("Ambush_By_Hater_Social_Condition", [Target, Hater])
#Ambush_Social_Condition.connect(Hater, {"Hates" : "N/A"}, Target)
#
##----------------------------------
## Social Modification
##----------------------------------
#mod_1 = {"Method" : {"name" : SocialNode.murder, "self" : {"ref" : "Victim"}, "args" : [{"ref" : "Hater"}]}}
#mod_2 = {"Attribute" : {"name" : {"ref" : "Victim"}, "key" : "alive", "value" : False}}
#
#Ambush_Modification = [mod_1, mod_2]
#
##----------------------------------
## Story Condition
##----------------------------------
#Murder = StoryNode("Kill_Victim", {"Node_Type" : "Murder"}, Target)
#Ambush_Story_Condition = StoryGraph("Ambush_By_Hater_Story_Condition", [Murder])
#
##----------------------------------
## Story Outcome
##----------------------------------
#Ambush = StoryNode("Ambush_By_Hater", {"Node_Type" : "Cutscene", "Additional" : "Branched_Node"}, Hater)
#Spare = StoryNode("Spare", {"Node_Type" : "Sympathy", "Additional" : "Branched_Node"}, Target)
#Ambush.set_modification(Ambush_Modification)
#Ambush_Story_Outcome = StoryGraph("Ambush_By_Hater_Story_Outcome", [Murder, Ambush, Spare])
#Ambush_Story_Outcome.connect(Murder, {}, Ambush)
#Ambush_Rule = RewriteRule(Ambush_Story_Condition, Ambush_Social_Condition, Ambush_Story_Outcome, None, "Ambush_By_Hater", True)
#----------------------------------------------------
# Ambush Skeleton
#----------------------------------------------------

#----------------------------------
# Social Condition
#----------------------------------
Monster = SocialNode("Monster", {"alive": True})
Recipient = SocialNode("Recipient", {"alive" : True})

Ambush_Social_Condition = Graph("Stolen_Gift_Social_Condition", [Monster, Recipient])
Ambush_Social_Condition.connect(Monster, {"Hates" : "N/A"}, Recipient)
#----------------------------------
# Social Modification
#----------------------------------
#----------------------------------
# Story Condition
#----------------------------------
Murder = StoryNode("Give_Gift", {"Node_Type" : "Give_Item"}, Recipient)
Ambush_Story_Condition = StoryGraph("Stolen_Gift_Condition", [Murder])

#----------------------------------
# Story Outcome
#----------------------------------
Spare = StoryNode("Stolen_Gift", {"Node_Type" : "Robbery", "Additional" : "Branched_Node"}, Monster)
Foigh = StoryNode("Fight_For_Gift", {"Node_Type" : "Fight", "Additional" : "Branched_Node"}, Monster)
Ambush_Story_Outcome = StoryGraph("Stolen_Gift_Story_Outcome", [Murder, Foigh, Spare])
Ambush_Story_Outcome.connect(Spare, {}, Foigh)
Ambush_Rule = RewriteRule(Ambush_Story_Condition, Ambush_Social_Condition, Ambush_Story_Outcome, None, "Stolen_Gift", True)
##----------------------------------------------------
## Ambush Skeleton
##----------------------------------------------------
#
##----------------------------------
## Social Condition
##----------------------------------
#Lover = SocialNode("Lover", {"alive" : True})
#Target = SocialNode("Victim", {"alive" : True})
#
#Ambush_Social_Condition = Graph("Ambush_Social_Condition", [Target, Lover])
#Ambush_Social_Condition.connect(Lover, {"Loves" : "N/A"}, Target)
#
##----------------------------------
## Social Modification
##----------------------------------
#mod_1 = {"Method" : {"name" : SocialNode.murder, "self" : {"ref" : "Lover"}, "args" : [{"ref" : "Player"}]}}
#mod_2 = {"Attribute" : {"name" : {"ref" : "Lover"}, "key" : "alive", "value" : False}}
#
#Ambush_Modification = [mod_1, mod_2]
#
##----------------------------------
## Story Condition
##----------------------------------
#Murder = StoryNode("Kill_Victim", {"Node_Type" : "Murder"}, Target)
#Ambush_Story_Condition = StoryGraph("Ambush_Story_Condition", [Murder])
#
##----------------------------------
## Story Outcome
##----------------------------------
#Ambush = StoryNode("Ambush_By_Lover", {"Node_Type" : "Murder", "Additional" : "Branched_Node"}, Lover)
#Spare = StoryNode("Spare", {"Node_Type" : "Sympathy", "Additional" : "Branched_Node"}, Target)
#Ambush.set_modification(Ambush_Modification)
#Ambush_Story_Outcome = StoryGraph("Ambush_Story_Outcome", [Murder, Ambush, Spare])
#Ambush_Story_Outcome.connect(Murder, {}, Ambush)
#Ambush_Rule = RewriteRule(Ambush_Story_Condition, Ambush_Social_Condition, Ambush_Story_Outcome, None, "Ambush", True)
#
##----------------------------------------------------
## Caught Skeleton
##----------------------------------------------------
#
##----------------------------------
## Social Condition
##----------------------------------
#Object = SocialNode("Object", {"type" : "Object"})
#Owner = SocialNode("Owner", {"type" : "NPC", "alive" : True})
#Steal_Social_Condition = Graph("Steal_Social_Condition", [Owner, Object])
#Steal_Social_Condition.connect(Owner, {"Owns": "N/A"}, Object)
#
##----------------------------------
## Story Condition
##----------------------------------
#Steal_Item = StoryNode("Steal_Item", {"Node_Type" : "Steal"}, Object)
#Steal_Story_Condition = StoryGraph("Steal_Story_Condition", [Steal_Item])
#
##----------------------------------
## Social Modification
##----------------------------------
#mod_1 = {"Method" : {"name" : SocialNode.murder, "self" : {"ref" : "Owner"}, "args" : [{"ref" : "Player"}]}}
#mod_2 = {"Attribute" : {"name" : {"ref" : "Owner"}, "key" : "alive", "value" : False}}
#
#Caught_Modification = [mod_1, mod_2]
#
##----------------------------------
## Story Outcome
##----------------------------------
#Caught = StoryNode("Caught_by_Owner", {"Node_Type" : "Caught", "Additional" : "Branched_Node"}, Owner)
#Kill = StoryNode("Murder_Owner", {"Node_Type" : "Murder", "Additional" : "Branched_Node"}, Owner)
#Kill.set_modification(Caught_Modification)
#Steal_Story_Outcome = StoryGraph("Steal_Story_Outcome", [Steal_Item, Caught, Kill])
#Steal_Story_Outcome.connect(Caught, {}, Kill)
#Caught_Rule = RewriteRule(Steal_Story_Condition, Steal_Social_Condition, Steal_Story_Outcome, None, "Caught", True)
#
##----------------------------------------------------
## Stealth Kill Skeleton
##----------------------------------------------------
##----------------------------------
## Social Condition
##----------------------------------
#Monster = SocialNode("Monster", {"type" : "Enemy"})
#StKill_Social_Condition = Graph("StKill_Condition", [Monster])
#
##----------------------------------
## Story Condition
##----------------------------------
#Fight = StoryNode("Fight_Monster", {"Node_Type" : "Fight"}, Monster)
#StKill_Story_Condition = StoryGraph("StKill_Story_Condition", [Fight])
#
##----------------------------------
## Social Modification
##----------------------------------
#StKill_Modification = [{"Method" : {"name" : SocialNode.killed_enemy, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Monster"}]}}]
#
##----------------------------------
## Story Outcome
##----------------------------------
#Kill = StoryNode("Stealth_Kill", {"Node_Type" : "Stealth", "Additional" : "Branched_Node"}, Monster)
#Loot = StoryNode("Loot_Corpse", {"Node_Type" : "Acquire", "Additional" : "Branched_Node"}, Monster)
#Kill.set_modification(StKill_Modification)
#StKill_Story_Outcome = StoryGraph("StKill_Story_Outcome", [Fight, Kill, Loot])
#StKill_Story_Outcome.connect(Fight, {}, Loot)
#StKill_Story_Outcome.connect(Kill, {}, Loot)
#StKill_Rule = RewriteRule(StKill_Story_Condition, StKill_Social_Condition, StKill_Story_Outcome, None, "Stealth_Kill", None)
#
## ------------------------------------------ #
##      INITIALIZE OUR REWRITE RULES          #
## ------------------------------------------ #
#story_rewrite_rules.append(Ambush_Rule)
#story_rewrite_rules.append(Caught_Rule)
#story_rewrite_rules.append(StKill_Rule)
story_rewrite_rules.append(Ambush_Rule)

for rule in story_rewrite_rules:
    writer = XMLRewriteRuleWriter(rule, "../../Data/Rules/RewriteRules/")
    writer.writeRule()