'''
Created on 2012-12-14

@author: bkybar
'''
from src.ReGEN.Graph.SocialNode import SocialNode
from src.ReGEN.Graph.StoryNode import StoryNode
from src.ReGEN.Graph.Graph import Graph
from src.ReGEN.Graph.StoryGraph import StoryGraph
from src.ReGEN.Graph.RewriteRule import RewriteRule
from src.ReGEN.IO.XMLInitializationRuleWriter import XMLInitializationRuleWriter
     
##---------------------------------------------------------------------
##    Skeleton Generation
##---------------------------------------------------------------------
#
##Initialize an array of our rules
story_initialization_rules = []
#
##----------------------------------------------------
## Assassination Attempt Skeleton
##----------------------------------------------------
#
##----------------------------------
## Social Condition
##----------------------------------
#A = SocialNode("Assassin", {"type" : "NPC", "alive" : True})
#B = SocialNode("Player", {"type" : "Player"})
#C = SocialNode("Location", {"type" : "Location"})
#
#Assassination = Graph("Assassination", [A, B, C])
#Assassination.connect(A, {"Hates" : "N/A"}, B)
#Assassination.connect(A, {"Lives" : "N/A"}, C)
#Assassination.connect(B, {"Currently_In" : "N/A"}, C)
#
##----------------------------------
## Social Outcomes
##----------------------------------
#
## Kill Victim
#mod_1 = {"Method" : {"name" : SocialNode.murder, "self" : {"ref" : "Assassin"}, "args" : [{"ref" : "Player"}]}}
#mod_2 = {"Attribute" : {"name" : {"ref" : "Assassin"}, "key" : "alive", "value" : False}}
#
#Assassination_Modification = [mod_1, mod_2]
#
##----------------------------------
## Story Results
##----------------------------------
#One = StoryNode("Encounter_NPC", {"Node_Type" : "Info"}, A)
#Two = StoryNode("Attacked_by_NPC", {"Node_Type" : "Attack"}, A)
#Three = StoryNode("Kill_NPC", {"Node_Type" : "Murder"}, A)
#Three.set_modification(Assassination_Modification)
#
#Assassination_Story = StoryGraph("Murder_Story", [One, Two, Three])
#Assassination_Story.connect(One, {}, Two)
#Assassination_Story.connect(Two, {}, Three)
#
#Assassination_Rule = RewriteRule(None, Assassination, Assassination_Story, None, "Assassinate")
#
##----------------------------------------------------
## Murder Skeleton
##----------------------------------------------------
#
##----------------------------------
## Social Condition
##----------------------------------
#A = SocialNode("Invoker", {"type" : "NPC", "alive" : True})
#B = SocialNode("Victim", {"type" : "NPC", "alive" : True})
#
#Murder = Graph("Murder", [A, B])
#Murder.connect(A, {"Hates" : "N/A"}, B)
#
##----------------------------------
## Social Outcomes
##----------------------------------
#
## Player Movement
#mod_a = {"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Invoker"}]}}
#Move_1 = [mod_a]
#
#mod_a = {"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Victim"}]}}
#Move_2 = [mod_a]
#
## Kill Victim
#mod_1 = {"Method" : {"name" : SocialNode.murder, "self" : {"ref" : "Victim"}, "args" : [{"ref" : "Player"}]}}
#mod_2 = {"Attribute" : {"name" : {"ref" : "Victim"}, "key" : "alive", "value" : False}}
#mod_3 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Friends", "Loves"], "Hates", {"ref" : "Invoker"}, "Murder_of_"]}}
#mod_4 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Hates", "Enemies"], "Friends", {"ref" : "Invoker"}, "Murder_of_"]}}
#
#Kill_Modification = [mod_1, mod_2, mod_3, mod_4]
#
##----------------------------------
## Story Results
##----------------------------------
#One = StoryNode("Murder_Request_from_Invoker", {"Node_Type" : "Info"}, A)
#One.set_modification(Move_1)
#Two = StoryNode("Go_To_Victim", {"Node_Type" : "Go_To"}, B)
#Two.set_modification(Move_2)
#Three = StoryNode("Kill_Victim", {"Node_Type" : "Murder"}, B)
#Three.set_modification(Kill_Modification)
#Four = StoryNode("Return_to_Invoker", {"Node_Type" : "Return"}, A)
#Four.set_modification(Move_1)
#
#Murder_Story = StoryGraph("Murder_Story", [One, Two, Three, Four])
#Murder_Story.connect(One, {}, Two)
#Murder_Story.connect(Two, {}, Three)
#Murder_Story.connect(Three, {}, Four)
#
#Murder_Rule = RewriteRule(None, Murder, Murder_Story, None, "Murder")
#
#
##----------------------------------------------------
## Uprising Skeleton
##----------------------------------------------------
#
##----------------------------------
## Social Condition
##----------------------------------
#A = SocialNode("Invoker", {"type" : "NPC", "alive" : True})
#B = SocialNode("Accomplice_1", {"type" : "NPC", "alive" : True})
#C = SocialNode("Accomplice_2", {"type" : "NPC", "alive" : True})
#D = SocialNode("Victim", {"type" : "NPC", "alive" : True})
#
#Rebel = Graph("Overthrow_Oppresion", [A, B, C, D])
#Rebel.connect(A, {"Hates" : "Oppression"}, D)
#Rebel.connect(B, {"Hates" : "Oppression"}, D)
#Rebel.connect(C, {"Hates" : "Oppression"}, D)
#
##----------------------------------
## Social Outcomes
##----------------------------------
## Player Movement
#mod_a = {"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Invoker"}]}}
#Move_1 = [mod_a]
#
## Kill Victim
#mod_1 = {"Method" : {"name" : SocialNode.murder, "self" : {"ref" : "Victim"}, "args" : [{"ref" : "Player"}]}}
#mod_2 = {"Attribute" : {"name" : {"ref" : "Victim"}, "key" : "alive", "value" : False}}
#mod_3 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Friends", "Loves"], "Hates", {"ref" : "Invoker"}, "Murder_of_"]}}
#mod_4 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Friends", "Loves"], "Hates", {"ref" : "Accomplice_1"}, "Murder_of_"]}}
#mod_5 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Friends", "Loves"], "Hates", {"ref" : "Accomplice_2"}, "Murder_of_"]}}
#mod_6 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Hates", "Enemies"], "Friends", {"ref" : "Invoker"}, "Murder_of_"]}}
#mod_7 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Hates", "Enemies"], "Friends", {"ref" : "Accomplice_1"}, "Murder_of_"]}}
#mod_8 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Victim"}, "args" : [["Hates", "Enemies"], "Friends", {"ref" : "Accomplice_2"}, "Murder_of_"]}}
#
#Uprising_Modification = [mod_1, mod_2, mod_3, mod_4, mod_5, mod_6, mod_7, mod_8]
#
##----------------------------------
## Story Results
##----------------------------------
#One = StoryNode("Meet_Leader", {"Node_Type" : "Info"}, A)
#Two = StoryNode("Plot_to_Destroy", {"Node_Type" : "Info"}, A)
#Three = StoryNode("Attack_Victim", {"Node_Type" : "Battle"}, D)
#Four = StoryNode("Kill_Victim", {"Node_Type" : "Murder"}, D)
#Three.set_modification(Uprising_Modification)
#Five = StoryNode("Return_to_Invoker", {"Node_Type" : "Return"}, A)
#
#Rebel_Story = StoryGraph("Murder_Story", [One, Two, Three, Four, Five])
#Rebel_Story.connect(One, {}, Two)
#Rebel_Story.connect(Two, {}, Three)
#Rebel_Story.connect(Three, {}, Four)
#Rebel_Story.connect(Four, {}, Five)
#Oppression_Rule = RewriteRule(None, Rebel, Rebel_Story, None, "Rebel")
#
#
#
##----------------------------------------------------
## Stealing Skeleton
##----------------------------------------------------
#
##----------------------------------
## Social Condition
##----------------------------------
#A = SocialNode("Thief", {"type" : "NPC", "alive" : True})
#B = SocialNode("Owner", {"type" : "NPC", "alive" : True})
#C = SocialNode("Object", {"type" : "Object", "value" : "Worthless"})
#
#Steal = Graph("Steal", [A, B, C])
##Steal.connect(A, {"Hates": "N/A"}, B)
#Steal.connect(B, {"Owns": "N/A"}, C)
#
##----------------------------------
## Social Outcomes
##----------------------------------
#
##Player Movement
#Move_1 = [{"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Thief"}]}}]
#Move_2 = [{"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Owner"}]}}]
#
## Exchange the stolen object
#stealing_modification = [{"Method" : {"name" : SocialNode.new_owner, "self" : {"ref" : "Object"}, "args" : [{"ref" : "Thief"}, "Stolen", "Stolen"]}}]
#
##----------------------------------
## Story Results
##----------------------------------
#One = StoryNode("Stealing_Request", {"Node_Type" : "Info"}, A)
#One.set_modification(Move_1)
#Two = StoryNode("Go_To_Owner", {"Node_Type" : "Go_To"}, B)
#Two.set_modification(Move_2)
#Three = StoryNode("Steal_Item", {"Node_Type" : "Steal"}, C)
#Three.set_modification(Move_1)
#Four = StoryNode("Return_Item", {"Node_Type" : "Return"}, A)
#Four.set_modification(stealing_modification)
#
#Steal_Story = StoryGraph("Steal Story", [One, Two, Three, Four])
#Steal_Story.connect(One, {}, Two)
#Steal_Story.connect(Two, {}, Three)
#Steal_Story.connect(Three, {}, Four)
#Steal_Rule = RewriteRule(None, Steal, Steal_Story, None, "Steal")
#
#----------------------------------------------------
# Fight the Monsters Skeleton
#----------------------------------------------------

