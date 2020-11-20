import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys


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
