from models.CompactWalks import *
from models.SubgraphConstruction import buildSubgraphDictonaryForNodes
from stellargraph import random
from tensorflow import random as tf_random
from numpy.random import seed
seed(1)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

### Use case 3 - ROBOKOP

## ROBOKOP (Disease)
# given G, node_List, user input regex, embedding method(m), walk_length(l), num_walk(r), 
# given compared_labels {only for database includes multiple labels for nodes}, 
# given metapath {if metapath2vec is used}   

# G = the database link
G = "bolt://robokopkg.renci.org" 

# node_list = a list of nodes of interest
node_list = ['Alzheimer disease','dementia (disease)',
'type 2 diabetes mellitus','type 1 diabetes mellitus',
'HIV infectious disease','AIDS',
'heart disease','hypertensive disorder', 
'palsy','cerebral palsy', 
'synovitis (disease)','rheumatoid arthritis',
'asthma','chronic obstructive pulmonary disease', 
'fatty liver disease','non-alcoholic fatty liver disease',
'migraine disorder','Headache'
            ]

# semantic_query = user input regular expressions
semantic_query = "`biolink:DiseaseOrPhenotypicFeature` ? `biolink:PhenotypicFeature` ? `biolink:Gene`"

# metapaths {if metapath2vec is used}   
metapaths = [['`biolink:DiseaseOrPhenotypicFeature`', '`biolink:PhenotypicFeature`', '`biolink:Gene`', '`biolink:PhenotypicFeature`', '`biolink:DiseaseOrPhenotypicFeature`']]

# compared_labels {only for database includes multiple labels for nodes}
compared_label = ["`biolink:DiseaseOrPhenotypicFeature`", "`biolink:PhenotypicFeature`", "`biolink:Gene`"]

# True node-pairs to evaluate
node_pair1 = ['Alzheimer disease','type 2 diabetes mellitus','HIV infectious disease','heart disease','palsy',
              'synovitis (disease)','asthma','fatty liver disease','migraine disorder']
node_pair2 = ['dementia (disease)','type 1 diabetes mellitus','AIDS','hypertensive disorder','cerebral palsy',
              'rheumatoid arthritis','chronic obstructive pulmonary disease','non-alcoholic fatty liver disease','Headache']

# biulding Subgraphs (SS & NS)
subGsRobokopDiseaseSS = buildSubgraphDictonaryForNodes(node_list, G, semantic_query, compared_label)
subGsRobokopDiseaseNS = buildSubgraphDictonaryForNodes(node_list, G, "`biolink:DiseaseOrPhenotypicFeature` ? ? ? ?", compared_label)

# disease pair prediction result for SS and NS on ROBOKOP
subgraph_dict_SS = subGsRobokopDiseaseSS
subgraph_dict_NS = subGsRobokopDiseaseNS

print("Disease-pair prediction result for SS and NS on ROBOKOP:")
methods = ['deepwalk', 'node2vec', 'metapath2vec']
for m in methods:
    metrics = PairPrediction(subgraph_dict_SS, node_list, node_pair1, node_pair2, m, metapath = metapaths)
    print("SS-"+ m, ":",metrics)
    metrics = PairPrediction(subgraph_dict_NS, node_list, node_pair1, node_pair2, m, metapath = metapaths)
    print("NS-"+ m, ":",metrics)