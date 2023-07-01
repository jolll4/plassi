def create_seating_order(avecs, groups, people):
    adjacent_groups = find_avecs_in_different_groups(avecs, groups)
    pairs_where_only_one_in_group = find_pairs_where_only_one_in_group(avecs, groups)
    print(adjacent_groups)
    print(pairs_where_only_one_in_group)

def find_avecs_in_different_groups(avecs, groups):
    adjacent_groups = []
    for pair in avecs:
        for group in groups:
            if (pair[0] in group and pair[1] not in group):
                find_other_group(adjacent_groups, pair[0], pair[1], group, groups)
            elif (pair[0] not in group and pair[1] in group):
                find_other_group(adjacent_groups, pair[1], pair[0], group, groups)
    
    remove_duplicate_group_pairs(adjacent_groups)
    return adjacent_groups

def find_other_group(adjacent_groups, person1, person2, group, groups):
    for second_group in groups:
        if person1 in group and person2 in second_group:
            adjacent_groups.append([groups.index(group), groups.index(second_group)])

def remove_duplicate_group_pairs(adjacent_groups):
    for i in adjacent_groups:
        for j in adjacent_groups:
            if i[0] == j[1] and i[1] == j[0]:
                adjacent_groups.remove(j)

def find_pairs_where_only_one_in_group(avecs, groups):
    pairs = []
    for pair in avecs:
        for group in groups:
            if pair[0] in group and pair[1] not in group:
                if(check_that_other_person_not_in_any_group(pair[1], groups)):
                    pairs.append([pair[0], pair[1]])
            elif pair[0] not in group and pair[1] in group:
                if(check_that_other_person_not_in_any_group(pair[0], groups)):
                    pairs.append([pair[0], pair[1]])
    return pairs

def check_that_other_person_not_in_any_group(person2, groups):
    for group in groups:
        if person2 in group:
            return False
    return True