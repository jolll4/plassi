import networkx as nx
import random

def triage_seating_orders(G):
    global seating_order
    global nodes_not_added
    orders = []
    for node in G:
        seating_order = []
        nodes_not_added = list(G.nodes())
        seat_neighbors(G, node)
        orders.append(seating_order)
        print(seating_order)
    #evaluate_orders(G, orders)

def seat_neighbors(G, node):
    place_on_seat(node)
    if len(nodes_not_added) == 0:
        return

    neighbors = []
    for i, j in list(G.edges(node)):
        if i in nodes_not_added:
            neighbors.append(i)
    neighbor_weights =[]
    for i, j in neighbors:
        neighbor_weights.append(G.get_edge_data(i, j)["weight"])
    if len(neighbor_weights) > 0:
        closest_neighbor = neighbors[neighbor_weights.index(max(neighbor_weights))]
    else:
        closest_neighbor = random.choice(nodes_not_added)
    seat_neighbors(G, closest_neighbor)

def place_on_seat(node):
    seating_order.append(node)
    nodes_not_added.remove(node)

def evaluate_orders(G, orders):
    print("asd")