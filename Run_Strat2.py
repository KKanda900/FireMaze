import sys
import re
import random
import numpy
import math
from collections import deque, OrderedDict
import threading
import time
import pandas as pd
import matplotlib.pyplot as plt

current1 = 0
dimensions = 0

class Maze:
    x, y = 0, 0
    cell_size = 20
    dim = 10
    tracking_obstacles = []
    x, y = 0, 0
    cell_size = 20
    dim = 10
    tracking_obstacles = []
    fire_array = None
    fire_maze = None
    fire_index = 0
    fringe = []
    tracking_array = []
    visited = []
    path_to_fire = False

    def build_maze(self, size, probability):
        self.dim = size
        self.fire_array = numpy.zeros((self.dim, self.dim))
        obstacle_num = 0  # See if the amount of obstacles required are 0 or not
        # if the maze area is 100 then there should be only 10 obstacles
        obstacles = (size*size)*probability
        # track where the obstacles are places so it doesn't double count
        tracking_array = numpy.zeros((size, size))
        dim_array = list(range(0, size))
        # iterate based on the amount of obstacles that are left, when there are no obstacles left then draw the maze
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

        self.tracking_obstacles = tracking_array
        self.tracking_array = tracking_array
        return self.tracking_obstacles

    def dfs(self, beginning, goal):

        #checks whether either the goal or beginning points are blocked, if so return false
        if self.tracking_array[int(beginning[0])][int(beginning[1])] == 1 or self.tracking_array[goal[0]][goal[1]] == 1:
            return False

        #If they are the same point then return true
        if beginning == goal:
            self.fringe.clear
            self.visited.clear
            return True

        #If not false, then add the beginning point to the fringe
        self.fringe.append((int(beginning[0]), int(beginning[1])))

        #loops through the fringe
        while len(self.fringe) > 0:

            #sets current to the topmost element of the fringe
            current = self.fringe.pop()

            #Terminating case in which current is equal to the goal
            if current == (goal[0], goal[1]):
                return True

            #Current not equal to goal
            else:
                #current has not been explored yet (haven't added surrounding valid children to the fringe)
                if current not in self.visited:
                    #All columns other than the first column
                    if current[1] > 0:

                        #Checks validity of left child
                        if self.tracking_array[current[0]][current[1]-1] == 0 and (current[0], current[1]-1) not in self.fringe and (current[0], current[1]-1) not in self.visited:
                            # left child is valid
                            self.fringe.append((current[0], current[1]-1))

                        #Checks whether the row is not the last row and also validity of bottom child
                        if current[0] != self.dim-1 and self.tracking_array[current[0]+1][current[1]] == 0 and (current[0]+1, current[1]) not in self.fringe and (current[0]+1, current[1]) not in self.visited:
                            # bottom child is valid
                            self.fringe.append((current[0]+1, current[1]))

                        #Checks whether the column is not the last column and validity of right child
                        if current[1] != self.dim-1 and self.tracking_array[current[0]][current[1]+1] == 0 and (current[0], current[1]+1) not in self.fringe and (current[0], current[1]+1) not in self.visited:
                            # right child is valid
                            self.fringe.append((current[0], current[1]+1))

                        #Checks whether the row is not the first row and validity of top child
                        if current[0] != 0 and self.tracking_array[current[0]-1][current[1]] == 0 and (current[0]-1, current[1]) not in self.fringe and (current[0]-1, current[1]) not in self.visited:
                            # top child is valid
                            self.fringe.append((current[0]-1, current[1]))

                    #The first column
                    else:
                        #Checks whether the row is not the last row and also validity of bottom child
                        if current[0] != self.dim-1 and self.tracking_array[current[0]+1][current[1]] == 0 and (current[0]+1, current[1]) not in self.fringe and (current[0]+1, current[1]) not in self.visited:
                            # bottom child is valid
                            self.fringe.append((current[0]+1, current[1]))

                        #Checks validity of right child
                        if self.tracking_array[current[0]][current[1]+1] == 0 and (current[0], current[1]+1) not in self.fringe and (current[0], current[1]+1) not in self.visited:
                            # right child is valid
                            self.fringe.append((current[0], current[1]+1))

                        #Checks whether the row is not the first row and validity of top child
                        if current[0] != 0 and self.tracking_array[current[0]-1][current[1]] == 0 and (current[0]-1, current[1]) not in self.fringe and (current[0]-1, current[1]) not in self.visited:
                            # top child is valid
                            self.fringe.append((current[0]-1, current[1]))

                #Adds the current node to visited (all valid children have been added to the fringe)
                self.visited.append(current)
        self.fringe.clear()
        self.visited.clear()
        #In the case that the fringe is empty and you could not find a path
        return False


    def check_valid_bounds(self, i, j, pop_value, arr):
        i = pop_value[0] + i
        j = pop_value[1] + j
        if i >= 0 and i < len(arr) and j >= 0 and j < len(arr):
            return True
        else:
            return False

    def generate_fire_maze1(self, probability, bln):
        q = probability
        fire_maze = self.tracking_obstacles  # the actual maze
        fire_array = self.fire_array  # array that keeps track of fire only in the maze
        # a copy of the fire_array to keep track of old fires, so the new ones are not counted when calculating probabilities
        fire_array_copy = numpy.zeros((len(fire_maze), len(fire_maze)))
        for x in range(0, len(fire_maze)):
            for y in range(0, len(fire_maze)):
                fire_array_copy[x][y] = fire_array[x][y]
        if bln:  # if it's the first fire then we chose a stop randomly
            while bln:  # for the first one does a random fire
                # random x spot for fire
                y = random.randint(0, len(fire_maze) - 1)
                # random y spot for fire
                x = random.randint(0, len(fire_maze) - 1)
                if fire_maze[x][y] != 2 and fire_maze[x][y] != 1 and (x != 0 and y != 0) and (
                        x != len(fire_maze) - 1 and y != len(fire_maze) - 1):  # only generate fire if there is no obstacle there and it's not the start or goal
                    fire_array[x][y] = 2
                    self.tracking_obstacles[x][y] = 2
                    return self.tracking_obstacles  # return the maze array
        else:
            # if it's not the first time then we traverse through every cell
            for i in range(0, len(self.tracking_obstacles)):
                # for each cell we calculate the probability fo it catching fire depending on how many of it's neighbours are on fire
                for j in range(0, len(self.tracking_obstacles)):
                    fire = 0
                    if fire_maze[i][j] != 1 and fire_array[i][j] != 2:
                        # we use the copy of fire array to make sure a new fire is not counted in the calculations
                        if i != len(self.tracking_obstacles) - 1 and fire_array_copy[i + 1][j] == 2:
                            fire += 1  # bottom cell
                        if fire_array_copy[i - 1][j] == 2 and i != 0:
                            fire += 1  # top cell
                        if j != len(self.tracking_obstacles) - 1 and fire_array_copy[i][j + 1] == 2:
                            fire += 1  # right cell
                        if fire_array_copy[i][j - 1] == 2 and j != 0:
                            fire += 1  # left cell
                        # calculate the probability with given formula
                        prob = 1 - ((1 - q) ** fire)
                        if fire > 0 and random.random() <= prob and prob > 0:  # if it catches on fire
                            # update the fire tracking array
                            fire_array[i][j] = 2
                            # update the actual maze array
                            self.tracking_obstacles[i][j] = 2
        self.x = 0
        self.y = 0
        size = self.dim
        tracking_array = self.tracking_obstacles

    def bfs_tree_search1(self, start, goal):
        arr = self.tracking_obstacles
        # now define the start and end node which in our case is the first indicies and the last indicies respectively

        # now because we are working with bfs, we know bfs calls for a fringe in the form of a queue because of the queue's policy (FIFO)
        fringe = deque()
        fringe.append(start)

        # keep an array to represent the visited arrays
        visited = numpy.zeros((len(arr), len(arr)), dtype=bool)

        # for this implementation of bfs we want to keep track of the parents to obtain the shortest path
        path = []

        # now iterate through the fringe to check for the path
        while len(fringe) > 0:
            #print(fringe)
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
        return False

    def strategy2(self, flammability):
        path1 = []
        self.generate_fire_maze1(flammability, True)
        time.sleep(1)
        path = self.bfs_tree_search1(
            (0, 0), (self.dim-1, self.dim-1))
        if path == False:
            return False
        path1.append(path[0])
        x = len(path1)
        while(x != 0):
            self.generate_fire_maze1(flammability, False)
            time.sleep(1)
            path1 = self.bfs_tree_search1(
                path1[0], (self.dim-1, self.dim-1))
            if path1 == False:
                return False
            time.sleep(1)
            path1 = self.bfs_tree_search1(
                path1[1], (self.dim-1, self.dim-1))
            if path1 == False:
                return False

            if path1[0] == (self.dim-1, self.dim-1):
                return True

    def draw_path(self, position):  # arr contains the coordinates of the path to draw
        self.x = 0
        self.y = 0
        screen = self.display
        size = self.dim
        tracking_array = self.tracking_obstacles
        curr = None

        curr = position
        tracking_array[curr[0]][curr[1]] = 3


