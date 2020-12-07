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
    files_to_skip = [7, 10, 11, 12, 18, 29, 31, 33, 44, 51, 54, 56, 60, 65, 71, 72, 73,
                    76, 77, 78, 81, 103, 110, 112, 121, 123, 125, 129, 131, 134, 135, 138,
                    151, 154, 165, 169, 173, 174, 178, 184, 187, 194, 196, 199, 201, 202, 203,
                    208, 213, 215, 218, 219, 224, 231, 233, 235]
    files_to_run = [i+1 for i in range(242)]
    for i in range(1, 243):
        print("======================================")
        print("Determining happiness for file ", i, "...")
        print("======================================")
        if ((i in files_to_skip) or (i not in files_to_run)):
            continue
        try:
            G, s = parse.read_input_file("inputs/large-" + str(i) + ".in")
        except (FileNotFoundError):
            continue

        maxHapp = float("-inf")
        for _ in range(100):
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

def greedy_solve_5_script():
    files_to_skip = [12, 17, 56, 135]
    for i in range(1, 243):
        print("======================================")
        print("Determining happiness for file ", i, "...")
        print("======================================")
        if (i in files_to_skip):
            continue
        try:
            G, s = parse.read_input_file("inputs/large-" + str(i) + ".in")
        except (FileNotFoundError):
            continue

        maxHapp = float("-inf")
        for _ in range(100):
            #try:
            rooms_to_students = solver.greedy_solve_5(G, s)
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

greedy_solve_2_script()