#----------------------------------
# Social Condition
#----------------------------------
#Monster = SocialNode("Monster", {"type" : "Enemy"})
#Invoker = SocialNode("Invoker", {"type" : "NPC", "alive" : True})
#Fight = Graph("Fight", [Monster, Invoker])
#
##----------------------------------
## Social Outcomes
##----------------------------------
#
#Move_1 = [{"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Invoker"}]}}]
#Move_2 = [{"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Monster"}]}}]
#fighting_modification = [{"Method" : {"name" : SocialNode.killed_enemy, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Monster"}]}}]
#
##----------------------------------
## Story Results
##----------------------------------
#
#One = StoryNode("Receive_Request", {"Node_Type" : "Info"}, Invoker)
#One.set_modification(Move_1)
#
#Two = StoryNode("Go_To_Lair", {"Node_Type" : "Go_To"}, Monster)
#Two.set_modification(Move_2)
#
#Three = StoryNode("Fight_Monster", {"Node_Type" : "Fight"}, Monster)
#Three.set_modification(fighting_modification)
#
#Four = StoryNode("Return_To_Invoker", {"Node_Type" : "Return"}, Invoker)
#Four.set_modification(Move_1)
# 
#Fight_Story = StoryGraph("Fight_Story", [One, Two, Three, Four])
#Fight_Story.connect(One, {}, Two)
#Fight_Story.connect(Two, {}, Three)
#Fight_Story.connect(Three, {}, Four)
#
#Fight_Rule = RewriteRule(None, Fight, Fight_Story, None, "Fight")
#----------------------------------------------------
# MurderBlackmailer Skeleton
#----------------------------------------------------

