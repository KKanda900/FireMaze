import numpy
import math
import random

dim = 10  # int(input("Enter a dimension"))
prob = .3  # float(input("Enter probability"))


def build_maze(size, probability):
    obstacle_num = 0  # See if the amount of obstacles required are 0 or not
    obstacles = int((size * size) * probability)  # if the maze area is 100 then there should be only 10 obstacles
    tracking_array = numpy.zeros((size, size))  # track where the obstacles are places so it doesn't double count
    while obstacles != 0:
        for i in range(0, size):
            for j in range(0, size):
                if i == 0 and j == 0:  # this is what we will define as a start node with yellow

                    pass
                elif i == size - 1 and j == size - 1:
                    pass
                else:
                    arr = [0, 1]  # these will represent random choices
                    if random.choice(arr) == 0 and obstacles != 0 and tracking_array[i][j] == 0:
                        tracking_array[i][j] = 1
                        obstacles -= 1
    print(tracking_array)
    return tracking_array


def a_star(maze_array, n):

    fringe = []
    visited = [[-1, -1, -1]]
    child1 = []
    child2 = []
    child3 = []
    child4 = []
    start = [0, 0, math.sqrt(2*((n-1)**2))]
    goal = [n - 1, n - 1, 0]
    tracker = [start]
    fringe.append(start)
    while len(fringe) > 0:
        current = fringe.pop(0)
        if len(child1) != 0:
            child1.pop()
        if len(child2) != 0:
            child2.pop()
        if len(child3) != 0:
            child3.pop()
        if len(child4) != 0:
            child4.pop()
        if not fringe:
            if current[0] != 0 and maze_array[current[0] - 1][current[1]] != 1 and current not in visited:
                temp = [current[0] - 1, current[1]]
                child1.append([current[0] - 1, current[1], distance_calculator(temp, goal)])  # top
                fringe = sorting(fringe, child1)
            if current[1] != n - 1 and maze_array[current[0]][current[1] + 1] != 1 and current not in visited:
                temp = [current[0], current[1] + 1]
                child2.append([current[0], current[1] + 1, distance_calculator(temp, goal)])  # right
                fringe = sorting(fringe, child2)
            if current[0] != n - 1 and maze_array[current[0] + 1][current[1]] != 1 and current not in visited:
                temp = [current[0] + 1, current[1]]
                child3.append([current[0] + 1, current[1], distance_calculator(temp, goal)])  # bottom
                fringe = sorting(fringe, child3)
            if current[1] != 0 and maze_array[current[0]][current[1] - 1] != 1 and current not in visited:
                temp = [current[0], current[1] - 1]
                child4.append([current[0], current[1] - 1, distance_calculator(temp, goal)])  # left
                fringe = sorting(fringe, child4)
        else:
            if current[0] != 0 and maze_array[current[0] - 1][current[1]] != 1 and current not in visited and current not in fringe:
                temp = [current[0] - 1, current[1]]
                child1.append([current[0] - 1, current[1], distance_calculator(temp, goal)])  # top
                if child1[0] not in visited and child1[0] not in fringe:
                    fringe = sorting(fringe, child1)
            if current[1] != n - 1 and maze_array[current[0]][current[1] + 1] != 1 and current not in visited and current not in fringe:
                temp = [current[0], current[1] + 1]
                child2.append([current[0], current[1] + 1, distance_calculator(temp, goal)])  # right
                if child2[0] not in visited and child2[0] not in fringe:
                    fringe = sorting(fringe, child2)
            if current[0] != n - 1 and maze_array[current[0] + 1][current[1]] != 1 and current not in visited and current not in fringe:
                temp = [current[0] + 1, current[1]]
                child3.append([current[0] + 1, current[1], distance_calculator(temp, goal)])  # bottom
                if child3[0] not in visited and child3[0] not in fringe:
                    fringe = sorting(fringe, child3)
            if current[1] != 0 and maze_array[current[0]][current[1] - 1] != 1 and current not in visited and current not in fringe:
                temp = [current[0], current[1] - 1]
                child4.append([current[0], current[1] - 1, distance_calculator(temp, goal)])  # left
                if child4[0] not in visited and child4[0] not in fringe:
                    fringe = sorting(fringe, child4)
        visited.append(current)
        if current[1] == tracker[len(tracker) - 1][1] + 1 and current[0] == tracker[len(tracker) - 1][0]:  # top
            tracker.append(current)
        elif current[1] == tracker[len(tracker) - 1][1] and current[0] == tracker[len(tracker) - 1][0] + 1:  # right
            tracker.append(current)
        elif current[1] == tracker[len(tracker) - 1][1] - 1 and current[0] == tracker[len(tracker) - 1][0]:  # bottom
            tracker.append(current)
        elif current[1] == tracker[len(tracker) - 1][1] and current[0] == tracker[len(tracker) - 1][0] - 1:  # left
            tracker.append(current)
        else:  # check if there was a dead end and update the tracker array to accommodate for that
            temp_array = []
            if len(tracker) == 1:  # edge case
                pass
            else:
                for i in range(0, len(tracker)):
                    if current[1] == tracker[i][1] + 1 and current[0] == tracker[i][0]:  # top
                        temp_array.append(current)
                        break
                    elif current[1] == tracker[i][1] and current[0] == tracker[i][0] + 1:  # right
                        temp_array.append(current)
                        break
                    elif current[1] == tracker[i][1] - 1 and current[0] == tracker[i][0]:  # bottom
                        temp_array.append(current)
                        break
                    elif current[1] == tracker[i][1] and current[0] == tracker[i][0] - 1:  # left
                        temp_array.append(current)
                        break
                    else:
                        temp_array.append(tracker[i])

                tracker.clear()
                for i in range(0, len(temp_array)):  # updating tracker array
                    tracker.append(temp_array[i])
        if current == goal:
            print(tracker)
            return True

    print("2d array sucks")
    return False


def distance_calculator(start, end):
    x_diff = start[0] - end[0]
    y_diff = start[1] - end[1]
    return math.sqrt((x_diff**2) + (y_diff**2))


def sorting(fringe, child):
    return_array = []
    child_dist = child[0][2]

    if len(fringe) == 0:
        fringe.append(child[0])
        return fringe

    for i in range(0, len(fringe)):
        if child_dist <= fringe[i][2] and child[0] not in return_array:
            return_array.append(child[0])
            return_array.append(fringe[i])
            i += 2
        elif i == len(fringe) - 1 and child[0] not in return_array:
            return_array.append(fringe[i])
            return_array.append(child[0])
        else:
            return_array.append(fringe[i])

    return return_array


a_star(build_maze(dim, prob), dim)
