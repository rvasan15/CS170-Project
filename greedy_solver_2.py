import networkx as nx
from parse import read_input_file, write_output_file
import utils
import random, sys, math
import os
from utils import is_valid_solution, calculate_happiness
import sys
from os.path import basename, normpath
import glob

"""
Assigns students based on largest happiness values. If stress levels exceeded, removes
students that cause most stress in each room and adds them back to list of unassigned
students, and continues assigning students. Assign students until all students assigned
"""


def greedy_solve_2(G, s, assigned_students=[], room_to_students={0:[]}, happy_edgeList=[]):
    """
    Probably open 1 room, add as many possible students w/o exceeding stress level, then
    if s_level exceeded, remove students that cause most stress, open 2 room, repeat
     - Remember to sort students (or sort edgelist or somt) and break ties by happiness
     - Will probably need algo to determine which student causes most stress in given room
    Helpful Utils:
     - utils.calculate_stress_for_room(arr, G)
    """
    #print("assigned_students: ", assigned_students)
    #print("room_to_students: ", room_to_students)
    #print("happy_edgeList: ", happy_edgeList)
    #Iterate by opening 1 breakout room at a time, up to n breakout rooms
    room_to_students_to_return = {}
    max_happy = -1
    #assigned_students = []
    i = 1
    #room_to_students = {}
    #for j in range(i):
    #    room_to_students[j] = []

    #print("room_to_students: ", room_to_students)
    #Make copy of graph (so we can use actual graph later on as reference)
    G_copy = nx.Graph(G)

    #Create edgeList pairs of students sorted by stress/happiness
    stress_edgeList = sorted(G_copy.edges, key=lambda x: G_copy.edges[x]["stress"], reverse = True)
    if ((happy_edgeList == []) or (len(happy_edgeList) == 0) or (happy_edgeList == None)):
        #print("I made it!")
        happy_edgeList = sorted(G_copy.edges, key=lambda x: G_copy.edges[x]["happiness"], reverse = True)
    #Todo: Maybe sort/solve based on some values/prioerities i.e. a * happy - b * stress, a & b can be constants passed in or randInts


    #dictionary of happiness values to list of all students that have same happiness value
    happy_dict = {}
    for edge in happy_edgeList:
        #print("edge: ", edge)
        #print("happiness: ", G_copy.edges[edge]["happiness"])
        if G_copy.edges[edge]["happiness"] in happy_dict:
            happy_dict[G_copy.edges[edge]["happiness"]] += [edge]
        else:
            happy_dict[G_copy.edges[edge]["happiness"]] = []
            happy_dict[G_copy.edges[edge]["happiness"]] += [edge]

    while (len(assigned_students) < len(list(G.nodes))):
        #print("im in", len(assigned_students))

        stress_edgeList = sorted(stress_edgeList, key=lambda x: G_copy.edges[x]["stress"], reverse = True)
        happy_edgeList = sorted(happy_edgeList, key=lambda x: G_copy.edges[x]["happiness"], reverse = True)

        #dictionary of happiness values to list of all students that have same happiness value
        happy_dict = {}
        for edge in happy_edgeList:
            #print("edge: ", edge)
            #print("happiness: ", G_copy.edges[edge]["happiness"])
            if G_copy.edges[edge]["happiness"] in happy_dict:
                happy_dict[G_copy.edges[edge]["happiness"]] += [edge]
            else:
                happy_dict[G_copy.edges[edge]["happiness"]] = []
                happy_dict[G_copy.edges[edge]["happiness"]] += [edge]



        #Assign students until all pairings are broken or assigned (i.e. all students in rooms)
        while (len(assigned_students) < len(list(G.nodes))):


            #Take happiest pair and try to assign them to rooms to maximize happiness
            #print(happy_dict)
            student_pair = None
            """
            for key in sorted(happy_dict.keys()):
                #print("key: ", key)
                #print("happy_dict[key]: ", happy_dict[key])
                if (len(happy_dict[key]) > 0):

                    student_pair = random.sample(happy_dict[key], 1)
                    #print(student_pair[0])
                    happy_dict[key].remove(student_pair[0])

            #student_pair = happy_edgeList.pop(0)

            # No more student pairs – shouldn't really hit this point tho??
            if (not student_pair):
                print("here")
                #for key in sorted(happy_dict.keys()):
                    #print("key: ", key)
                    #if (len(happy_dict[key]) > 0):

                        #print("happy_dict[key]: ", happy_dict[key])

                break

            student_pair = student_pair[0]
            """
            #Todo: Does this always pick happiest?
            pop_amt = min(len(happy_edgeList), 5)
            if (pop_amt <= 0):
                break
            #print("assigned_students: ", assigned_students)
            #print("room_to_students: ", room_to_students)
            #print("happy_edgeList: ", happy_edgeList)
            student_pair = happy_edgeList.pop(random.randint(0, pop_amt-1)) # ToDo: Maybe increase this value to 5 - 10?
            #print("num assigend students: ", len(assigned_students))
            #print("student_pair: ", student_pair)
            #print("happy val: ", G_copy.edges[student_pair]["happiness"])
            student0 = student_pair[0]
            student1 = student_pair[1]


            #Check if students have been assigned
            student0_assigned = (student0 in assigned_students)
            student1_assigned = (student1 in assigned_students)
            #If students are already assigned (whether in same or diff room), go to next happiest pair
            if (student0_assigned and student1_assigned):
                #print("here0")
                continue





            #Check which room the students are in, if they have already been asigned to a room
            room_of_student0 = -1
            room_of_student1 = -1
            for room in room_to_students:
                if student0 in room_to_students[room]:
                    room_of_student0 = room
                if student1 in room_to_students[room]:
                    room_of_student1 = room

            #If student0 assigned, try to put student1 in same room, else put in room that causes least stress
            if (student0_assigned):
                #print("here1")
                #print("room_of_student0: ", room_of_student0)
                room_to_students[room_of_student0] += [student1]

                assigned_students += [student1]
                valid0 = utils.is_valid_solution(utils.convert_dictionary(room_to_students), G, s, i)
                if (valid0):
                    continue

                #Can't put student1 in same room, so try to put in diff room
                room_to_students[room_of_student0].remove(student1)
                assigned_students.remove(student1)

                min_stress1 = float('inf')
                min_room1 = -1
                for room in room_to_students:
                    room_to_students[room] += [student1]

                    #check if adding students to this room causes minimum stress (disruption?)
                    temp_stress1 = utils.calculate_stress_for_room(room_to_students[room], G)
                    #check if solution is valid when adding students to this room
                    valid1 = utils.is_valid_solution(utils.convert_dictionary(room_to_students), G, s, i)
                    if (temp_stress1 < min_stress1 and valid1):
                        min_stress1 = temp_stress1
                        min_room1 = room

                    room_to_students[room].remove(student1)

                if (min_room1 >= 0):
                    room_to_students[min_room1] += [student1]
                    assigned_students += [student1]
                else:
                # at this point, student1 cant be assigned to any room without causing excess stress,
                # so this solution/number of breakout rooms cannot work, so try opening more rooms
                    #print("I got here2, assigned_students = ", assigned_students)
                    #break
                    happy_edgeList = remove_students_greedy(G, G_copy, s, room_to_students, happy_dict, assigned_students, happy_edgeList)
                    continue

            #If student1 assigned, try to put student0 in same room, else put in room that causes least stress
            if (student1_assigned):
                #print("here2")
                #print("room_of_student1: ", room_of_student1)
                room_to_students[room_of_student1] += [student0]
                assigned_students += [student0]
                valid1 = utils.is_valid_solution(utils.convert_dictionary(room_to_students), G, s, i)
                if (valid1):
                    continue

                #Can't put student1 in same room, so try to put in diff room
                room_to_students[room_of_student1].remove(student0)
                assigned_students.remove(student0)

                min_stress0 = float('inf')
                min_room0 = -1
                for room in room_to_students:
                    room_to_students[room] += [student0]

                    #check if adding students to this room causes minimum stress (disruption?)
                    temp_stress0 = utils.calculate_stress_for_room(room_to_students[room], G)
                    #check if solution is valid when adding students to this room
                    valid0 = utils.is_valid_solution(utils.convert_dictionary(room_to_students), G, s, i)
                    if (temp_stress0 < min_stress0 and valid0):
                        min_stress0 = temp_stress0
                        min_room0 = room

                    room_to_students[room].remove(student0)

                if (min_room0 >= 0):
                    room_to_students[min_room0] += [student0]
                    assigned_students += [student0]
                else:
                # at this point, student1 cant be assigned to any room without causing excess stress,
                # so this solution/number of breakout rooms cannot work, so try opening more rooms
                    #print("I got here4, assigned_students = ", assigned_students)
                    #break
                    happy_edgeList = remove_students_greedy(G, G_copy, s, room_to_students, happy_dict, assigned_students, happy_edgeList)
                    continue


            if (not student1_assigned and not student0_assigned):
                #print("here5")

                #If neither student assigned, put both into the breakout room that creates least stress
                #If putting them into a breakout room together always creates invalid solution, consider putting them into seperate rooms
                min_stress = float('inf')
                min_room = -1
                for room in room_to_students:
                    room_to_students[room] += [student0]
                    room_to_students[room] += [student1]

                    #check if adding students to this room causes minimum stress (disruption?)
                    temp_stress = utils.calculate_stress_for_room(room_to_students[room], G)
                    #check if solution is valid when adding students to this room
                    valid = utils.is_valid_solution(utils.convert_dictionary(room_to_students), G, s, i)
                    if (temp_stress < min_stress and valid):
                        min_stress = temp_stress
                        min_room = room

                    room_to_students[room].remove(student0)
                    room_to_students[room].remove(student1)

                if (min_room >= 0):
                    room_to_students[min_room] += [student0]
                    room_to_students[min_room] += [student1]
                    assigned_students += [student0]
                    assigned_students += [student1]
                    continue

                #if putting students together in breakout room still causes excess stress, put them in diff rooms
                min_stress0 = float('inf')
                min_room0 = -1

                for room in room_to_students:
                    room_to_students[room] += [student0]

                    #check if adding students to this room causes minimum stress (disruption?)
                    temp_stress0 = utils.calculate_stress_for_room(room_to_students[room], G)
                    #check if solution is valid when adding students to this room
                    valid0 = utils.is_valid_solution(utils.convert_dictionary(room_to_students), G, s, i)
                    if (temp_stress0 < min_stress0 and valid0):
                        min_stress0 = temp_stress0
                        min_room0 = room

                    room_to_students[room].remove(student0)



                min_stress1 = float('inf')
                min_room1 = -1

                for room in room_to_students:
                    room_to_students[room] += [student1]

                    #check if adding students to this room causes minimum stress (disruption?)
                    temp_stress1 = utils.calculate_stress_for_room(room_to_students[room], G)
                    #check if solution is valid when adding students to this room
                    valid1 = utils.is_valid_solution(utils.convert_dictionary(room_to_students), G, s, i)
                    if (temp_stress1 < min_stress1 and valid1):
                        min_stress1 = temp_stress1
                        min_room1 = room

                    room_to_students[room].remove(student1)

                if (min_room1 >= 0):
                    room_to_students[min_room1] += [student1]
                    assigned_students += [student1]
                if (min_room0 >= 0):
                    room_to_students[min_room0] += [student0]
                    assigned_students += [student0]
                else:
                    #continue
                # at this point, student0 cant be assigned to any room without causing excess stress,
                # so this solution/number of breakout rooms cannot work, so remove students
                # that cause stress level to exceed room stress level, put them back into
                # happiness edgelist and dictionary, and then continue from there



                    happy_edgeList = remove_students_greedy(G, G_copy, s, room_to_students, happy_dict, assigned_students, happy_edgeList)

                    #print("I got here, assigned_students = ", assigned_students)
                    #break
                    continue














        #print("here3")

        valid_sol = utils.is_valid_solution(utils.convert_dictionary(room_to_students), G, s, len(room_to_students))
        happy = utils.calculate_happiness(utils.convert_dictionary(room_to_students), G)
        if (len(assigned_students) < len(list(G.nodes))):
            #print(room_to_students)
            happy = float('-inf')

        #print("room_to_students: ", room_to_students)

        #print("room_to_students: ", room_to_students)
        #print("happy: ", happy)
        if (happy > max_happy and valid_sol):
            max_happy = happy
            room_to_students_to_return = {}
            for room in room_to_students:
                room_to_students_to_return[room] = room_to_students[room].copy()
        elif (not valid_sol):
            happy_edgeList = remove_students_greedy(G, G_copy, s, room_to_students, happy_dict, assigned_students, happy_edgeList)
        #elif ((happy < max_happy) and (len(room_to_students) < 50)):
            #happy_dict = remove_students_greedy(G, G_copy, s, room_to_students, happy_dict, assigned_students, happy_edgeList)
        #else:
            #break

        if (len(happy_edgeList) <= 0):
            break

    #print("here4")
    print("happy for ", len(room_to_students), " rooms: ", max_happy)
    return room_to_students_to_return






