from itertools import product
import math
from lark import Lark, Transformer, v_args
import pandas as pd
from stellargraph import StellarDiGraph
from neo4j import GraphDatabase
import matplotlib.pyplot as plt


regex_grammar = """
    start: node 
         | node (edge node)+
         | node "(" path ")"

    ?path: edge_node
         | path "|" edge_node   -> path_or 
    
    ?edge_node: edge node
         | "(" edge_node+ ")" 
         
    ?edge: attm
         | edge "|" attm        -> edge_or
         
    ?attm: EDGE_LABEL           -> edge
         | attm ">"             -> edge_right
         | attm "<"             -> edge_left
         | NULL                 -> edge_no_label
         | "(" edge ")"     
    
    ?node: atom
        | node "|" atom         -> node_or

    ?atom: NODE_LABEL           -> node
         | NODE_LABEL "*"       -> rep_from_0
         | NODE_LABEL "+"       -> rep_from_1
         | NULL                 -> node_no_label
         | "(" node ")"

    EDGE_LABEL: LABEL_STRING
    NODE_LABEL: LABEL_STRING
    NULL: "?"
    LCASE_LETTER: "a".."z"
    UCASE_LETTER: "A".."Z"
    DIGIT: "0".."9"

    LETTER: UCASE_LETTER | LCASE_LETTER | DIGIT | "_" | "-" | "`" | ":"
    LABEL_STRING: LETTER+ | "_" 

    %import common.CNAME -> NAME
    %import common.WS_INLINE
    %ignore WS_INLINE
"""


@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
    node_idx = 0
    edge_idx = 0
        
    def node(self, name):
        self.node_idx += 1
        return "(n{}:".format(self.node_idx) + str(name) +")"
    
    def edge(self, name):
        self.edge_idx += 1
        return "-[r{}:".format(self.edge_idx) + str(name) +"]-"
    
    def node_no_label(self, name):
        self.node_idx += 1
        return "(n{}".format(self.node_idx) +")"
    
    def edge_no_label(self, name):
        self.edge_idx += 1
        return "-[r{}".format(self.edge_idx) +"]-"
    
    def edge_node(self, name1, name2):
        path = name1 + name2
        return path

    def edge_right(self, name):
        path = ''
        path = name 
        return path + ">"

    def edge_left(self, name):
        path = ''
        path = name 
        return "<" + path

    def rep_from_0(self, name):
        self.node_idx += 1
        path1 = "(n{}:".format(self.node_idx) + str(name) +")"
        path2 = "(n{}:".format(self.node_idx) + str(name) +")" + "--" + "(n{}:".format(self.node_idx+1) + str(name) +")"
        self.node_idx += 1
        return ['', path1, path2]

    def rep_from_1(self, name):
        self.node_idx += 1
        path1 = "(n{}:".format(self.node_idx) + str(name) +")"
        path2 = "(n{}:".format(self.node_idx) + str(name) +")" + "--" + "(n{}:".format(self.node_idx+1) + str(name) +")"
        self.node_idx += 1
        return [path1, path2]

    def node_or(self, name1, name2):
        return [name1, name2]
    
    def edge_or(self, name1, name2):
        return [name1, name2]
    
    def path_or(self, name1, name2):
        return [name1, name2]

# Permutes all possible pathways from the regular expression.
def extractPathways(parse_tree):
    all_elems = []
    mlist = []
    # Walks through the parse tree. If a node may have two or more labels
    # it is added to our collection as a list of all possible labels.
    for child in parse_tree.children:
        if type(child) == str:
            mlist.append([child])
        else:
            mlist.append(child)
            
    # We iterate through all possible combinations of node and edge labels
    # along the provided regex.
    for i in product(*mlist):
        all_elems.append(list(i))
        
    # Filter null characters out of node labels.
    pathways = []
    for i in all_elems:
        if('' in i): 
            idx = i.index("")
            i.pop(idx)
            i.pop(idx-1)
            pathways.append(i)
        else:
            pathways.append(i)
    return pathways

