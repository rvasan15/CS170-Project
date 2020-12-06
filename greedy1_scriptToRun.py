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
    for i in range(225, 243):
        if i == 235: continue
        G, s = parse.read_input_file("inputs/large-" + str(i) + ".in")
        maxHapp = float("-inf")
        for _ in range(1, 31):
            rooms_to_students = solver.greedy_solve_1(G, s)
            D = utils.convert_dictionary(rooms_to_students)
            H = utils.calculate_happiness(D, G)
            if H > maxHapp:
                maxHapp = H
                parse.write_output_file(D, "outputs/large-" + str(i) + ".out")
        print(maxHapp)

def greedy_solve_2_script():
    files_to_skip = [12, 17, 56, 135]
    for i in range(142, 243):
        print("===================================")
        print("Determining happiness for file ", i, "...")
        print("===================================")
        if (i in files_to_skip):
            continue
        try:
            G, s = parse.read_input_file("inputs/large-" + str(i) + ".in")
        except (FileNotFoundError):
            continue

        maxHapp = float("-inf")
        for _ in range(1, 501):
            #try:
            rooms_to_students = solver.greedy_solve_2(G, s)
            path = "outputs/large-" + str(i) + ".out"
            utils.make_output_from_dict(rooms_to_students, path, G, s)
            #except(FileNotFoundError, ValueError, AssertionError, RuntimeError):
            #    continue
            """
            D = utils.convert_dictionary(rooms_to_students)
            H = utils.calculate_happiness(D, G)
            if H > maxHapp:
                maxHapp = H
                parse.write_output_file(D, "outputs/large-" + str(i) + ".out")
            """
        #print(maxHapp)

#greedy_solve_2_script()