def remove_students_greedy(G, G_copy, s, room_to_students, happy_dict, assigned_students, happy_edgeList):
    # Check which rooms exceed stress limit
    #print("in remove_students_greedy")
    counter = 0
    while True:
        #print("here: ", counter)
        room_numbers_that_exceed_stress = []
        for room in room_to_students:
            s_room = utils.calculate_stress_for_room(room_to_students[room], G)
            if (s_room >= (s/(len(room_to_students)))): #ToDo: should this be i or i+1? Think of 50 room case
                room_numbers_that_exceed_stress += [room]

        # From the rooms that exceed stress limit, remove students until all stress limit not exceeded
        removed_students = []
        for room in room_numbers_that_exceed_stress:
            s_room = utils.calculate_stress_for_room(room_to_students[room], G)
            while (s_room >= (s/(len(room_to_students)))):
                min_stress = float("inf")
                student_to_remove = -1
                for i in range(len(room_to_students[room])):

                    student = room_to_students[room].pop(i)
                    if (utils.calculate_stress_for_room(room_to_students[room], G) < min_stress):
                        min_stress = utils.calculate_stress_for_room(room_to_students[room], G)
                        student_to_remove = student
                    room_to_students[room].insert(i, student)

                room_to_students[room].remove(student_to_remove)
                removed_students += [student_to_remove]
                s_room = utils.calculate_stress_for_room(room_to_students[room], G)

        for i in range(len(removed_students)-1):
            for j in range(i+1, len(removed_students)):
                edge = (removed_students[i], removed_students[j])
                if (edge[0] == edge[1]):
                    continue
                #print(edge)
                happy_edgeList += [edge]
                if G_copy.edges[edge]["happiness"] in happy_dict:
                    happy_dict[G_copy.edges[edge]["happiness"]] += [edge]
                else:
                    happy_dict[G_copy.edges[edge]["happiness"]] = []
                    happy_dict[G_copy.edges[edge]["happiness"]] += [edge]

        happy_edgeList = sorted(happy_edgeList, key=lambda x: G_copy.edges[x]["happiness"], reverse = True)

        for student in removed_students:
            assigned_students.remove(student)


        #open another room
        if (len(room_to_students) < 50):
            room_to_students[len(room_to_students)] = []

        counter += 1
        if (utils.is_valid_solution(utils.convert_dictionary(room_to_students), G, s, len(room_to_students))):
            #print("why you always breakin")
            #print("This is valid? wyd: ", room_to_students)
            #print("How did you get this kinda happiness?: ", utils.calculate_happiness(utils.convert_dictionary(room_to_students), G))
            #print("Did you assign everyone tho: ", assigned_students)
            #print("Did you assign everyone tho pt 2: ", len(assigned_students))
            break
    #print("done with remove_students_greedy")
    return happy_edgeList
