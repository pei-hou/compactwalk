
from models.SubgraphConstruction import parsing, getSubgraph_neo4j
from stellargraph import random
from tensorflow import random as tf_random
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import time

from sklearn.manifold import TSNE

import numpy as np
import pandas as pd

from gensim.models import Word2Vec
from stellargraph.data import UniformRandomWalk, BiasedRandomWalk, UniformRandomMetaPathWalk

from sklearn import cluster
import matplotlib.pyplot as plt
from sklearn.metrics.cluster import normalized_mutual_info_score

from scipy import interpolate
from scipy.spatial import ConvexHull
from sklearn.cluster import KMeans

# Generates random walks for various methods.

random.random_state(1)
tf_random.set_seed(1)

#Generates random walks for various methods.
def compactWalks(subgraph_dict, node_list, method, l, r, metapath = None):
    Walks = []
    for node in node_list:
        subG = subgraph_dict[node]
        # DeepWalk
        if method == 'deepwalk':
            rw = UniformRandomWalk(subG) #BiasedRandomWalk(G)
            walks = rw.run(
                nodes= [node],#list(G.nodes()),  # root nodes
                length = l,#adj_wlength,  # maximum length of a random walk
                n = r #,  # number of random walks per root node
                #seed = 1
            )

        # Node2Vec
        elif method == 'node2vec':
            rw = BiasedRandomWalk(subG)
            walks = rw.run(
                nodes= [node],  # root nodes
                length = l,  # maximum length of a random walk
                n = r,  # number of random walks per root node
                p = 0.25,  # Defines (unormalised) probability, 1/p, of returning to source node
                q = 0.25#,  # Defines (unormalised) probability, 1/q, for moving away from source node
                #seed = 5
            )

        #Metapath2vec
        elif method == 'metapath2vec':
            rw = UniformRandomMetaPathWalk(subG)
            walks = rw.run(
                nodes= [node],#list(G.nodes()),  # root nodes
                length = l,  # maximum length of a random walk
                n = r,  # number of random walks per root node
                metapaths = metapath#,
                #seed = 5
            )

        # append walks
        for w in walks:
            Walks.append(w)
            
    return Walks

# find semantic ratio for Walks provided.
def sematicRatio_walks(regexes, Walks, subGs):
    num = 0
    den = 0

    # parse
    llink = parsing(regexes)
    print(llink)

    # matching process
    for i in Walks:     
        # matching nodes
        for j in i:
            res = []
            # find node type for j
            # if two or more graphs
            if type(subGs) == dict: 

                nodes = []
                for n in subGs.keys():
                    nodes.append(n)
                
                for n in nodes:
                    if j in subGs[n].nodes():
                        node_label = subGs[n].node_type(j)
                        break

            # if only one graph        
            else: 
                node_label = subGs.node_type(j)

            for l in llink:
                if node_label in l:
                    res.append('Y')
                    break
                else:
                    res.append('N')
            
            # counting how many signals in nodes
            if('Y' in res):
                num += 1
            den += 1
        
        # matching edges
        for j in range(len(i)-1):
            res = []
            node1 = i[j]
            node2 = i[j+1]
            
            # if two graphs
            if type(subGs) == dict: 
                for n in nodes:
                    if (node1, node2) in subGs[n].edges():
                        loc = subGs[n].edges().index((node1, node2))
                        edge_label = subGs[n].edges(' ')[loc][2]
                        break
                    elif (node2, node1) in subGs[n].edges():
                        loc = subGs[n].edges().index((node2, node1))
                        edge_label = subGs[n].edges(' ')[loc][2]
                        break

            # if one graph
            else:
                if (node1, node2) in subGs.edges():
                    loc = subGs.edges().index((node1, node2))
                    edge_label = subGs.edges(' ')[loc][2]
                elif (node2, node1) in subGs.edges():
                    loc = subGs.edges().index((node2, node1))
                    edge_label = subGs.edges(' ')[loc][2]
            
            for l in llink:
                if edge_label in l:
                    res.append('Y')
                    break
                else:
                    res.append('N')      
            # counting how many signals in edges
            if('Y' in res):
                num += 1
            den += 1
    print(num, den)
    return round(num/den,4)


# Generates a model with embeddings from provided collection of Walks.
def buildModel(Walks):
    str_walks = [[str(n) for n in walk] for walk in Walks]
    model = Word2Vec(str_walks, size=128, window=10, min_count=0, sg=1, workers=2, iter=5)
    return model


