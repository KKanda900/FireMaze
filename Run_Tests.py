import sys, random, numpy, math, time, threading
from collections import deque
import pandas as pd
import matplotlib.pyplot as plt

'''
The purpose of Run_Tests.py is to conduct tests on the various algorithms we implemented in 
specific scenarios.

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
        return math.sqrt(x_diff**2 + y_diff**2)

    def sorting(self, fringe, child, cost):
        l = len(cost) - 1
        return_array = []
        child_dist = self.distance_calculator(child[0], [l, l])

        if len(fringe) == 0:
            fringe.append(child[0])
            return fringe

        for i in range(0, len(fringe)):
            curr_child_dist = self.distance_calculator(fringe[i], [l, l])
            if child_dist + cost[child[0][0]][child[0][1]] <= curr_child_dist + cost[fringe[i][0]][fringe[i][1]] and \
                    child[0] not in return_array:
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
        start = [0, 0]
        cost = numpy.zeros([n, n])
        goal = [n - 1, n - 1]
        tracker = []
        fringe.append(start)
        parent = numpy.zeros([n, n])  # 1 top, 2 right, 3 bottom, 4 left
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
            if current not in visited:
                if not fringe:
                    if current[0] != 0 and maze_array[current[0] - 1][current[1]] != 1:
                        child1.append([current[0] - 1, current[1]])  # top
                        if child1[0] not in visited and cost[current[0] - 1][[current[1]]] >= cost[current[0]][
                            [current[1]]] + 1 or cost[current[0] - 1][[current[1]]] == 0:
                            cost[current[0] - 1][[current[1]]] = cost[current[0]][[current[1]]] + 1
                            fringe = self.sorting(fringe, child1, cost)
                            parent[current[0] - 1][[current[1]]] = 3
                    if current[1] != n - 1 and maze_array[current[0]][current[1] + 1] != 1:
                        child2.append([current[0], current[1] + 1])  # right
                        if child2[0] not in visited and cost[current[0]][[current[1] + 1]] >= cost[current[0]][
                            [current[1]]] + 1 or cost[current[0]][[current[1] + 1]] == 0:
                            cost[current[0]][[current[1] + 1]] = cost[current[0]][[current[1]]] + 1
                            fringe = self.sorting(fringe, child2, cost)
                            parent[current[0]][[current[1] + 1]] = 2
                    if current[0] != n - 1 and maze_array[current[0] + 1][current[1]] != 1:
                        child3.append([current[0] + 1, current[1]])  # bottom
                        if child3[0] not in visited and cost[current[0] + 1][[current[1]]] >= cost[current[0]][
                            [current[1]]] + 1 or cost[current[0] + 1][[current[1]]] == 0:
                            cost[current[0] + 1][[current[1]]] = cost[current[0]][[current[1]]] + 1
                            fringe = self.sorting(fringe, child3, cost)
                            parent[current[0] + 1][[current[1]]] = 1
                    if current[1] != 0 and maze_array[current[0]][current[1] - 1] != 1:
                        child4.append([current[0], current[1] - 1])  # left
                        if child4[0] not in visited and cost[current[0]][[current[1] - 1]] >= cost[current[0]][
                            [current[1]]] + 1 or cost[current[0]][[current[1] - 1]] == 0:
                            cost[current[0]][[current[1] - 1]] = cost[current[0]][[current[1]]] + 1
                            fringe = self.sorting(fringe, child4, cost)
                            parent[current[0]][[current[1] - 1]] = 4
                else:
                    if current not in fringe:
                        if current[0] != 0 and maze_array[current[0] - 1][current[1]] != 1:
                            child1.append([current[0] - 1, current[1]])  # top
                            if child1[0] not in visited and child1[0] not in fringe and cost[current[0] - 1][
                                [current[1]]] >= cost[current[0]][[current[1]]] + 1 or cost[current[0] - 1][
                                [current[1]]] == 0:
                                cost[current[0] - 1][[current[1]]] = cost[current[0]][[current[1]]] + 1
                                fringe = self.sorting(fringe, child1, cost)
                                parent[current[0] - 1][[current[1]]] = 3
                        if current[1] != n - 1 and maze_array[current[0]][current[1] + 1] != 1:
                            child2.append([current[0], current[1] + 1])  # right
                            if child2[0] not in visited and child2[0] not in fringe and cost[current[0]][
                                [current[1] + 1]] >= cost[current[0]][[current[1]]] + 1 or cost[current[0]][
                                [current[1] + 1]] == 0:
                                cost[current[0]][[current[1] + 1]] = cost[current[0]][[current[1]]] + 1
                                fringe = self.sorting(fringe, child2, cost)
                                parent[current[0]][[current[1] + 1]] = 2
                        if current[0] != n - 1 and maze_array[current[0] + 1][current[1]] != 1:
                            child3.append([current[0] + 1, current[1]])  # bottom
                            if child3[0] not in visited and child3[0] not in fringe and cost[current[0] + 1][
                                [current[1]]] >= cost[current[0]][[current[1]]] + 1 or cost[current[0] + 1][
                                [current[1]]] == 0:
                                cost[current[0] + 1][[current[1]]] = cost[current[0]][[current[1]]] + 1
                                fringe = self.sorting(fringe, child3, cost)
                                parent[current[0] + 1][[current[1]]] = 1
                        if current[1] != 0 and maze_array[current[0]][current[1] - 1] != 1:
                            child4.append([current[0], current[1] - 1])  # left
                            if child4[0] not in visited and child4[0] not in fringe and cost[current[0]][
                                [current[1] - 1]] >= cost[current[0]][[current[1]]] + 1 or cost[current[0]][
                                [current[1] - 1]] == 0:
                                cost[current[0]][[current[1] - 1]] = cost[current[0]][[current[1]]] + 1
                                fringe = self.sorting(fringe, child4, cost)
                                parent[current[0]][[current[1] - 1]] = 4
                    visited.append(current)

            # else:  # check if there was a dead end and update the tracker array to accommodate for that
            # if len(tracker) == 1:  # edge case
            #    pass
            # else:

            if current == goal:
                y = n - 1
                x = n - 1
                tracker.append([y, x])
                self.a_star_nodes = len(visited)
                while True:
                    if parent[y][x] == 1:
                        tracker.append([y - 1, x])
                        y -= 1
                    elif parent[y][x] == 2:
                        tracker.append([y, x - 1])
                        x -= 1
                    elif parent[y][x] == 3:
                        tracker.append([y + 1, x])
                        y += 1
                    elif parent[y][x] == 4:
                        tracker.append([y, x + 1])
                        x += 1
                    if x == 0 and y == 0:
                        break

                tracker.reverse()

                print(tracker)
                print(cost)
                return True

        print("2d array sucks")

        print(cost)
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
    tests = [(500, 0.1), (500, 0.2), (500, 0.3), (500, 0.4), (500, 0.5)]

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
    """ Run_Tests = Maze()
    tests = [(100, 0.1), (100, 0.2), (100, 0.3), (100, 0.4), (100, 0.5)]

    while len(tests) != 0:
        q = 0
        print("ITERATION")
        curr_test = tests.pop(0)
        maze = Run_Tests.build_maze(curr_test[0], curr_test[1])
        dimensions = curr_test[0]
        probability = curr_test[1]
        start_x = int(random.uniform(0, dimensions-1))
        start_y = int(random.uniform(0, dimensions-1))
        end_x = int(random.uniform(0, dimensions-1))
        end_y = int(random.uniform(0, dimensions-1))
        name = Run_Tests.dfs((start_x, start_y), (end_x, end_y))
        f = open("Density_vs_Success.txt", "a")
        if(name == True):
            q = 1
        elif (name == False):
            q = 0
        print(q)
        f.write(str(curr_test[1]) + " " + str(q) + '\n')

    plot = pd.read_csv('Density_vs_Success.txt', sep='\s+', header=None)
    plot = pd.DataFrame(plot)
    x = plot[0]
    y1 = plot[1]
    #print("Values",x,y1)
    plt.plot(x, y1, label='Density and Percentage Of Success')
    plt.xlabel('Density')
    plt.ylabel('Percentage')
    plt.title('Obstacle Desnity vs Probability Of Success')
    plt.legend()
    plt.savefig('plot.png')
    plt.show()
    exit(0) """

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
    print(run_tests())
