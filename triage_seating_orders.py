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
        orders.append(change_to_left_right_format(seating_order))
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
        next_person_sits_on_the_left = len(seating_order)%2
        if (i <= len(seating_order) and
             ((not next_person_sits_on_the_left and i != 3) 
              or (next_person_sits_on_the_left and i != 4))):

            old_node = seating_order[len(seating_order)-i]
            edges = get_edges(G, old_node)
            if len(edges) > 0:
                neighbor_weights = combine_neighbors(neighbor_weights,
                    get_neighbor_weights_for_node(G, edges,
                        get_proximity_increase(i, next_person_sits_on_the_left)))

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
        was_added = False
        for j in current_neighbor_weights:
            if i[0] == j[0]:
                j[1] += i[1]
                was_added = True
        if not was_added:
            current_neighbor_weights.append(i)
    return current_neighbor_weights


def find_highest_proximity_value(person_weights):
    if len(person_weights) == 0:
        return random.choice(nodes_not_added)
    else:
        person_weights.sort(key = lambda x: x[1], reverse=True)
    return person_weights[0][0]

def get_proximity_increase(proximity, person_sits_on_the_left):
    if proximity == 1 and not person_sits_on_the_left:
        return 4
    elif proximity == 2:
        return 3
    elif (proximity == 3 and not person_sits_on_the_left) or (proximity == 1 and person_sits_on_the_left):
        return 2
    elif (proximity == 5 and not person_sits_on_the_left) or (proximity == 3 and person_sits_on_the_left):
        return 1
    else:
        return 0

def place_on_seat(node):
    seating_order.append(node)
    nodes_not_added.remove(node)

def change_to_left_right_format(seating_order):
    for i in range(math.floor(len(seating_order)/2)):
        if i%2:
            seating_order[2*i], seating_order[2*i+1] = seating_order[2*i+1], seating_order[2*i]
    return seating_order

def evaluate_orders(G, orders):
    grades = []
    people_count = len(orders[0])
    for order in orders:
        grade = evaluate_grade(G, order, people_count)
        grades.append([order, grade])
    grades.sort(key = lambda x: x[1], reverse=True)
    grades_top_scores = prioritize_high_grade_positions(G, grades[0:5])
    print_top_n(G, grades_top_scores)

def evaluate_grade(G, order, people_count):
    grade = 0
    for i in range(0, people_count):
        for distance in range(-5, 6):
            if i + distance >=0 and i + distance < people_count and distance != 0:
                grade += grade_increase(G, order, i, distance)
    return grade

def grade_increase(G, order, i, distance):
    if G.has_edge(order[i], order[i+distance]):
        edge_weight = G.get_edge_data(order[i], order[i+distance])["weight"]
        return edge_weight + get_proximity_increase(i%2, distance)
    else:
        return 0
    
def prioritize_high_grade_positions(G, orders_and_grades):
    new_orders_and_grades = []
    for order, grade in orders_and_grades:
        order = improvement_round(G, order)
        grade = evaluate_grade(G, order, len(order))
        new_orders_and_grades.append([order, grade])
    return new_orders_and_grades
  
def improvement_round(G, order):
    for i in range(0, math.floor(len(order)/2)):
        left = order[2*i]
        if len(order)%2 or i+1 < len(order):
            right = order[2*i+1]
        else:
            right = False
        if i+1 < len(order):
            bottom_left = order[2*(i+1)]
            if not len(order)%2:
                bottom_right = order[2*(i+1)+1]
            else:
                bottom_right = False
        else:
            bottom_left = False

        
        if right:
            if i > 0:
                up_left = order[2*(i-1)]
                up_right = order[2*(i-1)+1]
                if get_edge_weight(G, left, up_left) >= 10 and ((does_not_have_an_avec(G, up_right) and does_not_have_an_avec(G, right)) or get_edge_weight(G, up_right, right) >= 10):
                    order[2*i+1], order[2*(i-1)] = order[2*(i-1)], order[2*i+1]
                elif get_edge_weight(G, right, up_right) >= 10 and ((does_not_have_an_avec(G, up_left) and does_not_have_an_avec(G, left)) or get_edge_weight(G, up_left, left) >= 10):
                    order[2*i], order[2*(i-1)+1] = order[2*(i-1)+1], order[2*i]
            if bottom_left:
                if get_edge_weight(G, left, bottom_left) >= 10 and does_not_have_an_avec(G, right):
                    order[2*i+1], order[2*(i+1)] = order[2*(i+1)], order[2*i+1]
                if bottom_right:
                    if get_edge_weight(G, right, bottom_right) >= 10 and ((does_not_have_an_avec(G, bottom_left) and does_not_have_an_avec(G, left)) or get_edge_weight(G, bottom_left, left) >= 10):
                        order[2*i], order[2*(i+1)+1] = order[2*(i+1)+1], order[2*i]

                
    return order

def does_not_have_an_avec(G, node):
    all_edges = G.edges(node, data='weight')
    for i, j, weight in all_edges:
        if weight >= 10:
            return False
    return True

def print_top_n(G, grades):
    for order, grade in grades:
        print("-----------------------------------")
        print("With an average seating score of: %.2f\n" %(grade/G.number_of_nodes()))
        print_table(G, order)

def print_table(G, group):
    for i in range(0, math.ceil(len(group)/2)):
        left = group[2*i]
        if len(group) > 2*i+1:
            right = group[2*i+1]
        else:
            right = False
        if left and right:
           if i>0:
               print(get_edge_weight(G, left, group[2*(i-1)]), "\t\t\t", get_edge_weight(G, right, group[2*(i-1)+1]))
           print(left, "\t",get_edge_weight(G, left, right),"\t", right)
        else:
            if i >0:
                print(get_edge_weight(G, left, group[2*(i-1)]))
            print(left)
    print("-----------------------------------")

def get_edge_weight(G, node1, node2):
    if G.has_edge(node1, node2):
        return G.get_edge_data(node1, node2)["weight"] 
    else:
        return 0
