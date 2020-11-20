import networkx as nx
import parse
from utils import is_valid_solution, calculate_happiness
import sys


def make_an_input(n, path):
    """
    Auto generates a input file based on number of  students
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


    #### INPUT TO CONSIDER ####
    6 students
    s_max = 9

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














    """
