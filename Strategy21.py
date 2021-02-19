import pygame, sys, re, random, numpy, math
from pygame_widgets import Button, TextBox
from collections import deque, OrderedDict
import threading, time

# Color Graphics used in the Maze Visualizer
BLACK = (0, 0, 0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
current1=0
dimensions=0
class Node:
    position = ()
    children = []
    g = 0
    h = 0
    f = 0

    def __init__(self, position):
        self.position = position
        children = []
        g = 0
        h = 0
        f = 0

class MazeGUI:
    x, y = 0, 0
    cell_size = 20
    dim = 10
    tracking_obstacles = []
    display = None
    fire_array = None


    def build_maze(self, screen, size, probability):
        self.dim = size
        self.display = screen
        self.fire_array = numpy.zeros((self.dim, self.dim))
        obstacle_num = 0  # See if the amount of obstacles required are 0 or not
        obstacles = (size*size)*probability  # if the maze area is 100 then there should be only 10 obstacles
        tracking_array = numpy.zeros((size, size))  # track where the obstacles are places so it doesn't double count
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

        for k in range(0, size):
            self.x = 20
            self.y += 20
            for b in range(0, size):
                if k == 0 and b == 0:  # this is what we will define as a start node with yellow
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, YELLOW, cell)
                elif k == size-1 and b == size-1:
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, GREEN, cell)
                elif tracking_array[k][b] == 1:
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLACK, cell)
                else:
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLACK, cell, 1)
                pygame.display.update()
                self.x += 20

        self.tracking_obstacles = tracking_array
        return self.tracking_obstacles


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
        fire_array_copy = numpy.zeros((len(fire_maze), len(fire_maze)))  # a copy of the fire_array to keep track of old fires, so the new ones are not counted when calculating probabilities
        for x in range(0, len(fire_maze)):
            for y in range(0, len(fire_maze)):
                fire_array_copy[x][y] = fire_array[x][y]
        if bln:  # if it's the first fire then we chose a stop randomly
            while bln:  # for the first one does a random fire
                y = random.randint(0, len(fire_maze) - 1)  # random x spot for fire
                x = random.randint(0, len(fire_maze) - 1)  # random y spot for fire
                if fire_maze[x][y] != 2 and fire_maze[x][y] != 1 and (x != 0 and y != 0) and (
                        x != len(fire_maze) - 1 and y != len(fire_maze) - 1):  # only generate fire if there is no obstacle there and it's not the start or goal
                    fire_array[x][y] = 2
                    self.tracking_obstacles[x][y] = 2
                    return self.tracking_obstacles  # return the maze array
        else:
            for i in range(0, len(self.tracking_obstacles)):  # if it's not the first time then we traverse through every cell
                for j in range(0, len(self.tracking_obstacles)):  # for each cell we calculate the probability fo it catching fire depending on how many of it's neighbours are on fire
                    fire = 0
                    if fire_maze[i][j] != 1 and fire_array[i][j] != 2:
                        if i != len(self.tracking_obstacles) - 1 and fire_array_copy[i + 1][j] == 2:  # we use the copy of fire array to make sure a new fire is not counted in the calculations
                            fire += 1  # bottom cell
                        if fire_array_copy[i - 1][j] == 2 and i != 0:
                            fire += 1  # top cell
                        if j != len(self.tracking_obstacles) - 1 and fire_array_copy[i][j + 1] == 2:
                            fire += 1  # right cell
                        if fire_array_copy[i][j - 1] == 2 and j != 0:
                            fire += 1  # left cell
                        prob = 1 - ((1 - q) ** fire)  # calculate the probability with given formula
                        if fire > 0 and random.random() <= prob and prob > 0:  # if it catches on fire
                            fire_array[i][j] = 2  # update the fire tracking array
                            self.tracking_obstacles[i][j] = 2  # update the actual maze array
        self.x = 0
        self.y = 0
        screen = self.display
        size = self.dim
        tracking_array = self.tracking_obstacles

        for k in range(0, size):
            self.x = 20
            self.y += 20
            for b in range(0, size):
                if k == 0 and b == 0:  # this is what we will define as a start node with yellow
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, YELLOW, cell)
                elif k == size-1 and b == size-1:  # goal node
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, GREEN, cell)
                elif tracking_array[k][b] == 1:
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLACK, cell)
                elif fire_array[k][b] == 2:
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLUE, cell)
                else:
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLACK, cell, 1)
                pygame.display.update()
                self.x += 20
        return self.tracking_obstacles

    def bfs_tree_search1(self,start,goal):
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

    def strategy2(self):
        path1=[]
        self.generate_fire_maze1(0.3,True)
        time.sleep(1.5)
        path=self.bfs_tree_search1((0,0),(int(sys.argv[1])-1,int(sys.argv[1])-1))
        if path==False:
            return False
        path1.append(path[0])
        x=len(path1)
        while(x!=0):
            self.generate_fire_maze1(0.3,False)
            time.sleep(1)         
            path1=self.bfs_tree_search1(path1[0],(int(sys.argv[1])-1,int(sys.argv[1])-1))
            if path1==False:
                return False
            time.sleep(1)
            path1=self.bfs_tree_search1(path1[1],(int(sys.argv[1])-1,int(sys.argv[1])-1))
            if path1==False:
                return False
            
            self.draw_path(path1[0])
            if path1[0]==(int(sys.argv[1])-1,int(sys.argv[1])-1):
                return True
    
    def draw_path(self, position): # arr contains the coordinates of the path to draw
        self.x = 0
        self.y = 0
        screen = self.display
        size = self.dim
        tracking_array = self.tracking_obstacles
        curr = None
        
        curr = position
        tracking_array[curr[0]][curr[1]] = 3
                
        for k in range(0, size):
            self.x = 20
            self.y += 20
            for b in range(0, size):
                if k == 0 and b == 0:  # this is what we will define as a start node with yellow
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, YELLOW, cell)
                elif k == size - 1 and b == size - 1:
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, GREEN, cell)
                elif tracking_array[k][b] == 1:
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLACK, cell)
                elif tracking_array[k][b] == 2:
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLUE, cell)
                elif tracking_array[k][b] == 3:
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, RED, cell)
                else:
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLACK, cell, 1)
                pygame.display.update()
                self.x += 20
    
def start():

    if(len(sys.argv) != 4):
        print("Incorrect Usage: python MazeGUI.py <dim> <probability> <algorithm>")
        sys.exit(1)

    # command line arguments
    dim = int(sys.argv[1])
    probability = float(sys.argv[2])

    # inital conditions to start pygame
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1000, 500))
    screen.fill('white')
    pygame.display.set_caption("Python Maze Generator")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Comic Sans MS', 30)

    maze = MazeGUI()
    maze.build_maze(screen, dim, probability)
    print(maze.strategy2())
    
    running = True
    
    index = 0
    while running:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # update pygame's display to display everything
        pygame.display.update()


if __name__ == "__main__":
    start()