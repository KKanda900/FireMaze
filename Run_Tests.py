import sys, random, numpy, math, time, threading
from collections import deque
import pandas as pd
import matplotlib.pyplot as plt

'''
The purpose of Run_Tests.py is to conduct tests on the various algorithms we implemented in 
specific scenerios.

Same code wise just without the drawing portions, so we can run the tests better
'''

class Maze:
    x, y = 0, 0
    cell_size = 3
    dim = 10
    tracking_obstacles = []
    display = None
    bfs_nodes = 0
    a_star_nodes = 0

    def build_maze(self, size, probability):
        self.x = 0 
        self.y = 0
        self.dim = size
        obstacle_num = 0  # See if the amount of obstacles required are 0 or not
        obstacles = (size*size)*probability  # if the maze area is 100 then there should be only 10 obstacles
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

        return tracking_array

    def distance_calculator(self, start, end):
        x_diff = abs(start[0] - end[0])
        y_diff = abs(start[1] - end[1])
        return x_diff + y_diff

    def sorting(self, fringe, child, cost):
        return_array = []
        child_dist = child[0][2]

        if len(fringe) == 0:
            fringe.append(child[0])
            return fringe

        for i in range(0, len(fringe)):
            if child_dist + cost[fringe[i][0]][fringe[i][1]] < fringe[i][2] + cost[fringe[i][0]][fringe[i][1]] and child[0] not in return_array:
                return_array.append(child[0])
                return_array.append(fringe[i])
                i += 2
            elif i == len(fringe) - 1 and child[0] not in return_array:
                return_array.append(fringe[i])
                return_array.append(child[0])
            else:
                return_array.append(fringe[i])

        return return_array

    def a_star(self, arr):
        maze_array = arr
        fringe = []
        visited = [[-1, -1, -1]]
        child1 = []
        child2 = []
        child3 = []
        child4 = []
        n = len(maze_array)
        start = [0, 0, 2*n]
        cost = numpy.zeros([n,n])
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
                    child1.append([current[0] - 1, current[1], self.distance_calculator(temp, goal)])  # top
                    cost[current[0] - 1][[current[1]]] = cost[current[0]][[current[1]]] + 1
                    fringe = self.sorting(fringe, child1, cost)
                if current[1] != n - 1 and maze_array[current[0]][current[1] + 1] != 1 and current not in visited:
                    temp = [current[0], current[1] + 1]
                    child2.append([current[0], current[1] + 1, self.distance_calculator(temp, goal)])  # right
                    cost[current[0]][[current[1] + 1]] = cost[current[0]][[current[1]]] + 1
                    fringe = self.sorting(fringe, child2, cost)
                if current[0] != n - 1 and maze_array[current[0] + 1][current[1]] != 1 and current not in visited:
                    temp = [current[0] + 1, current[1]]
                    child3.append([current[0] + 1, current[1], self.distance_calculator(temp, goal)])  # bottom
                    cost[current[0] + 1][[current[1]]] = cost[current[0]][[current[1]]] + 1
                    fringe = self.sorting(fringe, child3, cost)
                if current[1] != 0 and maze_array[current[0]][current[1] - 1] != 1 and current not in visited:
                    temp = [current[0], current[1] - 1]
                    child4.append([current[0], current[1] - 1, self.distance_calculator(temp, goal)])  # left
                    cost[current[0]][[current[1] - 1]] = cost[current[0]][[current[1]]] + 1
                    fringe = self.sorting(fringe, child4, cost)
            else:
                if current[0] != 0 and maze_array[current[0] - 1][current[1]] != 1 and current not in visited and current not in fringe:
                    temp = [current[0] - 1, current[1]]
                    child1.append([current[0] - 1, current[1], self.distance_calculator(temp, goal)])  # top
                    if child1[0] not in visited and child1[0] not in fringe:
                        cost[current[0] - 1][[current[1]]] = cost[current[0]][[current[1]]] + 1
                        fringe = self.sorting(fringe, child1, cost)
                if current[1] != n - 1 and maze_array[current[0]][current[1] + 1] != 1 and current not in visited and current not in fringe:
                    temp = [current[0], current[1] + 1]
                    child2.append([current[0], current[1] + 1, self.distance_calculator(temp, goal)])  # right
                    if child2[0] not in visited and child2[0] not in fringe:
                        cost[current[0]][[current[1] + 1]] = cost[current[0]][[current[1]]] + 1
                        fringe = self.sorting(fringe, child2, cost)
                if current[0] != n - 1 and maze_array[current[0] + 1][current[1]] != 1 and current not in visited and current not in fringe:
                    temp = [current[0] + 1, current[1]]
                    child3.append([current[0] + 1, current[1], self.distance_calculator(temp, goal)])  # bottom
                    if child3[0] not in visited and child3[0] not in fringe:
                        cost[current[0] + 1][[current[1]]] = cost[current[0]][[current[1]]] + 1
                        fringe = self.sorting(fringe, child3, cost)
                if current[1] != 0 and maze_array[current[0]][current[1] - 1] != 1 and current not in visited and current not in fringe:
                    temp = [current[0], current[1] - 1]
                    child4.append([current[0], current[1] - 1, self.distance_calculator(temp, goal)])  # left
                    if child4[0] not in visited and child4[0] not in fringe:
                        cost[current[0]][[current[1] - 1]] = cost[current[0]][[current[1]]] + 1
                        fringe = self.sorting(fringe, child4, cost)
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
                tracker.reverse()
                self.a_star_nodes = len(tracker)
                a_star_route = []
                while tracker[0] != start:
                    new_curr = tracker.pop(0)
                    if not a_star_route:
                        a_star_route.append(new_curr)
                    # top
                    elif new_curr[1] == a_star_route[len(a_star_route) - 1][1] + 1 and new_curr[0] == a_star_route[len(a_star_route) - 1][0]:
                        a_star_route.append(new_curr)
                    # right
                    elif new_curr[1] == a_star_route[len(a_star_route) - 1][1] and new_curr[0] == a_star_route[len(a_star_route) - 1][0] + 1:
                        a_star_route.append(new_curr)
                    # bottom
                    elif new_curr[1] == a_star_route[len(a_star_route) - 1][1] - 1 and new_curr[0] == a_star_route[len(a_star_route) - 1][0]:
                        a_star_route.append(new_curr)
                    # left
                    elif new_curr[1] == a_star_route[len(a_star_route) - 1][1] and new_curr[0] == a_star_route[len(a_star_route) - 1][0] - 1:
                        a_star_route.append(new_curr)

                a_star_route.append(start)
                a_star_route.reverse()
                return True

        return False

    def check_valid_bounds(self, i, j, pop_value, arr):
        i = pop_value[0] + i
        j = pop_value[1] + j
        if i >= 0 and i < len(arr) and j >= 0 and j < len(arr):
            return True
        else:
            return False
    
    def bfs_tree_search(self, arr):
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
                self.bfs_nodes = len(path)
                path.reverse()
                # now that we found the end node, let's perform a recursive backtracking algorithm to find the actual path
                bfs_route = []
                while path[0] != start:
                    new_curr = path.pop(0)
                    if not bfs_route:
                        bfs_route.append(new_curr)
                    # top
                    elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] + 1 and new_curr[0] == bfs_route[len(bfs_route) - 1][0]:
                        bfs_route.append(new_curr)
                    # right
                    elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] and new_curr[0] == bfs_route[len(bfs_route) - 1][0] + 1:
                        bfs_route.append(new_curr)
                    # bottom
                    elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] - 1 and new_curr[0] == bfs_route[len(bfs_route) - 1][0]:
                        bfs_route.append(new_curr)
                    # left
                    elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] and new_curr[0] == bfs_route[len(bfs_route) - 1][0] - 1:
                        bfs_route.append(new_curr)

                bfs_route.append(start)
                bfs_route.reverse()
                return bfs_route

            else:
                # first check the up direction
                if self.check_valid_bounds(-1, 0, current, arr) and arr[current[0] - 1][current[1]] == 0 and visited[current[0] - 1][current[1]] == False and (current[0] - 1, current[1]) not in fringe:
                    fringe.append((current[0] - 1, current[1]))
                    if current not in path:
                        path.append(current)

                # now check the down direction
                if self.check_valid_bounds(1, 0, current, arr) and arr[current[0] + 1][current[1]] == 0 and visited[current[0] + 1][current[1]] == False and (current[0] + 1, current[1]) not in fringe:
                    fringe.append((current[0] + 1, current[1]))
                    if current not in path:
                        path.append(current)

                # now we can check the left direction
                if self.check_valid_bounds(0, -1, current, arr) and arr[current[0]][current[1] - 1] == 0 and visited[current[0]][current[1] - 1] == False and (current[0], current[1] - 1) not in fringe:
                    fringe.append((current[0], current[1] - 1))
                    if current not in path:
                        path.append(current)

                # finally check the right side
                if self.check_valid_bounds(0, 1, current, arr) and arr[current[0]][current[1] + 1] == 0 and visited[current[0]][current[1] + 1] == False and (current[0], current[1] + 1) not in fringe:
                    fringe.append((current[0], current[1] + 1))
                    if current not in path:
                        path.append(current)
        return []

