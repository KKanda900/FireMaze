import numpy, math
from collections import deque, OrderedDict


def print_2darray(arr):
    for i in range(0, len(arr)):
        for j in range(0, len(arr[i])):
            print(arr[i][j], end=" ")

        print("\n")


def check_valid_bounds(i, j, pop_value, arr):
    a = pop_value[0] + i
    b = pop_value[1] + j
    if a >= 0 and a < len(arr) and b >= 0 and b < len(arr):
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

    # for this implementation of bfs we want to keep track of the parents to obtain the shortest parent
    parent = []

    # now iterate through the fringe to check for the parent
    while len(fringe) > 0:
        current = fringe.popleft()
        visited[current[0]][current[1]] = True
        arr[current[0]][current[1]] = 2
        if current == goal:
            parent.append(current)
            parent.reverse()
            # now that we found the end node, let's perform a recursive backtracking algorithm to find the actual parent
            bfs_route = [goal]
            while parent[0] != start:
                a = parent.pop(0)
                parent.append(a)
                print(bfs_route)
            bfs_route.append(start)
            bfs_route.reverse()
            return list(OrderedDict.fromkeys(bfs_route))
        else:
            # first check the up direction
            if check_valid_bounds(-1, 0, current, arr) == True and arr[current[0] - 1][current[1]] == 0 and visited[current[0] - 1][current[1]] == False:
                fringe.append((current[0] - 1, current[1]))
                parent.append(current)

            # now check the down direction
            if check_valid_bounds(1, 0, current, arr) == True and arr[current[0] + 1][current[1]] == 0 and visited[current[0] + 1][current[1]] == False:
                fringe.append((current[0] + 1, current[1]))
                parent.append(current)

            # now we can check the left direction
            if check_valid_bounds(0, -1, current, arr) == True and arr[current[0]][current[1] - 1] == 0 and visited[current[0]][current[1] - 1] == False:
                fringe.append((current[0], current[1] - 1))
                parent.append(current)

            # finally check the right side
            if check_valid_bounds(0, 1, current, arr) == True and arr[current[0]][current[1] + 1] == 0 and visited[current[0]][current[1] + 1] == False:
                fringe.append((current[0], current[1] + 1))
                parent.append(current)
                
    return []


if __name__ == "__main__":
    arr = [[0, 0, 0], [0, 1 ,0], [0, 1, 0]]
    print(arr[0])
    print(arr[1])
    print(arr[2])
    print(bfs_tree_search(arr))
