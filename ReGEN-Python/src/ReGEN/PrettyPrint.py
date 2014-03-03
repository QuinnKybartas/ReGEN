from src.ReGEN.IO.XMLSocialGraphReader import XMLSocialGraphReader
from src.ReGEN.IO.XMLSocialGraphWriter import XMLSocialGraphWriter
import xml.dom.minidom
import random
a = XMLSocialGraphReader('../../Data/SocialGraphs/Fantasy_World_Improved.xml')
b = a.readGraph()

temp = []
random.seed(5)

for node in b.get_nodes():
    for node_2 in b.get_nodes():
        if not node == node_2:
            if node.get_attributes()['type'] == 'NPC' and node_2.get_attributes()['type'] == 'NPC':
                similarity = 0
                if node.get_attributes()['conscientious'] == node_2.get_attributes()['conscientious']:
                    similarity += 1
                if node.get_attributes()['agreeable'] == node_2.get_attributes()['agreeable']:
                    similarity += 1
                if node.get_attributes()['neurotic'] == node_2.get_attributes()['neurotic']:
                    similarity += 1
                if node.get_attributes()['open'] == node_2.get_attributes()['open']:
                    similarity += 1
                if node.get_attributes()['extraverted'] == node_2.get_attributes()['extraverted']:
                    similarity += 1
                    
                print similarity
                
                if similarity == 0:
                    b.connect(node, {'Hates' : 'Personality'}, node_2)
                elif similarity == 1:
                    b.connect(node, {'Distrusts' : 'Personality'}, node_2)
                elif similarity == 2:
                    if node.get_attributes()['neurotic'] == True:
                        b.connect(node, {'Distrusts' : 'Personality'}, node_2)
                elif similarity == 3:
                    b.connect(node, {'Trusts' : 'Personality'}, node_2)
                elif similarity == 4:
                    if not node.get_attributes()['male'] == node_2.get_attributes()['male']:
                        b.connect(node, {'Loves' : 'Personality'}, node_2)
                    else:
                        b.connect(node, {'Friends' : 'Personality'}, node_2)
#         if not node == node_2:
#             if 'alignment_gne' in node.get_attributes().keys() and 'alignment_gne' in node_2.get_attributes().keys():
#                 if node.get_attributes()['alignment_gne'] == 'Evil' and node_2.get_attributes()['alignment_gne'] == 'Good':
#                     b.connect(node, {'Enemies' : 'Good'}, node_2)
#                     b.connect(node_2, {'Enemies' : 'Evil'}, node)
#                 elif node.get_attributes()['alignment_gne'] == 'Evil' and node_2.get_attributes()['alignment_gne'] == 'Evil':
#                     b.connect(node, {'Allies' : 'Evil'}, node_2)
#                 elif node.get_attributes()['alignment_gne'] == 'Good' and node_2.get_attributes()['alignment_gne'] == 'Good':
#                     b.connect(node, {'Allies' : 'Good'}, node_2)
#             if 'alignment_lnc' in node.get_attributes().keys() and 'alignment_lnc' in node_2.get_attributes().keys():
#                 if node.get_attributes()['alignment_lnc'] == 'Chaotic' and node_2.get_attributes()['alignment_lnc'] == 'Lawful':
#                     b.connect(node, {'Enemies' : 'Lawful'}, node_2)
#                     b.connect(node_2, {'Enemies' : 'Chaotic'}, node)
#                 elif node.get_attributes()['alignment_lnc'] == 'Chaotic' and node_2.get_attributes()['alignment_lnc'] == 'Chaotic':
#                     b.connect(node, {'Allies' : 'Chaotic'}, node_2)
#                 elif node.get_attributes()['alignment_lnc'] == 'Lawful' and node_2.get_attributes()['alignment_lnc'] == 'Lawful':
#                     b.connect(node, {'Allies' : 'Lawful'}, node_2)
#             if 'wealth' in node.get_attributes().keys() and 'wealth' in node_2.get_attributes().keys():
#                 if (node.get_attributes()['wealth'] == 'Rich' or node.get_attributes()['wealth'] == 'Wealthy') and node_2.get_attributes()['wealth'] == 'Poor':
#                     b.connect(node, {'Distrust' : 'Poor'}, node_2)
#                     b.connect(node_2, {'Distrust' : 'Rich'}, node)
#             if 'male' in node.get_attributes().keys() and 'male' in node_2.get_attributes().keys():
#                 if not node.get_attributes()['male'] == node_2.get_attributes()['male']:
#                     rand_num = random.randint(0, 10)
#                     if rand_num >= 5:
#                         if rand_num >= 8:
#                             b.connect(node, {'Desires' : 'Looks'}, node_2)
#                         else:
#                             b.connect(node, {'Repulsed' : 'Looks'}, node_2)

#b.plot('FantasyWorld')
#print "Done"

c = XMLSocialGraphWriter('../../Data/SocialGraphs/Fantasy_World_Autogen', b)
c.writeGraph()

xml = xml.dom.minidom.parse('../../Data/SocialGraphs/Fantasy_World_Autogen.xml')
pretty_xml = xml.toprettyxml()

f = open('../../Data/SocialGraphs/Fantasy_World_Improved_Autogen.xml', 'w')
f.write(pretty_xml)