# Generates a CYPHER query for a regular expression. The first node in the regular expression will be 
# mapped onto the source_node_name.
def getQueries(source_node_name, regexes):
    all_queries = []
    subgraph_nodes = []
    # parse
    regex_parser = Lark(regex_grammar, parser='lalr',transformer=CalculateTree())
    parsed = regex_parser.parse(regexes)
    all_pathways = extractPathways(parsed)
    
    queryStr = ''
    final_idx = len(all_pathways)-1
    for i, path in enumerate(all_pathways):
        
        if(path[-1]==''):path[-1]
        start_node_num = path[0].split(":")[0].split("(")[1].split(")")[0]
        query = "MATCH p1="
        query += ''.join(str(elem) for elem in path)   
        query += " WHERE %s.name =" % start_node_num
        query += " '%s'" % source_node_name
        
        # add conditions to the node names if repeated types in the path
        add_where = ""
        repeated = []
        for j in path:
            if ":" in j: # if type is given
                if j.split(":")[1] in repeated: # if type is repeated
                    if ")" in j: # if it is a node
                        prev = path[repeated.index(j.split(":")[1])].split(":")[0].split("(")[1]
                        current = j.split(":")[0].split("(")[1]
                        add_where += " AND %s" % prev
                        add_where += " <> %s" % current
                repeated.append(j.split(":")[1])
            else:
                repeated.append("?")                
            
        query += add_where
        query += " RETURN p1 LIMIT 5000" 
        if(i==final_idx): queryStr += query
        else: queryStr += query + " UNION "
        
#         print(queryStr)
    
    return queryStr

def parsing(regexes):
    # parse
    regex_parser = Lark(regex_grammar, parser='lalr',transformer=CalculateTree())
    reg = regex_parser.parse
    parsed = reg(regexes)
    all_elems = extractPathways(parsed)

    
    llink = []
    for i in all_elems:
        Link = []
        for j in i:
            if ':' in j:
                if '(' in j:
                    nodes = j.split(':',1)[1].split(')')[0]
                    Link.append(nodes)
                if '[' in j:
                    edges = j.split(':',1)[1].split(']')[0]
                    Link.append(edges)
            else:
                edges = '?'
                Link.append(edges)
#         print(Link)

        for i in range(math.floor(len(Link)/2)):
            #print(i)
            if i == 0:
                llink.append(Link[i:(i+3)])
            else:
                llink.append(Link[(i*2):(i*2)+3])

    return llink


def getSubgraph_neo4j(graph_uri, source_node_name, regexes, compared_labels = None):
    
    queryStr = getQueries(source_node_name, regexes)    
    driver = GraphDatabase.driver(graph_uri)
    
    user_labels = []
    for ele in parsing(regexes):
        user_labels += ele
    user_labels = list(set(user_labels))
            
    with driver.session() as session:
        result = session.run(queryStr)
        d = {}
        join_values = []
        for i in result.graph().nodes:
            node_name = i['name']
            if node_name not in join_values:
                #print('labels = ',list(i.labels))
                if len(i.labels)>1:
                    for m in i.labels:
                        
                        if(":" in m):
                            mm = "`" + m + "`"
                            m = mm
                        
                        if m in user_labels:
                            node_type = m
                        
                        ### for multiple-labeled graph using regex "? ? ?"
                        
                        elif compared_labels != None:
                            if m in compared_labels:
                                node_type = m
                        else:
                            node_type = list(i.labels)[0]
                        ###
                else:
                    node_type = list(i.labels)[0]
                s = d.get(node_type,set())

                if type(node_name) == list:
                    s.add(node_name[0])
                else:
                    s.add(node_name)

                d[node_type] = s
            join_values.append(node_name)

        rels = set()
        for i in result.graph().relationships:
            start = i.start_node["name"]
            end = i.end_node["name"]

            if type(start) == list:
                start_n = start[0]
            else:
                start_n = start

            if type(end) == list:
                end_n = end[0]
            else:
                end_n = end

            rel_type = i.type
            rels.add((start_n, end_n, rel_type))

    raw_nodes = d        
    edges = pd.DataFrame.from_records(list(rels),columns=["source","target","label"])

    data_frames = {}
    for k in d:
        node_names = list(d[k])
        df = pd.DataFrame({"name":node_names}).set_index("name")
        data_frames[k] = df

    sg = StellarDiGraph(data_frames,edges=edges, edge_type_column="label")
   
    return sg 

# Helper function. Constructs a dictonary; the keys are node names provided in
# node_list. The values are the semantic subgraphs constructed using the 
# parameters G, semantic_query, and compare_labels.
def buildSubgraphDictonaryForNodes(node_list, G, semantic_query, compared_labels):
    subGs = {}
    for node in node_list:
        subG = getSubgraph_neo4j(G, node, semantic_query, compared_labels)
        subGs[node] = subG
#         print(node)
#         print(infoDict(subG))
    return subGs


# Returns counts of all node by labels in graph and all relationships by types.
def infoDict(subG):
    Info = {}
    for i in subG.info().split('\n'):
        if '[' in i:
            temp = i.rsplit(':',1)
            text = temp[0].strip()
            num = temp[1].split('[')[1].split(']')[0]
            Info[text] = num
    return Info