#----------------------------------
# Social Condition
#----------------------------------
A = SocialNode("Invoker", {"type" : "NPC", "alive" : True})
B = SocialNode("Recipient", {"type" : "NPC", "alive" : True})

MurderBlackmailer = Graph("MurderBlackmailer", [A, B])
MurderBlackmailer.connect(A, {"Blackmail" : "N/A"}, B)

#----------------------------------
# Social Outcomes
#----------------------------------

# Player Movement
mod_a = {"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Invoker"}]}}
Move_1 = [mod_a]

mod_a = {"Method" : {"name" : SocialNode.move_player_to_node, "self" : {"ref" : "Player"}, "args" : [{"ref" : "Recipient"}]}}
Move_2 = [mod_a]

# Kill Victim
mod_1 = {"Method" : {"name" : SocialNode.murder, "self" : {"ref" : "Recipient"}, "args" : [{"ref" : "Player"}]}}
mod_2 = {"Attribute" : {"name" : {"ref" : "Recipient"}, "key" : "alive", "value" : False}}
mod_3 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Recipient"}, "args" : [["Friends", "Loves"], "Hates", {"ref" : "Invoker"}, "MurderBlackmailer_of_"]}}
mod_4 = {"Method" : {"name" : SocialNode.set_other_nodes_relations, "self" : {"ref" : "Recipient"}, "args" : [["Hates", "Enemies"], "Friends", {"ref" : "Invoker"}, "MurderBlackmailer_of_"]}}