def run_tests():
    Run_Tests = Maze()
    tests = [(200, 0.9), (200, 0.9)]

    while len(tests) != 0:
        print("ITERATION")
        curr_test = tests.pop(0)
        maze = Run_Tests.build_maze(curr_test[0], curr_test[1])
        Run_Tests.bfs_tree_search(maze)
        Run_Tests.a_star(maze)
        f = open("Nodes_Per_Density.txt", "a")
        f.write(str(curr_test[1]) + " " + str(Run_Tests.bfs_nodes) + " " + str(Run_Tests.a_star_nodes) + '\n')
    
    plot = pd.read_csv('Nodes_Per_Density.txt', sep='\s+', header=None)
    plot = pd.DataFrame(plot)
    x = plot[0]
    y1 = plot[1]
    y2 = plot[2]
    plt.plot(x, y1, label='Avg. BFS Nodes per Density')
    plt.plot(x, y2, label='Avg. A Star Nodes per Density')
    plt.xlabel('Density')
    plt.ylabel('Avg. Nodes')
    plt.title('Number of Nodes explored in BFS and A Star vs Obstacle Density')
    plt.legend()
    plt.savefig('plot.png')
    plt.show()
    exit(0)

def largest_bfs():
    Run_Tests = Maze()

    Running = True
    start_time = 0
    end_time = 0
    while Running:
        start_time = time.time()
        maze = Run_Tests.build_maze(100, 0.3)
        bfs = Run_Tests.bfs_tree_search(maze)
        if bfs != [] or bfs == []:
            end_time = time.time()
            Running = False
            break
    
    elapsed_time = end_time-start_time

    if elapsed_time <= 60.0:
        return elapsed_time
    
    return elapsed_time

if __name__ == "__main__":
    print(largest_bfs())
