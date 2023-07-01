def create_test_person(person_identifier, i):
    return person_identifier + " " + str(i)

def create_person_list(n):
    people = []
    default_name = "person"
    for i in range(n):
        people.append(create_test_person(default_name, i))
    return people