Kill_Modification = [mod_1, mod_2, mod_3, mod_4]

#----------------------------------
# Story Results
#----------------------------------
One = StoryNode("MurderBlackmailer_Request_from_Invoker", {"Node_Type" : "Info"}, A)
One.set_modification(Move_1)
Two = StoryNode("Go_To_Victim", {"Node_Type" : "Go_To"}, B)
Two.set_modification(Move_2)
Three = StoryNode("Kill_Victim", {"Node_Type" : "MurderBlackmailer"}, B)
Three.set_modification(Kill_Modification)
Four = StoryNode("Return_to_Invoker", {"Node_Type" : "Return"}, A)
Four.set_modification(Move_1)

MurderBlackmailer_Story = StoryGraph("MurderBlackmailer_Story", [One, Two, Three, Four])
MurderBlackmailer_Story.connect(One, {}, Two)
MurderBlackmailer_Story.connect(Two, {}, Three)
MurderBlackmailer_Story.connect(Three, {}, Four)

MurderBlackmailer_Rule = RewriteRule(None, MurderBlackmailer, MurderBlackmailer_Story, None, "Murder_Blackmailer")

#----------------------------------------------------
# GiveGift Skeleton
#----------------------------------------------------

#----------------------------------
# Social Condition
#----------------------------------
A = SocialNode("Invoker", {"type" : "NPC", "alive" : True})
B = SocialNode("Recipient", {"type" : "NPC", "alive" : True})

GiveGift = Graph("GiveGift", [A, B])
GiveGift.connect(A, {"Loves" : "N/A"}, B)

#----------------------------------
# Story Results
#----------------------------------
One = StoryNode("GiveGift_Request_from_Invoker", {"Node_Type" : "Info"}, A)
Two = StoryNode("Go_To_Recipient", {"Node_Type" : "Go_To"}, B)
Three = StoryNode("Give_Gift", {"Node_Type" : "Give_Item"}, B)
Four = StoryNode("Return_to_Invoker", {"Node_Type" : "Return"}, A)

GiveGift_Story = StoryGraph("GiveGift_Story", [One, Two, Three, Four])
GiveGift_Story.connect(One, {}, Two)
GiveGift_Story.connect(Two, {}, Three)
GiveGift_Story.connect(Three, {}, Four)

GiveGift_Rule = RewriteRule(None, GiveGift, GiveGift_Story, None, "Give_Gift")

#----------------------------------------------------
# BreakAlly Skeleton
#----------------------------------------------------

#----------------------------------
# Social Condition
#----------------------------------
A = SocialNode("Invoker", {"type" : "NPC", "alive" : True})
B = SocialNode("Recipient", {"type" : "NPC", "alive" : True})

BreakAlly = Graph("BreakAlly", [A, B])
BreakAlly.connect(A, {"Allies" : "N/A"}, B)

#----------------------------------
# Story Results
#----------------------------------
One = StoryNode("Break_Ally_Request_from_Invoker", {"Node_Type" : "Info"}, A)
Two = StoryNode("Go_To_Recipient", {"Node_Type" : "Go_To"}, B)
Three = StoryNode("Break_Allegiance", {"Node_Type" : "Damage"}, B)
Four = StoryNode("Return_to_Invoker", {"Node_Type" : "Return"}, A)

BreakAlly_Story = StoryGraph("BreakAlly_Story", [One, Two, Three, Four])
BreakAlly_Story.connect(One, {}, Two)
BreakAlly_Story.connect(Two, {}, Three)
BreakAlly_Story.connect(Three, {}, Four)

BreakAlly_Rule = RewriteRule(None, BreakAlly, BreakAlly_Story, None, "Break_Ally")

#----------------------------------------------------
# ForgeAlly Skeleton
#----------------------------------------------------

#----------------------------------
# Social Condition
#----------------------------------
A = SocialNode("Invoker", {"type" : "NPC", "alive" : True})
B = SocialNode("Recipient", {"type" : "NPC", "alive" : True})

ForgeAlly = Graph("ForgeAlly", [A, B])
ForgeAlly.connect(A, {"Enemies" : "N/A"}, B)

