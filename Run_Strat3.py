import sys
import random
import numpy
import math
import threading
import time
import matplotlib.pyplot as plt
import pandas as pd
from collections import deque, OrderedDict

# Color Graphics used in the Maze Visualizer
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# these nodes will be placed in a 2D array to represent the Node's probability of catching on fire and the value (0 for clear cell, 1 for occupied with obstacle, 2 for occupied with fire)


class FireNode:
    fire_prob = 0.0
    value = 0

    def __init__(self, value, prob_fire):
        self.fire_prob = prob_fire
        self.value = value


class Maze:
    x, y = 0, 0
    cell_size = 20
    dim = 10
    tracking_obstacles = []
    display = None
    fire_array = None
    fire_maze = None
    fire_index = 0
    fringe = []
    tracking_array = []
    visited = []

    # this is where the logic to build the maze is based to create based on a certain obstacle density
    def build_maze(self, size, probability):
        self.dim = size
        self.fire_array = numpy.zeros((self.dim, self.dim))
        obstacle_num = 0  # See if the amount of obstacles required are 0 or not
        # if the maze area is 100 then there should be only 10 obstacles
        obstacles = (size*size)*probability
        # track where the obstacles are places so it doesn't double count
        tracking_array = numpy.zeros((size, size))
        dim_array = list(range(0, size))
        self.fire_maze = [[FireNode(0, 0.0) for x in range(self.dim)] for y in range(
            self.dim)]  # generate the fire maze intial upon start
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
    
    # this is where the primary logic goes to create the fire in the maze overall to create dynamic mazes
    def generate_fire_maze(self, probability):
        q = probability  # the likely hood of a cell catching on fire

        # tracking obstacles in our case will also track fire now
        fire_maze = self.tracking_obstacles
        fire_array = self.fire_array  # fire_array will represent a dynamically changing maze
        # copy the contents of fire maze into the copy in order to get accurate places to store the fire
        fire_array_copy = numpy.zeros((len(fire_maze), len(fire_maze)))

        # copy the contents of fire_array into fire_array_copy
        for x in range(0, len(fire_maze)):
            for y in range(0, len(fire_maze)):
                fire_array_copy[x][y] = fire_array[x][y]

        # the first fire being placed is placed randomly in the maze so we want to check if this is the first fire being generated
        if self.fire_index == 0:
            while self.fire_index == 0:  # for the first one does a random fire
                # get a random y index based on the size of the maze
                y = random.randint(0, len(fire_maze) - 1)
                # get a radnom x index based on the size of the maze
                x = random.randint(0, len(fire_maze) - 1)
                # if a spot is already not on fire and not the first or last cell make it on fire
                if fire_maze[x][y] != 2 and fire_maze[x][y] != 1 and (x != 0 and y != 0) and (x != len(fire_maze) - 1 and y != len(fire_maze) - 1):
                    pathResult = self.dfs((0,0), (x, y))
                    if pathResult == False:
                        return False
                    fire_array[x][y] = 2  # 2 indicates there is fire placed
                    # this is so we can take account for the maze globally
                    self.tracking_obstacles[x][y] = 2
                    self.fire_index += 1  # increase this so we dont choose another random spot
                    # Fire Node is 2 and 1 (100%) of catching on fire because its on fire already
                    self.fire_maze[x][y] = FireNode(2, 1.0)
                    return True
        else:
            # now that we choose one spot on the maze to catch on fire, the fire can move only one spot and the chance is based on the neighbors that are on fire
            for i in range(0, len(self.tracking_obstacles)):
                for j in range(0, len(self.tracking_obstacles)):
                    fire = 0  # to track the fire neighbors
                    if fire_maze[i][j] != 1 and fire_array[i][j] != 2:
                        # check the below neighbor
                        if i != len(self.tracking_obstacles) - 1 and fire_array_copy[i + 1][j] == 2:
                            fire += 1
                        # check the up neighbor
                        if fire_array_copy[i - 1][j] == 2 and i != 0:
                            fire += 1
                        # check the right neighbor
                        if j != len(self.tracking_obstacles) - 1 and fire_array_copy[i][j + 1] == 2:
                            fire += 1
                        # check the left neighbor
                        if fire_array_copy[i][j - 1] == 2 and j != 0:
                            fire += 1
                        # calculate the probability of a cell catching on fire
                        prob = 1 - ((1 - q) ** fire)
                        if fire > 0 and random.random() <= prob and prob > 0:
                            fire_array[i][j] = 2  # track it locally
                            # track it globally
                            self.tracking_obstacles[i][j] = 2
                            # Fire Node is 2 and 1 (100%) of catching on fire because its on fire already
                            self.fire_maze[i][j] = FireNode(2, 1.0)
                        else:
                            # indicate the cell has a certain chance of catching on fire if its not based on the variable prob
                            self.fire_maze[i][j] = FireNode(0, prob)
                    elif fire_maze[i][j] == 1:  # there is an obstacle
                        # obstacles would be indicated with 1 and have no chance of catching on fire
                        self.fire_maze[i][j] = FireNode(1, 0.0)

        return True

    def dfs(self, beginning, goal):
        if self.tracking_array[beginning[0]][beginning[1]] == 1 or self.tracking_array[goal[0]][goal[1]] == 1:
            return False
        self.fringe.append((beginning[0], beginning[1]))
        while len(self.fringe) > 0:
            current = self.fringe.pop()
            #print(current)
            if current == (goal[0], goal[1]):
                return True
            else:
                if current not in self.visited:
                    if current[1] > 0:
                        if self.tracking_array[current[0]][current[1]-1] == 0 and (current[0], current[1]-1) not in self.fringe and (current[0], current[1]-1) not in self.visited:
                            self.fringe.append((current[0], current[1]-1))
                        if current[0] != self.dim-1 and self.tracking_array[current[0]+1][current[1]] == 0 and (current[0]+1, current[1]) not in self.fringe and (current[0]+1, current[1]) not in self.visited:
                            self.fringe.append((current[0]+1, current[1]))
                        if current[1] != self.dim-1 and self.tracking_array[current[0]][current[1]+1] == 0 and (current[0], current[1]+1) not in self.fringe and (current[0], current[1]+1) not in self.visited:
                            self.fringe.append((current[0], current[1]+1))
                        if current[0] == self.dim-1 and self.tracking_array[current[0]-1][current[1]] == 0 and (current[0]-1, current[1]) not in self.fringe and (current[0]-1, current[1]) not in self.visited:
                            self.fringe.append((current[0]-1, current[1]))
                    else:
                        if current[0] != self.dim-1 and self.tracking_array[current[0]+1][current[1]] == 0 and (current[0]+1, current[1]) not in self.fringe and (current[0]+1, current[1]) not in self.visited:
                            self.fringe.append((current[0]+1, current[1]))
                        if self.tracking_array[current[0]][current[1]+1] == 0 and (current[0], current[1]+1) not in self.fringe and (current[0], current[1]+1) not in self.visited:
                            self.fringe.append((current[0], current[1]+1))
                        if current[0] == self.dim-1 and self.tracking_array[current[0]-1][current[1]] == 0 and (current[0]-1, current[1]) not in self.fringe and (current[0]-1, current[1]) not in self.visited:
                            self.fringe.append((current[0]-1, current[1]))

                self.visited.append(current)

        return False

    # check if the bounds are valid for the given maze
    def check_valid_bounds(self, i, j, pop_value, arr):
        # arg i indicate direction +1 or -1 for up and down
        i = pop_value[0] + i
        # arg j indicates direction +1 or -1 for left and right
        j = pop_value[1] + j
        if i >= 0 and i < len(arr) and j >= 0 and j < len(arr):
            return True  # in bounds, return true
        else:
            return False  # not in bounds, return false

    # strategy 3: finding the way out of the fire
    def fire_route_search(self, start):  # implemented using a modified bfs
        arr = self.tracking_obstacles
        # now define the start and end node which in our case is the first indicies and the last indicies respectively
        goal = (self.dim-1, self.dim-1)

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

            # agent is on fire
            if self.tracking_obstacles[current[0]][current[1]] == 2:
                return []

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
                #print(bfs_route)
                return bfs_route

            else:
                # first check the up direction now checking the probability of cell on fire is less than .3
                if self.check_valid_bounds(-1, 0, current, arr) and arr[current[0] - 1][current[1]] == 0 and self.fire_maze[current[0] - 1][current[1]].fire_prob < .3 and visited[current[0] - 1][current[1]] == False and (current[0] - 1, current[1]) not in fringe:
                    fringe.append((current[0] - 1, current[1]))
                    if current not in path:
                        path.append(current)

                # now check the down direction now checking the probability of cell on fire is less than .3
                if self.check_valid_bounds(1, 0, current, arr) and arr[current[0] + 1][current[1]] == 0 and self.fire_maze[current[0] + 1][current[1]].fire_prob < .3 and visited[current[0] + 1][current[1]] == False and (current[0] + 1, current[1]) not in fringe:
                    fringe.append((current[0] + 1, current[1]))
                    if current not in path:
                        path.append(current)

                # now we can check the left direction now checking the probability of cell on fire is less than .3
                if self.check_valid_bounds(0, -1, current, arr) and arr[current[0]][current[1] - 1] == 0 and self.fire_maze[current[0]][current[1] - 1].fire_prob < .3 and visited[current[0]][current[1] - 1] == False and (current[0], current[1] - 1) not in fringe:
                    fringe.append((current[0], current[1] - 1))
                    if current not in path:
                        path.append(current)

                # finally check the right side now checking the probability of cell on fire is less than .3
                if self.check_valid_bounds(0, 1, current, arr) and arr[current[0]][current[1] + 1] == 0 and self.fire_maze[current[0]][current[1] + 1].fire_prob < .3 and visited[current[0]][current[1] + 1] == False and (current[0], current[1] + 1) not in fringe:
                    fringe.append((current[0], current[1] + 1))
                    if current not in path:
                        path.append(current)
        # return [] is there is no feasible route
        return []

    # this is the name of strategy 3: escape the fire
    def etf(self, flammability):
        ALIVE = True  # indicates if the agent is alive which it will be when it starts
        DEAD = False  # indicates if the agent is dead which it wont be in the start
        start = (0, 0)  # we want to start in the beginning of the maze
        # keep going until ALIVE turns to False (indicating the agent died or no path) or if the agent made it through
        while ALIVE:
            # generate the fire at a given rate based on the command line
            flameRoute = self.generate_fire_maze(flammability)
            if flameRoute == False:
                DEAD = True
                ALIVE = False
                break
            time.sleep(1)  # for calculation
            escape_route = self.fire_route_search(start)
            if len(escape_route) == 0:  # indicates the agent died
                DEAD = True
                ALIVE = False
                break
            # indicates the agent made it through
            elif escape_route[0] == (self.dim-1, self.dim-1):
                break
            # because we are drawing one path at a time make start the next position
            start = escape_route[1]

        if ALIVE == True:  # success
            return ALIVE
        else:  # failure
            return DEAD


def running_tests():
    success = 0
    numTests = 10
    
    tests = [(100, 0.3, 0.1), (100, 0.3, 0.2),
             (100, 0.3, 0.3), (100, 0.3, 0.4), (100, 0.3, 0.5), (100, 0.3, 0.6)]

    while len(tests) != 0:
        curr_test = tests.pop(0)
        while numTests != 0:
            Running_Tests = Maze()
            Running_Tests.build_maze(curr_test[0], curr_test[1])
            result = Running_Tests.etf(curr_test[2])
            if result == True:
                success += 1
            numTests-=1
        f = open("Strategy_3_Success_Rate.txt", "a")
        f.write(str(curr_test[2]) + " " + str(success/10) + "\n")

    plot = pd.read_csv('Strategy_3_Success_Rate.txt', sep='\s+', header=None)
    plot = pd.DataFrame(plot)
    x = plot[0]
    y = plot[1]
    plt.plot(x, y, label='Success vs Flammability')
    plt.xlabel('Flammability')
    plt.ylabel('Average Success')
    plt.title('Average Success Rate vs Flammability at p = 0.3')
    plt.legend()
    plt.savefig('plot214.png')
    plt.show()



# this is where strategy 3 method will be launched from
if __name__ == "__main__":
    running_tests()
