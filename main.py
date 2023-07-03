from create_people_data import create_people_data
from create_network import create_network
from draw_network import draw_network
from triage_seating_orders import triage_seating_orders

import sys
import networkx as nx

def main():
    people_list_file = ""
    placement_list_file = "test_groups.txt"
    avecs, groups, people = create_people_data(people_list_file, placement_list_file)
    G = create_network(avecs, groups, people)
    triage_seating_orders(G)

    draw_network(G)
    return 0


if __name__ == '__main__':
    globals()[sys.argv[1]]()