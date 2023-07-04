import networkx as nx
import random
import math

def triage_seating_orders(G):
    global seating_order
    global nodes_not_added
    orders = []
    for node in G:
        seating_order = []
        nodes_not_added = list(G.nodes())
        seat_neighbors(G, node)
        orders.append(seating_order)
    evaluate_orders(G, orders)

def seat_neighbors(G, node):
    place_on_seat(node)
    if len(nodes_not_added) == 0:
        return

    neighbor_weights = []
    edges = get_edges(G, node)
    if len(edges) > 0:
        neighbor_weights = get_neighbor_weights_for_node(G, edges, proximity_increase=4)
    for i in range(1, 6):
        next_person_sits_to_the_side = len(seating_order)%2
        if (i <= len(seating_order) and
             ((not next_person_sits_to_the_side and i != 4) 
              or (next_person_sits_to_the_side and i != 3))):

            old_node = seating_order[len(seating_order)-i]
            edges = get_edges(G, old_node)
            if len(edges) > 0:
                combine_neighbors(neighbor_weights,
                    get_neighbor_weights_for_node(G, edges,
                        get_proximity_increase(i, next_person_sits_to_the_side)))

        closest_neighbor = find_highest_proximity_value(neighbor_weights)
    seat_neighbors(G, closest_neighbor)

def get_edges(G, node):
    edges = []
    for i in list(G.edges(node)):
        if i[1] in nodes_not_added:
            edges.append(i)
    return edges

def get_neighbor_weights_for_node(G, edges, proximity_increase):
    neighbor_weights =[]
    for i, j in edges:
        neighbor_weights.append([j, G.get_edge_data(i, j)["weight"]])
        neighbor_weights[-1][1] += proximity_increase
    return neighbor_weights

def combine_neighbors(current_neighbor_weights, incoming_neighbor_weights):
    for i in incoming_neighbor_weights:
        for j in current_neighbor_weights:
            if i[0] == j[0]:
                j[1] += i[1]


def find_highest_proximity_value(person_weights):
    if len(person_weights) == 0:
        return random.choice(nodes_not_added)
    else:
        person_weights.sort(key = lambda x: x[1], reverse=True)
    return person_weights[0][0]

def get_proximity_increase(proximity, next_person_sits_to_the_side):
    if proximity == 1 and not next_person_sits_to_the_side:
        return 4
    elif proximity == 2 or (proximity == 1 and next_person_sits_to_the_side):
        return 2
    elif proximity == 3 or (proximity == 2 and next_person_sits_to_the_side):
        return 3
    elif proximity == 5 or (proximity == 4 and next_person_sits_to_the_side):
        return 1
    else:
        return 0

def place_on_seat(node):
    seating_order.append(node)
    nodes_not_added.remove(node)

def evaluate_orders(G, orders):
    grades = []
    people_count = len(orders[0])
    for order in orders:
        grade = 0
        for i in range(0, people_count):
            for distance in range(-5, 6):
                if i + distance >=0 and i + distance < people_count and distance != 0:
                    grade += grade_increase(G, order, i, distance)
        grades.append([order, grade])
    grades.sort(key = lambda x: x[1], reverse=True)
    print_top_n(grades, n=5)

def grade_increase(G, order, i, distance):
    if G.has_edge(order[i], order[i+distance]):
        edge_weight = G.get_edge_data(order[i], order[i+distance])["weight"]
        return edge_weight
    else:
        return 0

def print_top_n(grades, n):
    for i in range(0,n):
        print("With a score of:", grades[i][1], "\n")
        print_table(grades[i][0])

def print_table(group):
    for i in range(0, math.ceil(len(group)/2)):
        if group[2*i+1]:
           print(group[2*i], "\t|\t", group[2*i+1])
        elif group[2*i]:
            print(group[2*i], "\t|")
    print("-----------------------------------\n")
