import networkx as nx
import parse
from utils import is_valid_solution, calculate_happiness
import sys


def make_input_one(n, path):
    """
    Auto generates input #1 (see below notes) based on number of students
    Args:
        n: number of students
        path: str, a filepath to create file
    Creates:
        input file (i.e. path.in) by using parse.write_input_file(G, budget, path)
    """

    # TODO: your code here!
    pass


    """
    Phase 1 Thoughts:

    Possible inputs
     - s_max = n, students give lots of stress & no happiness to each other -->
       each student in own breakout room


    5 students
    s_max =

    1 2  h s  h/s

    0 1  1 2  0.5
    0 2  2 3  0.6
    0 3  3 4  0.75
    0 4  1 4  0.25
    1 2  2 5  0.4
    1 3  5 2  2.5
    1 4  3 2  1.5
    2 3  3 1  3
    2 4  1 0  infinity
    3 4  0 3  0


    0: 0, 3


    ========== INPUT #1 ==========
    #### INPUT TO CONSIDER ####
    6 students
    s_max = 9 (they key is to make s_max/k = max(s) + 1 i.e. constrain s.t. size(room) <= 2 for all rooms)

    1 2  h s

    0 1  1 2
    0 2  2 2
    0 3  3 2
    0 4  3 2
    0 5  2 2
    1 2  1 2
    1 3  1 2
    1 4  1 2
    1 5  2 2
    2 3  3 2
    2 4  2 2
    2 5  2 2
    3 4  3 2
    3 5  1 2
    4 5  2 2


    0: 0, 3
    1: 1, 5
    2: 2, 4
    h = 3 + 2 + 2 = 7

    Optimal:
    0: 0, 4
    1: 2, 3
    2: 1, 5
    h = 3 + 3 + 2 = 8





    ========== INPUT #2 ==========
    ### Doesn't really feel like a hard input ###
    6 students
    s_max = 10
    k = 3
    s_max/k = 3.3333

    1 2  h s

    0 1  5 1
    0 2  5 4
    0 3  5 4
    0 4  5 5
    0 5  5 2
    1 2  5 3
    1 3  5 2
    1 4  5 3
    1 5  5 4
    2 3  5 2
    2 4  5 1
    2 5  5 4
    3 4  5 2
    3 5  5 1
    4 5  5 3

    0: 0, 1     s = 1
    1: 3, 5     s = 1
    2: 2, 4     s = 1
    h = 15


    0: 2, 3, 4  s = 2 + 2 + 1 = 5
    1: 0, 1, 5  s = 1 + 2 + 4 = 7
    h = 30




    ========== INPUT #3 ==========
    ### Might trick algo that tries to sort by stress level instead of happiness ###
    6 students
    s_max = 22 (possible idea: what if s_max = 70?)
    k = 2
    s_max/k = 11


    1 2  h s

    0 1  1 1
    0 2  2 3
    0 3  3 4
    0 4  2 2
    0 5  4 3
    1 2  2 2
    1 3  5 4
    1 4  2 2
    1 5  3 5
    2 3  4 3
    2 4  2 1
    2 5  3 1
    3 4  5 2
    3 5  2 3
    4 5  3 4

    Answers (i.e. most optimal, not necessarly picked by computer)
    0: 3, 4, 2     s = 2 + 3 + 1 = 6
    1: 0, 5, 1     s = 3 + 1 + 5 = 9
    h = 11 + 8 = 19

    0: 1, 3, 4     s = 4 + 2 + 2 = 8
    1: 2, 5, 0     s = 1 + 3 + 3 = 7
    h = 12 + 9 = 21

    0: 0, 1, 2, 4  s = 11
    1: 3, 5        s = 3
    h = 5 + 4 + 2 + 2 = 13


    Should we create a brute force solution to verify the optimality of the solutions we eyeballed?




    ========== INPUT #4 ==========
    #### INPUT TO CONSIDER ####
    (Note: Probably hard to replicate for 10 people, probably requires more trial and error to find optimal solution that would trick algo)
    6 students
    s_max = 24
    k = 3
    s_max/k = 8


    1 2  h s

    0 1  1 3
    0 2  2 4
    0 3  3 6
    0 4  4 7
    0 5  6 8
    1 2  6 9
    1 3  7 8
    1 4  8 7
    1 5  9 6
    2 3  8 5
    2 4  7 4
    2 5  6 3
    3 4  5 2
    3 5  4 1
    4 5  3 2

    0: 1, 5      s = 6
    1: 2, 3      s = 5
    2: 0, 4      s = 7

    h = 9 + 8 + 4 = 21

    0: 2, 3     s = 5
    1: 1, 4     s = 7
    0: 0, 5     s = 8
    h = 8 + 8 + 5 = 22





    ========== INPUT #5 ==========
    ### Could be used for 20, might be a little hard to replicate ###
    (s = h-c where 0 ≤ c ≤ 100, s_max constrains breakout rooms to 3 people/room)
    6 students
    s_max = 24
    k = 3
    s_max/k = 8


    1 2  h s

    0 1  1 9
    0 2  9 1
    0 3  9 1
    0 4  9 1
    0 5  9 1
    1 2  1 9
    1 3  1 9
    1 4  1 9
    1 5  1 9
    2 3  7 3
    2 4  7 3
    2 5  7 3
    3 4  2 8
    3 5  3 7
    4 5  2 8

    Optimal
    0: 0, 2, 4      s = 1 + 3 + 1 = 5
    1: 3, 5         s = 7
    2: 1
    h = 9 + 9 + 7 + 3 = 28

    Scenario #1
    0: 0, 2, 3      s = 1 + 3 + 1
    1: 4, 5         s = 8
    2: 1
    h = 9 + 9 + 7 + 2 = 27

    Scenario #2
    0: 0, 2, 5      s = 1 + 3 + 1 = 5
    1: 3, 4         s = 8
    2: 1
    h = 9 + 9 + 7 + 2 = 27

    Scenario #3 = Scenario #2
    0: 0, 5, 2
    1: 3, 4
    2: 1
    h =







    ========== INPUT #6 ==========
    (another input: h/s is equal for everyone)
























    """












def brute_force_solution(G, s):
    """
    Brute force solution to rest optimality of our input/output files
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
