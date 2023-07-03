from create_test_data import create_person_list

def create_people_data(people_list_file, placement_list_file):
    people = read_people(people_list_file, True)
    avecs, groups = read_placements(placement_list_file, people)
    remove_non_participants(groups, people)
    return avecs, groups, people

def read_people(people_list_file, is_a_test):
    people = []
    if is_a_test:
        people = create_person_list(n=30)
    return people

def read_placements(filename, people):
    file = open(filename, 'r')
    avecs = find_avecs(file, people)
    groups = find_groups(file, people)
    return avecs, groups
    
def find_avecs(file, people):
    row = readline_and_strip(file)
    if row != "#Avecs":
        print("No avecs were listed")
        return []
    avecs = []
    row = readline_and_strip(file)
    while ";" in row:
        pair = split_avecs_on_row(row)
        pair[0] = pair[0].strip()
        pair[1] = pair[1].strip()
        if pair[0] in people and pair[1] in people:
            avecs.append(pair)
        row = readline_and_strip(file)
    return avecs

def find_groups(file, people):
    groups = []
    row = readline_and_strip(file)
    while row:
        if "#" not in row and row in people:
            groups.append(read_group(file, row))
        row = readline_and_strip(file)
    return groups

def remove_non_participants(groups, people):
    for group in groups:
        for i in group:
            if i not in people:
                group.remove(i)

def read_group(file, row):
    group = []
    while "#" not in row and row:
        group.append(row)
        row = readline_and_strip(file)
    return group

def split_avecs_on_row(row):
    return row.rstrip().rsplit(';')

def readline_and_strip(file):
    return file.readline().strip()
