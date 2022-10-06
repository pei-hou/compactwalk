from models.CompactWalks import *
from models.SubgraphConstruction import buildSubgraphDictonaryForNodes
from stellargraph import random
from tensorflow import random as tf_random
from numpy.random import seed
seed(1)

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