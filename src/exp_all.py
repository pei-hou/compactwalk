from models.CompactWalks import * 
from models.SubgraphConstruction import buildSubgraphDictonaryForNodes
from stellargraph import random
from tensorflow import random as tf_random
from numpy.random import seed
seed(1)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

### Use case 1

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



### Use case 2

# drug pair prediction result for SS and NS on Hetionet
subgraph_dict_SS = subGsHetioDrugSS
subgraph_dict_NS = subGsHetioDrugNS

# Reload the needed inputs (node_list, node_pair1, node_pair2, metapath) for Hetio drug-pairs
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

node_pair1 = ['Canagliflozin', 'Dexamethasone','Lapatinib', 
                'Captopril','Losartan', 'Nifedipine', 
                'Simvastatin', 'Alendronate', 'Citalopram']
node_pair2 = ['Dapagliflozin','Betamethasone','Afatinib',
                'Enalapril','Valsartan','Felodipine',
                'Atorvastatin','Incadronate','Escitalopram']

metapaths = [['Compound','Gene','Disease', 'Gene', 'Compound']]


print("Drug-pair prediction result for SS and NS on Hetionet:")
methods = ['deepwalk', 'node2vec', 'metapath2vec']
for m in methods:
    metrics = PairPrediction(subgraph_dict_SS, node_list, node_pair1, node_pair2, m, metapath = metapaths)
    print("SS-"+ m, ":",metrics)
    metrics = PairPrediction(subgraph_dict_NS, node_list, node_pair1, node_pair2, m, metapath = metapaths)
    print("NS-"+ m, ":",metrics)



# drug pair prediction result for SS and NS on ROBOKOP
subgraph_dict_SS = subGsRobokopDrugSS
subgraph_dict_NS = subGsRobokopDrugNS

# Reload the needed inputs (node_list, node_pair1, node_pair2, metapath) for Robokop drug-pairs
node_list = ['Fluoxetine', 'Paroxetine', 
            'Felodipine', 'Isradipine', 
            'Nilotinib', 'Bosutinib', 
            'Dexamethasone', 'Betamethasone', 
            'Promethazine', 'Diphenhydramine', 
            'Omeprazole', 'Pantoprazole',
            'Norethindrone', 'Levonorgestrel', 
            'Apraclonidine', 'Brimonidine', 
            'Glyburide', 'Tolbutamide', 
            'Simvastatin', 'Lovastatin'
            ] 

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



### Use case 3

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



## ROBOKOP (Disease)
# given G, node_List, user input regex, embedding method(m), walk_length(l), num_walk(r), 
# given compared_labels {only for database includes multiple labels for nodes}, 
# given metapath {if metapath2vec is used}   

# G = the database link
G = "bolt://robokopkg.renci.org" 

# node_list = a list of nodes of interest
node_list = ['Alzheimer disease','dementia',
'type 2 diabetes mellitus','type 1 diabetes mellitus',
'HIV infectious disease','AIDS',
'heart disorder','hypertensive disorder', 
'palsy','cerebral palsy', 
'synovitis','rheumatoid arthritis',
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
node_pair1 = ['Alzheimer disease','type 2 diabetes mellitus','HIV infectious disease','heart disorder','palsy',
              'synovitis','asthma','fatty liver disease','migraine disorder']
node_pair2 = ['dementia','type 1 diabetes mellitus','AIDS','hypertensive disorder','cerebral palsy',
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


### Figures

# Drug clustering (Deepwalk-SS)
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

subgraph_dict_SS = subGsHetioDrugSS
subgraph_dict_NS = subGsHetioDrugNS

cluster_df = ClusteringDF(subgraph_dict_SS, node_list, label_true)
tSNEplotSS(cluster_df, node_list, Node_Lists)
plt.savefig('/plots/deepwalk_SS.png', dpi=400, bbox_inches='tight')

# Drug clustering (Deepwalk-NS)
cluster_df = ClusteringDF(subgraph_dict_NS, node_list, label_true)
tSNEplotNS(cluster_df, node_list, Node_Lists)
plt.savefig('/plots/deepwalk_NS.png', dpi=400, bbox_inches='tight')



### Data needed for Figure 4

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

# semantic_query = user input regular expressions
semantic_query = "`biolink:ChemicalEntity` ? `biolink:Gene` `biolink:causes` `biolink:DiseaseOrPhenotypicFeature`" 

# compared_labels {only for database includes multiple labels for nodes}
compared_label = ["`biolink:ChemicalEntity`", "`biolink:Gene`", "`biolink:DiseaseOrPhenotypicFeature`"]

timeSS = TimeToBuildSubgraph(node_list, G, semantic_query, compared_label)
timeNS1 = TimeToBuildSubgraph(node_list, G, "`biolink:ChemicalEntity` ? ?", compared_label)
timeNS2 = TimeToBuildSubgraph(node_list, G, "`biolink:ChemicalEntity` ? ? ? ?", compared_label)

df = pd.DataFrame({'nodes': node_list,
                   'SS': timeSS,
                   'NS1': timeNS1,
                   'NS2': timeNS2})
#reshape DataFrame from wide format to long format
df = pd.melt(df, id_vars='nodes', value_vars=['SS', 'NS1', 'NS2'])
print(df)
df.to_csv('runtime.csv', sep='\t')