# Computes various benchmarks for a machine learning models.
def evaluate(model, subgraph_dict, node_list1, node_list2):
    evaluate_dict = {}
    hit_at_1_in_list = 0
    hit_at_3_in_list = 0
    hit_at_5_in_list = 0
    mrr_in_list = 0
    
    Node_List = node_list1 + node_list2
    
    for n in node_list1:
#         print("==", n, "==")
        n_all = 0
        num_in_list = 0
        rank_in_list = 0

        for i in model.wv.most_similar(n, topn = 20000):
            n_all += 1

            for j in Node_List:
                if i[0] in subgraph_dict[j].nodes():
                    nodeType = subgraph_dict[j].node_type(i[0])
                    break

            if i[0] in Node_List:
                num_in_list += 1

            if i[0] == node_list2[node_list1.index(n)]:
#                 print('drugs* ',num_in_list)
                # test: include only drugs in list
                rank_in_list = num_in_list
                if rank_in_list == 1:
                    hit_at_1_in_list += 1
                if rank_in_list <= 3:
                    hit_at_3_in_list += 1
                if rank_in_list <= 5:
                    hit_at_5_in_list += 1
                mrr_in_list += 1/rank_in_list

    HIT1 = round(hit_at_1_in_list/len(node_list1),4)
    HIT3 = round(hit_at_3_in_list/len(node_list1),4)
    HIT5 = round(hit_at_5_in_list/len(node_list1),4)
    MRR = round(mrr_in_list/len(node_list1),4)
    
    evaluate_dict['HIT@1'] = HIT1
    evaluate_dict['HIT@3'] = HIT3
    evaluate_dict['HIT@5'] = HIT5
    evaluate_dict['MRR'] = MRR
    
    return evaluate_dict


## process of experiment use case 1 to compute average NMI
def Clustering(subgraph_dict, node_list, label_true, m, metapath = None):
    NMI = []
    for i in range(0,10): # the times you want to run can be altered here
        Walks = compactWalks(subgraph_dict, node_list, m, 80, 20, metapath)
        model = buildModel(Walks)
        # Retrieve node embeddings and corresponding subjects
        node_ids = model.wv.index2word  # list of node IDs
        node_embeddings = (model.wv.vectors)    

        # clustering
        elist = []
        for i in node_list:
            elist.append(node_embeddings[node_ids.index(i)])
        node_embeddings_drug = np.array(elist)
        X = node_embeddings_drug
        kmeans_fit = cluster.KMeans(n_clusters = 10).fit(X)
        cluster_labels = kmeans_fit.labels_
        label_pred = cluster_labels
        nmi = normalized_mutual_info_score(label_true, label_pred)
        NMI.append(nmi)
        
    return round(sum(NMI)/len(NMI),4)


## process of experiment use case 2, 3 to compute average MRR & Hits@k
def PairPrediction(subgraph_dict, node_list, node_pair1, node_pair2, m, metapath=None):
    metrics = []
    average_dict = {}
    for i in range(0, 10):  # the times you want to run can be altered here
        Walks = compactWalks(subgraph_dict, node_list, m, 80, 20, metapath)
        model = buildModel(Walks)
        # Retrieve node embeddings and corresponding subjects
        node_ids = model.wv.index2word  # list of node IDs
        node_embeddings = (model.wv.vectors)
        mrr_hit = evaluate(model, subgraph_dict, node_pair1, node_pair2)
        metrics.append(mrr_hit)

    HIT1 = round(sum(item.get('HIT@1', 0) for item in metrics) / len(metrics), 4)
    HIT3 = round(sum(item.get('HIT@3', 0) for item in metrics) / len(metrics), 4)
    HIT5 = round(sum(item.get('HIT@5', 0) for item in metrics) / len(metrics), 4)
    MRR = round(sum(item.get('MRR', 0) for item in metrics) / len(metrics), 4)

    average_dict['HIT@1'] = HIT1
    average_dict['HIT@3'] = HIT3
    average_dict['HIT@5'] = HIT5
    average_dict['MRR'] = MRR

    return average_dict


