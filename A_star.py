import numpy, math


def a_star(maze_array):

    fringe = []
    visited = []
    child1 = []
    child2 = []
    child3 = []
    child4 = []
    n = 5
    start = [0, 0, math.sqrt(50)]
    goal = [n, n, 0]
    tracker = [start]
    fringe.append(start)
    while len(fringe) > 0:
        current = fringe.pop()
        if len(child1) != 0:
            child1.pop()
        if len(child2) != 0:
            child2.pop()
        if len(child3) != 0:
            child3.pop()
        if len(child4) != 0:
            child4.pop()
        if current[1] != 0 and maze_array[current[0]][current[1]] != 1 and current not in visited and current not in fringe:
            temp = [current[0], current[1] - 1]
            child1.append([current[0] - 1, current[1], distance_calculator(temp, goal)])  # top
            fringe = sorting(fringe, child1)
        if current[0] != n - 1 and maze_array[current[0]][current[1]] != 1 and current not in visited and current not in fringe:
            temp = [current[0] + 1, current[1]]
            child2.append([current[0] + 1, current[1], distance_calculator(temp, goal)])  # right
            fringe = sorting(fringe, child2)
        if current[1] != n - 1 and maze_array[current[0]][current[1]] != 1 and current not in visited and current not in fringe:
            temp = [current[0], current[1] - 1]
            child3.append([current[0], current[1] - 1, distance_calculator(temp, goal)])  # bottom
            fringe = sorting(fringe, child3)
        if current[0] != 0 and maze_array[current[0]][current[1]] != 1 and current not in visited and current not in fringe:
            temp = [current[0] - 1, current[1]]
            child4.append([current[0] - 1, current[1], distance_calculator(temp, goal)])  # left
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
            tracker.append(temp_array)
        if current == goal:
            return True

    return False


def distance_calculator(start, end):
    x_diff = start[0] - end[0]
    y_diff = start[1] - end[1]
    return int(math.sqrt((x_diff**2) + (y_diff**2)))


def sorting(fringe, child):
    return_array = []
    child_dist = child[2]

    if len(fringe) == 0:
        return fringe.append(child)

    for i in range(0, len(fringe)):
        if child_dist < fringe[i][2]:
            return_array[i] = child
            return_array[i+1] = fringe[i]
            i += 1
        elif i == len(fringe) - 1:
            fringe.append(child)
        else:
            return_array[i] = fringe[i]

    return return_array