def parallel_tests(curr_test):
    numTests = 10
    success = 0
    while numTests != 0:
        print(numTests)
        Running_Tests = Maze()
        Running_Tests.build_maze(curr_test[0], curr_test[1])
        path = Running_Tests.dfs((0, 0), (99, 99))
        if path:
            result = Running_Tests.strategy2(curr_test[2])
            if result == True:
                success += 1
            numTests -= 1
    f = open("Strategy_2_Success_Rate.txt", "a")
    f.write(str(curr_test[2]) + " " + str(success/10) + "\n")


def running_tests1():
    tests = [(100, 0.3, 0.1), (100, 0.3, 0.2), (100, 0.3, 0.3),
             (100, 0.3, 0.4), (100, 0.3, 0.5), (100, 0.3, 0.6)]

    x = threading.Thread(target=parallel_tests, args=(tests[0],))
    x.start()
    y = threading.Thread(target=parallel_tests, args=(tests[1],))
    y.start()
    z = threading.Thread(target=parallel_tests, args=(tests[2],))
    z.start()
    a = threading.Thread(target=parallel_tests, args=(tests[3],))
    a.start()
    b = threading.Thread(target=parallel_tests, args=(tests[4],))
    b.start()
    c = threading.Thread(target=parallel_tests, args=(tests[5],))
    c.start()

    x.join()
    y.join()
    z.join()
    a.join()
    b.join()
    c.join()

    plot = pd.read_csv('Strategy_2_Success_Rate.txt', sep='\s+', header=None)
    plot = pd.DataFrame(plot)
    x = plot[0]
    y = plot[1]
    plt.plot(x, y, label='Success vs Flammability')
    plt.xlabel('Flammability')
    plt.ylabel('Average Success')
    plt.title('Average Success Rate vs Flammability at p = 0.3')
    plt.legend()
    plt.savefig('plot231.png')
    plt.show()
    


if __name__ == "__main__":
    running_tests1()
