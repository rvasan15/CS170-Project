import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import random, sys, math




def brute_solve(G, s):
    """
    Brute force solves G to find most optimal solution
    """

    all_possible_combinations = {} # maps a particular combination to happiness
    num_open_rooms = 1
    students = list(G.nodes)


    while (num_open_rooms <= len(students)):
        rooms = []
        for _ in range(num_open_rooms):
            rooms.append([])
        all_possible_combinations = recursive_fill_rooms(rooms, students, s, all_possible_combinations, G)
        num_open_rooms += 1

    # Find max Happiness and return
    h = 0
    room = None
    for combo in all_possible_combinations:
        if (all_possible_combinations[combo] > h):
            room = combo
            h = all_possible_combinations[combo]
    return room, h


def recursive_fill_rooms(rooms, student_lst, s_max, all_possible_combinations, G):
    #base case of if student_lst is 0 or if rooms is empty or things
    if (len(rooms) <= 0 or len(student_lst) <= 0):
        return all_possible_combinations

    for i in range(len(student_lst)):
        for j in range(len(rooms)):
            student = student_lst.pop(j)
            rooms[i] += [student]
            all_possible_combinations = recursive_fill_rooms(rooms, student_lst, s_max, all_possible_combinations, G)
            for room in rooms:
                h, s = happy_and_stress_of_student_subset(G, room)
            if (s <= s_max/len(rooms)):
                all_possible_combinations[rooms] = h
            student_lst.insert(j, student)


    return all_possible_combinations


def happy_and_stress_of_student_subset(G, student_lst):
    happy = 0;
    stress = 0;
    if (len(student_lst) <= 1):
        return happy, stress
    for i in range(len(student_lst)-1):
        for j in range(i+1, len(student_lst)):
            #print(student_lst[i])
            #print(student_lst[j])
            #print(G[student_lst[i]][student_lst[j]])
            happy += G[student_lst[i]][student_lst[j]]["happiness"]
            stress += G[student_lst[i]][student_lst[j]]["stress"]

    return happy, stress





def brute_solve2(G, s):
    """
    Brute force solves G to find most optimal solution (SPECIFICALLY WITH ON input #1 types)
    To modify code to brute force all possible inputs, change lines 87 (first while loop)
    and 111 (last line of while loop that changes num_open_rooms)
    """

    all_possible_combinations = {} # maps a particular combination to happiness
    students = list(G.nodes)
    num_open_rooms = int(ceil(len(students)/2))
    lst_combos = []
    h = -1
    best_rooms = []


    while (num_open_rooms >= int(ceil(len(students)/2))):
        rooms = []
        for _ in range(num_open_rooms):
            rooms.append([])



        assigned_students = []

        room_temp, h = recursive_fill_rooms2(rooms, students, all_possible_combinations, G, s, best_rooms, h, assigned_students)
        #best_rooms = room_temp.copy()

        best_rooms = []
        for i in range(len(room_temp)):
            best_rooms += [room_temp[i]].copy()

        print("here3")
        print(best_rooms)
        #lst_combos += lst
        #all_possible_combinations.update(dct)


        #all_possible_combinations = recursive_fill_rooms(rooms, students, s, all_possible_combinations, G)
        num_open_rooms = int(ceil(num_open_rooms/2))

    """

    for i in range(len(lst_combos)):
        if (all_possible_combinations[i] > h):
            room = lst_combos[i]
            h = all_possible_combinations[i]
    """
    return best_rooms, h



def recursive_fill_rooms2(rooms, students, all_possible_combinations, G, s, best_rooms, best_h, assigned_students):

    """
    print()
    print(rooms)
    print(students)
    print(best_rooms)
    print(best_h)
    print()
    """

    h = 0
    s_room = 0
    for room in rooms:

        temp_h, temp_s = happy_and_stress_of_student_subset(G, room)
        h += temp_h
        s_room = max(temp_s, s_room)
    if (s_room > s/len(rooms)):
        return best_rooms, best_h


    if (len(students) <= 0):
        #print("here")

        if (s_room <= s/len(rooms)):
            if (h > best_h):
                #print("here2")
                best_rooms = []
                room_temp = rooms.copy()
                #print(room_temp)
                for i in range(len(rooms)):
                    best_rooms += [rooms[i].copy()]
                #print(best_rooms)
                best_h = h
                #print(best_h)

        #print(lst_combos)
        #for i in range(len(best_rooms)):
            #best_rooms[i] = best_rooms[i].copy()
        return best_rooms.copy(), best_h

    start = -1
    if (assigned_students == []):
        start = 0
    else:
        start = max(assigned_students) + 1

    temp_student = students.copy()

    student = min(students)

    #for student in temp_student:
    for room in rooms:
        students.remove(student)
        room += [student]
        #assigned_students += [student]

        room_temp, best_h = recursive_fill_rooms2(rooms, students, all_possible_combinations, G, s, best_rooms, best_h, assigned_students)
        #best_rooms = room_temp.copy()
        best_rooms = []
        for i in range(len(room_temp)):
            best_rooms += [room_temp[i].copy()]
        #lst_combos += lst
        #all_possible_combinations.update(dct)
        room.pop()
        #assigned_students.pop()
        students.append(student)
    return best_rooms.copy(), best_h