def ClusteringDF(subgraph_dict, node_list, label_true):
    Walks = compactWalks(subgraph_dict, node_list, 'deepwalk', 80, 20, None)
    model = buildModel(Walks)
    # Retrieve node embeddings and corresponding subjects
    node_ids = model.wv.index2word  # list of node IDs
    node_embeddings = (model.wv.vectors)

    # Apply t-SNE transformation on node embeddings and find corresponding embeddings for each node
    tsne = TSNE(n_components=2, random_state=1)
    node_embeddings_2d = tsne.fit_transform(node_embeddings)
    elist = []
    for i in node_list:
        elist.append(node_embeddings_2d[node_ids.index(i)])
    node_embeddings_drug_2d = np.array(elist)

    # clustering
    X = node_embeddings_drug_2d
    df = pd.DataFrame(X, columns=['d1', 'd2'])

    # k means
    kmeans = KMeans(n_clusters=10, random_state=1)
    df['cluster'] = kmeans.fit_predict(X)
    df['label_true'] = label_true

    # get centroids
    centroids = kmeans.cluster_centers_
    cen_x = [i[0] for i in centroids]
    cen_y = [i[1] for i in centroids]

    ## add to df
    df['cen_x'] = df.cluster.map({0: cen_x[0], 1: cen_x[1], 2: cen_x[2], 3: cen_x[3], 4: cen_x[4], 5: cen_x[5],
                                  6: cen_x[6], 7: cen_x[7], 8: cen_x[8], 9: cen_x[9]})
    df['cen_y'] = df.cluster.map({0: cen_x[0], 1: cen_x[1], 2: cen_x[2], 3: cen_x[3], 4: cen_x[4], 5: cen_x[5],
                                  6: cen_x[6], 7: cen_x[7], 8: cen_x[8], 9: cen_x[9]})
    return df


def tSNEplotSS(df, node_list, Node_Lists):
    fig = plt.figure()
    ax = plt.subplot(111)
    # draw the points
    MFC = ['r', 'none', 'g', 'none', 'c', 'none', 'y', 'none', 'C1', 'none']
    markers = ['ro', 'ko', 'gs', 'ks', 'c^', 'k^', 'y*', 'k*', 'C1d', 'kd']

    X = np.array(df[['d1', 'd2']])
    for i, nodes in enumerate(Node_Lists):
        loc = [node_list.index(n) for n in nodes]
        plt.plot(X[loc, 0], X[loc, 1], markers[i], label=Node_Lists[i], mfc=MFC[i])

    for i in df.cluster.unique():
        # get the convex hull
        points = df[df.cluster == i][['d1', 'd2']].values  # predited points
        l = list(points)
        l.append([points.mean(axis=0)[0] * 1.1 - 0.0015, points.mean(axis=0)[1]])
        l.append([points.mean(axis=0)[0], points.mean(axis=0)[1] * 1.1 - 0.0015])
        points = np.array(l)

        hull = ConvexHull(points)
        x_hull = np.append(points[hull.vertices, 0],
                           points[hull.vertices, 0][0])
        y_hull = np.append(points[hull.vertices, 1],
                           points[hull.vertices, 1][0])

        # interpolate
        dist = np.sqrt((x_hull[:-1] - x_hull[1:]) ** 2 + (y_hull[:-1] - y_hull[1:]) ** 2)
        dist_along = np.concatenate(([0], dist.cumsum()))
        spline, u = interpolate.splprep([x_hull, y_hull],
                                        u=dist_along, s=0)
        interp_d = np.linspace(dist_along[0], dist_along[-1], 50)
        interp_x, interp_y = interpolate.splev(interp_d, spline)
        # plot shape
        plt.fill(interp_x, interp_y, '--', alpha=0.2)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.6, box.height * 0.6])
    # Put a legend to the right of the current axis
    lgd = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))


def tSNEplotNS(df, node_list, Node_Lists):
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.grid(False)
    # draw the points
    MFC = ['r', 'none', 'g', 'none', 'c', 'none', 'y', 'none', 'C1', 'none']
    markers = ['ro', 'ko', 'gs', 'ks', 'c^', 'k^', 'y*', 'k*', 'C1d', 'kd']

    X = np.array(df[['d1', 'd2']])
    for i, nodes in enumerate(Node_Lists):
        loc = [node_list.index(n) for n in nodes]
        plt.plot(X[loc, 0], X[loc, 1], markers[i], label=Node_Lists[i], mfc=MFC[i])

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.6, box.height * 0.6])
    # Put a legend to the right of the current axis
    lgd = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))


def TimeToBuildSubgraph(node_list, G, semantic_query, compared_labels):
    times = []
    for node in node_list:
        start = time.time()
        subG = getSubgraph_neo4j(G, node, semantic_query, compared_labels)
        end = time.time()
        times.append(end-start)
    return times