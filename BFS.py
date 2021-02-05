import numpy, math
from collections import deque, OrderedDict


def print_2darray(arr):
    for i in range(0, len(arr)):
        for j in range(0, len(arr[i])):
            print(arr[i][j], end=" ")

        print("\n")


def check_valid_bounds(i, j, pop_value, arr):
    i = pop_value[0] + i
    j = pop_value[1] + j
    if i >= 0 and i < len(arr) and j >= 0 and j < len(arr):
        return True
    else:
        return False


def bfs_tree_search(arr):
    # now define the start and end node which in our case is the first indicies and the last indicies respectively
    start = (0, 0)
    goal = (len(arr) - 1, len(arr) - 1)

    # now because we are working with bfs, we know bfs calls for a fringe in the form of a queue because of the queue's policy (FIFO)
    fringe = deque()
    fringe.append(start)

    # keep an array to represent the visited arrays
    visited = numpy.zeros((len(arr), len(arr)), dtype=bool)

    # for this implementation of bfs we want to keep track of the parents to obtain the shortest path
    path = []

    # now iterate through the fringe to check for the path
    while len(fringe) > 0:
        current = fringe.popleft()
        visited[current[0]][current[1]] = True
        if current == goal:
            path.append(current)
            path.reverse()
            # now that we found the end node, let's perform a recursive backtracking algorithm to find the actual path
            bfs_route = []
            while path[0] != start:
                new_curr = path.pop(0)
                bfs_route.append(new_curr)
            bfs_route.append(start)
            bfs_route.reverse()
            return list(OrderedDict.fromkeys(bfs_route))
        else:
            # first check the up direction
            if check_valid_bounds(-1, 0, current, arr) == True and arr[current[0] - 1][current[1]] == 0 and visited[current[0] - 1][current[1]] == False:
                fringe.append((current[0] - 1, current[1]))
                path.append(current)

            # now check the down direction
            if check_valid_bounds(1, 0, current, arr) == True and arr[current[0] + 1][current[1]] == 0 and visited[current[0] + 1][current[1]] == False:
                fringe.append((current[0] + 1, current[1]))
                path.append(current)

            # now we can check the left direction
            if check_valid_bounds(0, -1, current, arr) == True and arr[current[0]][current[1] - 1] == 0 and visited[current[0]][current[1] - 1] == False:
                fringe.append((current[0], current[1] - 1))
                path.append(current)

            # finally check the right side
            if check_valid_bounds(0, 1, current, arr) == True and arr[current[0]][current[1] + 1] == 0 and visited[current[0]][current[1] + 1] == False:
                fringe.append((current[0], current[1] + 1))
                path.append(current)
    return []


if __name__ == "__main__":
    arr = [[0, 1, 0], [0, 1 ,0], [0, 0, 0]]
    print(arr[0])
    print(arr[1])
    print(arr[2])
    print(bfs_tree_search(arr))
