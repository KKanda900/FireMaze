import numpy, random
from collections import deque, OrderedDict


def print_2darray(arr):
    for i in range(0, len(arr)):
        for j in range(0, len(arr[i])):
            print(arr[i][j], end=" ")

        print("\n")

def build_maze(size, probability):
    obstacle_num = 0  # See if the amount of obstacles required are 0 or not
    obstacles = int((size * size) * probability)  # if the maze area is 100 then there should be only 10 obstacles
    tracking_array = numpy.zeros((size, size))  # track where the obstacles are places so it doesn't double count
    dim_array = list(range(0, size))
    while obstacles != 0:
        i = random.choice(dim_array)
        j = random.choice(dim_array)
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
                if not bfs_route:
                    bfs_route.append(new_curr)
                elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] + 1 and new_curr[0] == bfs_route[len(bfs_route) - 1][0]:  # top
                    bfs_route.append(new_curr)
                elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] and new_curr[0] == bfs_route[len(bfs_route) - 1][0] + 1:  # right
                    bfs_route.append(new_curr)
                elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] - 1 and new_curr[0] == bfs_route[len(bfs_route) - 1][0]:  # bottom
                    bfs_route.append(new_curr)
                elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] and new_curr[0] == bfs_route[len(bfs_route) - 1][0] - 1:  # left
                    bfs_route.append(new_curr)

            bfs_route.append(start)
            bfs_route.reverse()
            return list(bfs_route)
        else:
            # first check the up direction
            if check_valid_bounds(-1, 0, current, arr) and arr[current[0] - 1][current[1]] == 0 and visited[current[0] - 1][current[1]] == False and (current[0] - 1, current[1]) not in fringe:
                fringe.append((current[0] - 1, current[1]))
                if current not in path:
                    path.append(current)

            # now check the down direction
            if check_valid_bounds(1, 0, current, arr) and arr[current[0] + 1][current[1]] == 0 and visited[current[0] + 1][current[1]] == False and (current[0] + 1, current[1]) not in fringe:
                fringe.append((current[0] + 1, current[1]))
                if current not in path:
                    path.append(current)

            # now we can check the left direction
            if check_valid_bounds(0, -1, current, arr) and arr[current[0]][current[1] - 1] == 0 and visited[current[0]][current[1] - 1] == False and (current[0], current[1] - 1) not in fringe:
                fringe.append((current[0], current[1] - 1))
                if current not in path:
                    path.append(current)

            # finally check the right side
            if check_valid_bounds(0, 1, current, arr) and arr[current[0]][current[1] + 1] == 0 and visited[current[0]][current[1] + 1] == False and (current[0], current[1] + 1) not in fringe:
                fringe.append((current[0], current[1] + 1))
                if current not in path:
                    path.append(current)
    return []


if __name__ == "__main__":
    arr = build_maze(7, .4)
    print(bfs_tree_search(arr))
