from models.CompactWalks import *
from models.SubgraphConstruction import buildSubgraphDictonaryForNodes
from stellargraph import random
from tensorflow import random as tf_random
from numpy.random import seed
seed(1)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

### Use case 1 - Hetionet

## Hetionet (Drug) 
# given G, node_List, user input regex, embedding method(m), walk_length(l), num_walk(r), 
# given compared_labels {only for database includes multiple labels for nodes}, 
# given metapath {if metapath2vec is used}   

# G = the database link
G = "bolt://neo4j.het.io" 

# node_list = a list of nodes of interest

node_list = ['Dexamethasone', 'Betamethasone', 'Hydrocortisone', 'Mometasone',
'Canagliflozin', 'Dapagliflozin', 
'Lapatinib', 'Afatinib', 'Erlotinib', 'Gefitinib',
'Captopril', 'Enalapril', 'Benazepril', 'Lisinopril',
'Losartan', 'Valsartan', 'Telmisartan', 'Irbesartan',
'Nifedipine', 'Felodipine', 'Amlodipine', 'Nicardipine',
'Simvastatin', 'Atorvastatin', 'Fluvastatin', 'Lovastatin',
'Alendronate', 'Incadronate', 'Zoledronate',
'Citalopram', 'Escitalopram', 'Fluoxetine', 'Paroxetine', 'Sertraline',
'Fluconazole', 'Voriconazole', 'Itraconazole', 'Ketoconazole']
label_true = [0,0,0,0,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,8,8,8,8,8,9,9,9,9] 

# semantic_query = user input regular expressions
semantic_query = "Compound BINDS_CbG Gene ASSOCIATES_DaG< Disease"

# metapaths {if metapath2vec is used}   
metapaths = [['Compound','Gene','Disease', 'Gene', 'Compound']]

# biulding Subgraphs (SS & NS)
subGsHetioDrugSS = buildSubgraphDictonaryForNodes(node_list, G, semantic_query, None)
subGsHetioDrugNS = buildSubgraphDictonaryForNodes(node_list, G, "Compound ? ? ? ?", None)


# drug clustering result for SS and NS on Hetionet
subgraph_dict_SS = subGsHetioDrugSS
subgraph_dict_NS = subGsHetioDrugNS

print("Drug clustering result for SS and NS on Hetionet:")
methods = ['deepwalk', 'node2vec', 'metapath2vec']
for m in methods:
    nmi = Clustering(subgraph_dict_SS, node_list, label_true, m, metapath = metapaths)
    print("SS-"+ m, ":",nmi)
    nmi = Clustering(subgraph_dict_NS, node_list, label_true, m, metapath = metapaths)
    print("NS-"+ m, ":",nmi)


### Use case 2 - Hetionet
node_pair1 = ['Canagliflozin', 'Dexamethasone','Lapatinib', 
                'Captopril','Losartan', 'Nifedipine', 
                'Simvastatin', 'Alendronate', 'Citalopram']
node_pair2 = ['Dapagliflozin','Betamethasone','Afatinib',
                'Enalapril','Valsartan','Felodipine',
                'Atorvastatin','Incadronate','Escitalopram']

print("Drug-pair prediction result for SS and NS on Hetionet:")
methods = ['deepwalk', 'node2vec', 'metapath2vec']
for m in methods:
    metrics = PairPrediction(subgraph_dict_SS, node_list, node_pair1, node_pair2, m, metapath = metapaths)
    print("SS-"+ m, ":",metrics)
    metrics = PairPrediction(subgraph_dict_NS, node_list, node_pair1, node_pair2, m, metapath = metapaths)
    print("NS-"+ m, ":",metrics)


### Figures

Node_Lists = [['Dexamethasone', 'Betamethasone', 'Hydrocortisone', 'Mometasone'],
                ['Canagliflozin', 'Dapagliflozin'],
                ['Lapatinib', 'Afatinib', 'Erlotinib', 'Gefitinib'],
                ['Captopril', 'Enalapril', 'Benazepril', 'Lisinopril'],
                ['Losartan', 'Valsartan', 'Telmisartan', 'Irbesartan'],
                ['Nifedipine', 'Felodipine', 'Amlodipine', 'Nicardipine'],
                ['Simvastatin', 'Atorvastatin', 'Fluvastatin', 'Lovastatin'],
                ['Alendronate', 'Incadronate', 'Zoledronate'],
                ['Citalopram', 'Escitalopram', 'Fluoxetine', 'Paroxetine', 'Sertraline'],
                ['Fluconazole', 'Voriconazole', 'Itraconazole', 'Ketoconazole']]

# Drug clustering (Deepwalk-SS)
cluster_df = ClusteringDF(subgraph_dict_SS, node_list, label_true)
tSNEplotSS(cluster_df, node_list, Node_Lists)
plt.savefig('/plots/deepwalk_SS.png', dpi=400, bbox_inches='tight') #bbox_extra_artists=(lgd,),

# Drug clustering (Deepwalk-NS)
cluster_df = ClusteringDF(subgraph_dict_NS, node_list, label_true)
tSNEplotNS(cluster_df, node_list, Node_Lists)
plt.savefig('/plots/deepwalk_NS.png', dpi=400, bbox_inches='tight')
