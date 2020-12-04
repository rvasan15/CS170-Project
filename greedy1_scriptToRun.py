import networkx as nx
import parse
from parse import read_input_file, write_output_file
import utils
import random, sys, math
import os
from utils import is_valid_solution, calculate_happiness
import sys
from os.path import basename, normpath
import glob
import solver

def greedy1_script():
    for i in range(1, 237):
        G, s = parse.read_input_file("inputs/large-" + str(i) + ".in")

        maxHapp = float("-inf")
        for _ in range(1, 101):
            rooms_to_students = solver.greedy_solve_2(G, s)
            D = utils.convert_dictionary(rooms_to_students)
            H = utils.calculate_happiness(D, G)
            if H > maxHapp:
                maxHapp = H
                parse.write_output_file(D, "outputs/large-" + str(i) + ".out")
        print(maxHapp)