import numpy


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
    # first define the starting indicies
    i = 0
    j = 0

    # now define the start and end node which in our case is the first indicies and the last indicies respectively
    start = (0, 0)
    goal = (len(arr) - 1, len(arr) - 1)
    print("The defined goal node is {}".format(goal))

    # now because we are working with bfs, we know bfs calls for a fringe in the form of a queue because of the queue's policy (FIFO)
    fringe = []
    fringe.append(start)

    # keep an array to represent the visited arrays
    visited = numpy.zeros((len(arr), len(arr)), dtype=bool)

    # now iterate through the fringe to check for the path

    """
    Thoughts: 
        1. Iterate through the nested array then inside the jth iteration conduct bfs like implemented on the bottom
    """

    while len(fringe) > 0:
        current = fringe.pop(0)
        print("Current is {}".format(current))
        visited[current[0]][current[1]] = True
        if current == goal:
            return True
        else:
            # first check the up direction
            if check_valid_bounds(-1, 0, current, arr) == True:
                if (
                    arr[current[0] - 1][current[1]] == 0
                    and visited[current[0] - 1][current[1]] == True
                ):
                    fringe.append((current[0] - 1, current[1]))

            # now check the down direction
            if check_valid_bounds(1, 0, current, arr) == True:
                if (
                    arr[current[0] + 1][current[1]] == 0
                    and visited[current[0] + 1][current[1]] == False
                ):
                    fringe.append((current[0] + 1, current[1]))

            # now we can check the left direction
            if check_valid_bounds(0, -1, current, arr) == True:
                if (
                    arr[current[0]][current[1] - 1] == 0
                    and visited[current[0]][current[1] - 1] == False
                ):
                    fringe.append((current[0], current[1] - 1))

            # finally check the right side
            if check_valid_bounds(0, 1, current, arr) == True:
                if (
                    arr[current[0]][current[1] + 1] == 0
                    and visited[current[0]][current[1] + 1] == False
                ):
                    fringe.append((current[0], current[1] + 1))

    print(visited)
    return False


if __name__ == "__main__":
    arr = [[0, 1, 0], [0, 0, 0], [0, 1, 0]]
    print(arr[0])
    print(arr[1])
    print(arr[2])
    print(bfs_tree_search(arr))