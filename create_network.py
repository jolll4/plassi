import networkx as nx

def create_network(avecs, groups, people):
    global G
    G = nx.Graph()
    create_edgeless_network(people)
    add_avecs(avecs)
    add_groups(groups)
    return G

def create_edgeless_network(people):
    for i in people:
        G.add_node(i)

def add_avecs(avecs):
    for i, j in avecs:
        G.add_edge(i,j,weight=8)

def add_groups(groups):
    for group in groups:
        for i in range(0,len(group)-1):
            for j in range(i+1,len(group)):
                if (G.has_edge(group[i], group[j])):
                    G[group[i]][group[j]]["weight"] += 2
                else:
                    G.add_edge(group[i], group[j], weight=2)
