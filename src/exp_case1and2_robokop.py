from models.CompactWalks import *
from models.SubgraphConstruction import buildSubgraphDictonaryForNodes
from stellargraph import random
from tensorflow import random as tf_random
from numpy.random import seed
seed(1)

### Use case 1 - ROBOKOP

## ROBOKOP (Drugs)
# given G, node_List, user input regex, embedding method(m), walk_length(l), num_walk(r),
# given compared_labels {only for database includes multiple labels for nodes},
# given metapath {if metapath2vec is used}

# G = the database link
G = "bolt://robokopkg.renci.org"

# # node_list = a list of nodes of interest
node_list = ['Fluoxetine', 'Paroxetine', 'Sertraline',
            'Felodipine', 'Isradipine', 'Nifedipine',
            'Nilotinib', 'Bosutinib', 'Ponatinib',
            'Dexamethasone', 'Betamethasone', 'Desoximetasone',
            'Promethazine', 'Diphenhydramine', 'Chloropyramine',
            'Omeprazole', 'Pantoprazole',
            'Norethindrone', 'Levonorgestrel',
            'Apraclonidine', 'Brimonidine',
            'Glyburide', 'Tolbutamide',
            'Simvastatin', 'Lovastatin', 'Pravastatin'
            ]

label_true = [0,0,0,1,1,1,2,2,2,3,3,3,4,4,4,5,5,6,6,7,7,8,8,9,9,9] # for clustering

# semantic_query = user input regular expressions
semantic_query = "`biolink:ChemicalEntity` ? `biolink:Gene` `biolink:causes` `biolink:DiseaseOrPhenotypicFeature`"

# metapaths {if metapath2vec is used}
metapaths = [['`biolink:ChemicalEntity`', '`biolink:Gene`', '`biolink:DiseaseOrPhenotypicFeature`', '`biolink:Gene`', '`biolink:ChemicalEntity`']]

# compared_labels {only for database includes multiple labels for nodes}
compared_label = ["`biolink:ChemicalEntity`", "`biolink:Gene`", "`biolink:DiseaseOrPhenotypicFeature`"]

# True node-pairs to evaluate
node_pair1 = ['Fluoxetine','Felodipine','Nilotinib','Dexamethasone','Promethazine',
              'Omeprazole','Norethindrone','Apraclonidine',
              'Glyburide',
              'Simvastatin']
node_pair2 = ['Paroxetine','Isradipine','Bosutinib','Betamethasone','Diphenhydramine',
              'Pantoprazole','Levonorgestrel','Brimonidine',
              'Tolbutamide',
              'Lovastatin']

# biulding Subgraphs (SS & NS)
subGsRobokopDrugSS = buildSubgraphDictonaryForNodes(node_list, G, semantic_query, compared_label)
subGsRobokopDrugNS = buildSubgraphDictonaryForNodes(node_list, G, "`biolink:ChemicalEntity` ? ? ? ?", compared_label)

# drug clustering result for SS and NS on ROBOKOP
subgraph_dict_SS = subGsRobokopDrugSS
subgraph_dict_NS = subGsRobokopDrugNS

print("Drug clustering result for SS and NS on ROBOKOP:")
methods = ['deepwalk', 'node2vec', 'metapath2vec']
for m in methods:
    nmi = Clustering(subgraph_dict_SS, node_list, label_true, m, metapath = metapaths)
    print("SS-"+ m, ":",nmi)
    nmi = Clustering(subgraph_dict_NS, node_list, label_true, m, metapath = metapaths)
    print("NS-"+ m, ":",nmi)


### Use case 2 - ROBOKOP

node_pair1 = ['Fluoxetine','Felodipine','Nilotinib','Dexamethasone','Promethazine',
              'Omeprazole','Norethindrone','Apraclonidine',
              'Glyburide',
              'Simvastatin']
node_pair2 = ['Paroxetine','Isradipine','Bosutinib','Betamethasone','Diphenhydramine',
              'Pantoprazole','Levonorgestrel','Brimonidine',
              'Tolbutamide',
              'Lovastatin'] 

metapaths = [['`biolink:ChemicalEntity`', '`biolink:Gene`', '`biolink:DiseaseOrPhenotypicFeature`', '`biolink:Gene`', '`biolink:ChemicalEntity`']]


print("Drug-pair prediction result for SS and NS on ROBOKOP:")
methods = ['deepwalk', 'node2vec', 'metapath2vec']
for m in methods:
    metrics = PairPrediction(subgraph_dict_SS, node_list, node_pair1, node_pair2, m, metapath = metapaths)
    print("SS-"+ m, ":",metrics)
    metrics = PairPrediction(subgraph_dict_NS, node_list, node_pair1, node_pair2, m, metapath = metapaths)
    print("NS-"+ m, ":",metrics)
