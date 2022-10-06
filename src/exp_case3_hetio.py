from models.CompactWalks import *
from models.SubgraphConstruction import buildSubgraphDictonaryForNodes
from stellargraph import random
from tensorflow import random as tf_random
from numpy.random import seed
seed(1)

### Use case 3 - Hetionet

## Hetionet (Disease)
# given G, node_List, user input regex, embedding method(m), walk_length(l), num_walk(r), 
# given compared_labels {only for database includes multiple labels for nodes}, 
# given metapath {if metapath2vec is used}   

# G = the database link
G = "bolt://neo4j.het.io" 

# node_list = a list of nodes of interest
node_list = ["hypertension","coronary artery disease",
"endogenous depression","panic disorder",
"schizophrenia",
"endogenous depression",
"pancreatic cancer","lung cancer",
"breast cancer","ovarian cancer",
"bipolar disorder","endogenous depression",
"stomach cancer","prostate cancer",
"migraine","epilepsy syndrome"]

# semantic_query = user input regular expressions
semantic_query = "Disease ASSOCIATES_DaG> Gene BINDS_CbG Compound"

# metapaths {if metapath2vec is used}   
metapaths = [['Disease', 'Gene', 'Compound', 'Gene', 'Disease']]

# True node-pairs to evaluate
node_pair1 = ["hypertension","endogenous depression","schizophrenia","endogenous depression","pancreatic cancer",
              "breast cancer","bipolar disorder","bipolar disorder","stomach cancer","migraine"]


node_pair2 = ["coronary artery disease","panic disorder","panic disorder","panic disorder","lung cancer",
              "ovarian cancer","endogenous depression","panic disorder","prostate cancer","epilepsy syndrome"]

# biulding Subgraphs (SS & NS)
subGsHetioDiseaseSS = buildSubgraphDictonaryForNodes(node_list, G, semantic_query, None)
subGsHetioDiseaseNS = buildSubgraphDictonaryForNodes(node_list, G, "Disease ? ? ? ?", None)

# disease pair prediction result for SS and NS on Hetionet
subgraph_dict_SS = subGsHetioDiseaseSS
subgraph_dict_NS = subGsHetioDiseaseNS

print("Disease-pair prediction result for SS and NS on Hetionet:")
methods = ['deepwalk', 'node2vec', 'metapath2vec']
for m in methods:
    metrics = PairPrediction(subgraph_dict_SS, node_list, node_pair1, node_pair2, m, metapath = metapaths)
    print("SS-"+ m, ":",metrics)
    metrics = PairPrediction(subgraph_dict_NS, node_list, node_pair1, node_pair2, m, metapath = metapaths)
    print("NS-"+ m, ":",metrics)