#----------------------------------
# Story Results
#----------------------------------
One = StoryNode("Forge_Ally_Request_from_Invoker", {"Node_Type" : "Info"}, A)
Two = StoryNode("Go_To_Recipient", {"Node_Type" : "Go_To"}, B)
Three = StoryNode("Forge_Allegiance", {"Node_Type" : "Ally"}, B)
Four = StoryNode("Return_to_Invoker", {"Node_Type" : "Return"}, A)

ForgeAlly_Story = StoryGraph("ForgeAlly_Story", [One, Two, Three, Four])
ForgeAlly_Story.connect(One, {}, Two)
ForgeAlly_Story.connect(Two, {}, Three)
ForgeAlly_Story.connect(Three, {}, Four)

ForgeAlly_Rule = RewriteRule(None, ForgeAlly, ForgeAlly_Story, None, "Forge_Ally")

#----------------------------------------------------
# Spy Skeleton
#----------------------------------------------------

#----------------------------------
# Social Condition
#----------------------------------
A = SocialNode("Invoker", {"type" : "NPC", "alive" : True})
B = SocialNode("Recipient", {"type" : "NPC", "alive" : True})

Spy = Graph("Spy", [A, B])
Spy.connect(A, {"Distrusts" : "N/A"}, B)

#----------------------------------
# Story Results
#----------------------------------
One = StoryNode("Spy_Request_from_Invoker", {"Node_Type" : "Info"}, A)
Two = StoryNode("Go_To_Untrusted_NPC", {"Node_Type" : "Go_To"}, B)
Three = StoryNode("Spy_On_Untrusted_NPC", {"Node_Type" : "Spy"}, B)
Four = StoryNode("Return_to_Invoker", {"Node_Type" : "Return"}, A)

Spy_Story = StoryGraph("Spy_Story", [One, Two, Three, Four])
Spy_Story.connect(One, {}, Two)
Spy_Story.connect(Two, {}, Three)
Spy_Story.connect(Three, {}, Four)

Spy_Rule = RewriteRule(None, Spy, Spy_Story, None, "Spy")

#----------------------------------------------------
# GiveBlackmailLetter Skeleton
#----------------------------------------------------

#----------------------------------
# Social Condition
#----------------------------------
A = SocialNode("Invoker", {"type" : "NPC", "alive" : True})
B = SocialNode("Recipient", {"type" : "NPC", "alive" : True})

GiveBlackmailLetter = Graph("GiveBlackmailLetter", [A, B])
GiveBlackmailLetter.connect(A, {"Distrusts" : "N/A"}, B)

#----------------------------------
# Story Results
#----------------------------------
One = StoryNode("GiveBlackmailLetter_Request_from_Invoker", {"Node_Type" : "Info"}, A)
Two = StoryNode("Go_To_Recipient", {"Node_Type" : "Go_To"}, B)
Three = StoryNode("Give_BlackmailLetter", {"Node_Type" : "Give_Item"}, B)
Four = StoryNode("Return_to_Invoker", {"Node_Type" : "Return"}, A)

GiveBlackmailLetter_Story = StoryGraph("GiveBlackmailLetter_Story", [One, Two, Three, Four])
GiveBlackmailLetter_Story.connect(One, {}, Two)
GiveBlackmailLetter_Story.connect(Two, {}, Three)
GiveBlackmailLetter_Story.connect(Three, {}, Four)

GiveBlackmailLetter_Rule = RewriteRule(None, GiveBlackmailLetter, GiveBlackmailLetter_Story, None, "Give_Blackmail_Letter")


story_initialization_rules.append(BreakAlly_Rule)
story_initialization_rules.append(MurderBlackmailer_Rule)
story_initialization_rules.append(ForgeAlly_Rule)
story_initialization_rules.append(Spy_Rule)
story_initialization_rules.append(GiveBlackmailLetter_Rule)
story_initialization_rules.append(GiveGift_Rule)
#story_initialization_rules.append(Steal_Rule)
#story_initialization_rules.append(Oppression_Rule)
#story_initialization_rules.append(Murder_Rule)
#story_initialization_rules.append(Assassination_Rule)
        
for rule in story_initialization_rules:
    writer = XMLInitializationRuleWriter(rule,  "../../Data/Rules/InitializationRules/")
    writer.writeRule()
            
        