#import networkx as nx
from create_people_data import create_people_data
from create_seating_order import create_seating_order

def main():
    people_list_file = ""
    placement_list_file = "test_groups.txt"
    avecs, groups, people = create_people_data(people_list_file, placement_list_file)
    create_seating_order(avecs, groups, people)
    return 0

main()