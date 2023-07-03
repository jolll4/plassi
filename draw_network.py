import networkx as nx
import matplotlib.pyplot as plt

def draw_network(G):
    pos = nx.spring_layout(G, seed=0)
    nx.draw_networkx_nodes(G, pos, node_size=10)
    nx.draw_networkx_edges(G, pos, width=0.1)
    plt.show()