def gamble_solve(G, s, num_open_rooms, reps=100, limit = -1):
    """
    Gambles by randomly assigning students to rooms and checking optimality and stress levels
    Works specifically for input #1 type
     - can be modified by changin num_open_rooms to randint
     - can be modified adding checks before h > best_h to check stress_max val per room
    """

    students = list(G.nodes)
    #num_open_rooms = int(math.ceil(len(students)/2))
    best_h = -1
    best_rooms = []



    for _ in range(reps):
        rooms = []
        for _ in range(num_open_rooms):
            rooms.append([])
        temp_students = students.copy()



        rooms = random_assign(temp_students, rooms, limit)

        h = 0
        s_room = 0
        for room in rooms:

            temp_h, temp_s = happy_and_stress_of_student_subset(G, room)
            h += temp_h
            s_room = max(temp_s, s_room)
        if ((s_room <= s/len(rooms)) and (h > best_h)):
            best_rooms = []
            room_temp = rooms.copy()
            for i in range(len(rooms)):
                best_rooms += [rooms[i].copy()]
            best_h = h

        return best_rooms.copy(), best_h



def random_assign(students, rooms, limit_per_room = -1):

    temp_students = students.copy()

    if (limit_per_room >= 0):
        for room in rooms:
            temp_room = random.sample(temp_students, limit_per_room).copy() #look at this line for copy issue
            for student in temp_room:
                room += [student]
            for student in temp_room:
                temp_students.remove(student)
    else:
        while (len(temp_students) > 0):
            rin = random.randint(0, len(rooms)-1)
            student = random.sample(temp_students, 1)
            rooms[rin] += student
            temp_students.remove(student[0])

    return rooms





def gamble_solve_runner(G, s, num_open_rooms, reps=10, reps_to_run=100, limit = -1):
    best_room = []
    h = -1
    for _ in range(reps_to_run):
        room, hap = gamble_solve(G, s, num_open_rooms, reps, limit=limit)
        if (hap > h):
            best_room = []
            for i in range(len(room)):
                best_room += [room[i].copy()]
            h = hap
    return best_room, h



#Todo: Make solver for test20.in (i.e. input #5) that like "splits" students into high
#stress and high happiness groups, puts high stress students in seperate rooms (and opens
#as many necessary rooms to put high stress students in their own rooms) then assigns
#high happiness students s.t. i is put with j iff j < i, run all possible permutations, calc
def solve_input_five(G, s):
    students = list(G.nodes)
    high_stress_students = [2*i+1 for i in range(len(students)/2)]
    high_happy_students = [2*i for i in range(len(students)/2)]

    best_h = -1
    best_rooms = []

    rooms = []
    for _ in range(len(high_stress_students)):
        rooms.append([])

    for _ in range(len(high_stress_students)):
        rooms[i] += [high_stress_students[i]]



    temp_students = high_happy_students.copy()

#    0123456789
#    13579
#    i
#    2i+1























def make_output_from_list(lst, path):
    dict = {}
    for i in range(len(lst)):
        for item in lst[i]:
            dict[item] = i
    dict2 = {}
    for i in sorted(dict.keys()):
        dict2[i] = dict[i]
    write_output_file(dict2, path)









#TODO: Also write a psuedo greedy solution to optimize for happiness at least for 50


"""
import solver, parse
G, s = parse.read_input_file("test20.in")
room, h = solver.gamble_solve_runner(G, s, 10)

solver.make_output_from_list(room, "test20.out")
"""





















def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """

    # TODO: your code here!
    pass

    # Idea (Deepak): Something like a greedy solution, where we start by opening n/2 breakout rooms
    # and greedily assign student pairs to maximize happiness, and if a room exceeds the
    # stress_budget per room, we reduce the number of rooms (which increases stress/k)
    # and continue assigning student pairs greedily by maximum happiness to the room with
    # the lowest stress level

    """
    Phase 1 thoughts:

    Possible Solutions
     - Subrtact stress from happiness and then apply the "enemies" solution (hw problem)
       while keeping stress levels below s_max/k
     - Randomly greedy: choose student @ random, assign, choose another student @ random,
       assign to any of the existing breakout rooms s.t. s_max/k isn't exceeded, or if
       it is exceeded no matter what, then put student in own breakotu room, recalculate
       s_max/k, remove any students from (other) breakout rooms that exceed this new value
       and reassign them, repeat until all students assigned
     - Bellman Fords/DFS/BFS/other graph solutions?
     - DP: Max happiness with n-1 students or all students except student i (knapsack?)
     - Residual Graph/Flow algorithm (Max Flow problem?) (Probably not)
     - Set Cover/NP Problem? Search Problem?


    Pseudocode for greedy solution:

    num_filled_rooms = 0
    student_stack = {}
    num_unassigned_students = [i for i in range(n)]
    dictionary = {[i : empty set] for i in range(n)}


    while (len(num_unassigned_students) > 0):
        student_to_assign = pick_random_student()
        current_max_happiness = -infinity
        for breakout_room in range(0, num_filled_rooms):
            add student_to_assign to breakout_room
            if (stress(breakout_room) > s_max/num_filled_rooms):
                continue;

            current_max_happiness = max(happiness(breakout_room), current_max_happiness) #also keeep track of which room creates max happiness

        if (current_max_happiness = -inifinty):
            num_filled_rooms += 1
            for breakout_room in range(0, num_filled_rooms):
                while (stress(breakout_room) > s_max/num_filled_rooms):
                    current_min_stress = stress(breakout_room)
                    for student in breakout_room:
                        remove student from breakout_room
                        current_min_stress = min(current_min_stress, stress(breakout_room)) # see line 59 (current_max_happiness)
                    remove student that minimized stress of breakout_room






    """


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G, s = read_input_file(path)
#     D, k = solve(G, s)
#     assert is_valid_solution(D, G, s, k)
#     print("Total Happiness: {}".format(calculate_happiness(D, G)))
#     write_output_file(D, 'out/test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)
