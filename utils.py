import networkx as nx
import parse
#from parse import write_output_file

def is_valid_solution(D, G, s, rooms):
    """
    Checks whether D is a valid mapping of G, by checking every room adheres to the stress budget.
    Args:
        D: Dictionary mapping student to room
        G: networkx.Graph
        s: Stress budget
        rooms: Number of breakout rooms

    Returns:
        bool: whether D is a valid solution
    """
    room_budget = s/rooms
    room_to_student = {}
    for k, v in D.items():
        room_to_student.setdefault(v, []).append(k)

    for k, v in room_to_student.items():
        room_stress = calculate_stress_for_room(v, G)
        if room_stress > room_budget:
            return False
    return True


def calculate_happiness(D, G):
    """
    Calculates the total happiness in mapping D by summing the happiness of each room.
    Args:
        D: Dictionary mapping student to room
        G: networkx.Graph
        s: Stress budget
        k: Number of breakout rooms

    Returns:
        float: total happiness
    """
    room_to_s = {}
    for k, v in D.items():
        room_to_s.setdefault(v, []).append(k)

    happiness_total = 0
    for k, v in room_to_s.items():
        room_happiness = calculate_happiness_for_room(v, G)
        happiness_total += room_happiness
    return happiness_total

def convert_dictionary(room_to_student):
    """
    Converts the dictionary mapping room_to_student to a valid return of the solver
    Args:
        room_to_student: Dictionary of room to a list of students
    Returns:
        D: Dictionary mapping student to room
    e.g {0: [1,2,3]} ==> {1:0, 2:0, 3:0}
    """
    d = {}
    for room, lst in room_to_student.items():
        for student in lst:
            d[student] = room
    return d

def convert_list_to_dictionary(list_of_rooms):
    """
    Converts list of rooms and students to the dictionary mapping room_to_student
    Args:
        list_of_rooms: List of lists (i.e. rooms) that contain numbers (i.e. students)

    Returns:
        room_to_student: Dictionary of room to a list of students
    e.g [[1, 2, 3], [4, 5]] ==> {0: [1,2,3], 1: [4, 5]}
    """
    d = {}
    for i in range(len(list_of_rooms)):
        d[i] = list_of_rooms[i].copy()
    return d

def make_output_from_list(lst, path):
    """
    Converts the list of students in rooms to a valid return of the solver and writes to
    output file
    Args:
        lst: List of lists (i.e. rooms) that contain numbers (i.e. students)
        path: filepath to output file to write dictionary output
    """
    dict = {}
    for i in range(len(lst)):
        for item in lst[i]:
            dict[item] = i
    dict2 = {}
    for i in sorted(dict.keys()):
        dict2[i] = dict[i]
    write_output_file(dict2, path)

def make_output_from_dict(rooms_to_students, path, G, s):
    """
    Converts the dictionary of rooms to students to a valid return of the solver and writes to
    output file
    Args:
        rooms_to_students: Dictionary of room to a list of students
        path: filepath to output file to write dictionary output
    """
    dct = convert_dictionary(rooms_to_students)

    try:
        din = parse.read_output_file(path, G, s)
    except (FileNotFoundError, AssertionError):
        if (len(rooms_to_students) <= 0):
            print("Empty Room Configuration")
            return
        if (is_valid_solution(dct, G, s, len(rooms_to_students))):
            parse.write_output_file(dct, path)
        D = parse.read_output_file(path, G, s)
        happy2 = calculate_happiness(D, G)
        print("current happiness of this file: ", happy2)
        return




    happy0 = calculate_happiness(din, G)
    happy1 = calculate_happiness(dct, G)
    #print("happiness of previous configuration: ", happy0)
    #print("happiness of this configuration: ", happy1)

    if ((happy1 > happy0) and (is_valid_solution(dct, G, s, len(rooms_to_students)))):
        print("Valid")
        parse.write_output_file(dct, path)

    D = parse.read_output_file(path, G, s)
    happy2 = calculate_happiness(D, G)
    print("current happiness of this file: ", happy2)

    assert(max(happy1, happy0) == happy2)


def calculate_stress_for_room(arr, G):
    """
    Given an array of students in to be placed in a room, calculate stress for the room.
    Args:
        arr: Array of students
        G: Original graph
    Returns:
        room_stress: Stress value of the room
    """
    H = G.subgraph(arr)
    return H.size("stress")

def calculate_happiness_for_room(arr, G):
    """
    Given an array of students in to be placed in a room, calculate happiness for the room.
    Args:
        arr: Array of students
        G: Original graph
    Returns:
        room_happiness: Happiness value of the room
    """
    H = G.subgraph(arr)
    return H.size("happiness")
