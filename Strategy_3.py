import pygame, sys, random, numpy, math, threading, time
from pygame_widgets import Button, TextBox
from collections import deque, OrderedDict

# Color Graphics used in the Maze Visualizer
BLACK = (0, 0, 0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)

# these nodes will be placed in a 2D array to represent the Node's probability of catching on fire and the value (0 for clear cell, 1 for occupied with obstacle, 2 for occupied with fire)
class FireNode:
    fire_prob = 0.0 
    value = 0

    def __init__(self, value, prob_fire):
        self.fire_prob = prob_fire
        self.value = value

class MazeGUI:
    x, y = 0, 0
    cell_size = 20
    dim = 10
    tracking_obstacles = []
    display = None
    fire_array = numpy.zeros((dim, dim))
    fire_maze = None
    fire_index = 0

    # this is where the logic to build the maze is based to create based on a certain obstacle density
    def build_maze(self, screen, size, probability):
        self.dim = size
        self.display = screen
        obstacle_num = 0  # See if the amount of obstacles required are 0 or not
        obstacles = (size*size)*probability  # if the maze area is 100 then there should be only 10 obstacles
        tracking_array = numpy.zeros((size, size))  # track where the obstacles are places so it doesn't double count
        dim_array = list(range(0, size))
        self.fire_maze = [[FireNode(0, 0.0) for x in range(self.dim)] for y in range(self.dim)] # generate the fire maze intial upon start
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

    # this is where the primary logic goes to create the fire in the maze overall to create dynamic mazes
    def generate_fire_maze(self, probability):
        q = probability # the likely hood of a cell catching on fire
        
        fire_maze = self.tracking_obstacles # tracking obstacles in our case will also track fire now
        fire_array = self.fire_array # fire_array will represent a dynamically changing maze
        fire_array_copy = numpy.zeros((len(fire_maze), len(fire_maze))) # copy the contents of fire maze into the copy in order to get accurate places to store the fire
        
        # copy the contents of fire_array into fire_array_copy
        for x in range(0, len(fire_maze)):
            for y in range(0, len(fire_maze)):
                fire_array_copy[x][y] = fire_array[x][y]
        
        # the first fire being placed is placed randomly in the maze so we want to check if this is the first fire being generated
        if self.fire_index == 0:
            while self.fire_index == 0:  # for the first one does a random fire
                y = random.randint(0, len(fire_maze) - 1) # get a random y index based on the size of the maze
                x = random.randint(0, len(fire_maze) - 1) # get a radnom x index based on the size of the maze
                if fire_maze[x][y] != 2 and fire_maze[x][y] != 1 and (x != 0 and y != 0) and (x != len(fire_maze) - 1 and y != len(fire_maze) - 1): # if a spot is already not on fire and not the first or last cell make it on fire
                    fire_array[x][y] = 2 # 2 indicates there is fire placed
                    self.tracking_obstacles[x][y] = 2 # this is so we can take account for the maze globally
                    self.fire_index += 1 # increase this so we dont choose another random spot
                    self.fire_maze[x][y] = FireNode(2, 1.0) # Fire Node is 2 and 1 (100%) of catching on fire because its on fire already
                    return self.tracking_obstacles
        else:
            # now that we choose one spot on the maze to catch on fire, the fire can move only one spot and the chance is based on the neighbors that are on fire
            for i in range(0, len(self.tracking_obstacles)):
                for j in range(0, len(self.tracking_obstacles)):
                    fire = 0 # to track the fire neighbors
                    if fire_maze[i][j] != 1 and fire_array[i][j] != 2:
                        if i != len(self.tracking_obstacles) - 1 and fire_array_copy[i + 1][j] == 2: # check the below neighbor
                            fire += 1
                        if fire_array_copy[i - 1][j] == 2 and i != 0: # check the up neighbor
                            fire += 1
                        if j != len(self.tracking_obstacles) - 1 and fire_array_copy[i][j + 1] == 2: # check the right neighbor
                            fire += 1
                        if fire_array_copy[i][j - 1] == 2 and j != 0: # check the left neighbor
                            fire += 1
                        prob = 1 - ((1 - q) ** fire) # calculate the probability of a cell catching on fire
                        if fire > 0 and random.random() <= prob and prob > 0:
                            fire_array[i][j] = 2 # track it locally
                            self.tracking_obstacles[i][j] = 2 # track it globally
                            self.fire_maze[i][j] = FireNode(2, 1.0) # Fire Node is 2 and 1 (100%) of catching on fire because its on fire already
                        else:
                            # indicate the cell has a certain chance of catching on fire if its not based on the variable prob
                            self.fire_maze[i][j] = FireNode(0, prob)
                    elif fire_maze[i][j] == 1: # there is an obstacle
                        self.fire_maze[i][j] = FireNode(1, 0.0) # obstacles would be indicated with 1 and have no chance of catching on fire

        return self.tracking_obstacles

    # check if the bounds are valid for the given maze
    def check_valid_bounds(self, i, j, pop_value, arr):
        i = pop_value[0] + i # arg i indicate direction +1 or -1 for up and down
        j = pop_value[1] + j # arg j indicates direction +1 or -1 for left and right
        if i >= 0 and i < len(arr) and j >= 0 and j < len(arr):
            return True # in bounds, return true
        else:
            return False # not in bounds, return false
    
    # strategy 3: finding the way out of the fire
    def fire_route_search(self, start): # implemented using a modified bfs
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

            if self.tracking_obstacles[current[0]][current[1]] == 2: # agent is on fire
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
    def etf(self):
        ALIVE = True # indicates if the agent is alive which it will be when it starts
        DEAD = False # indicates if the agent is dead which it wont be in the start
        start = (0, 0) # we want to start in the beginning of the maze
        # keep going until ALIVE turns to False (indicating the agent died or no path) or if the agent made it through 
        while ALIVE:
            self.generate_fire_maze(float(sys.argv[4])) # generate the fire at a given rate based on the command line 
            time.sleep(1) # for calculation
            escape_route = self.fire_route_search(start)
            if len(escape_route) == 0: # indicates the agent died
                DEAD = True
                ALIVE = False
                break
            elif escape_route[0] == (self.dim-1, self.dim-1): # indicates the agent made it through
                break
            # keep drawing the agent going through the maze
            self.draw_path(escape_route[1])
            start = escape_route[1] # because we are drawing one path at a time make start the next position
            
        if ALIVE == True: # success
            exit()
            return ALIVE
        else: # failure
            exit()
            return DEAD
    
    # same drawing mechanism used to draw the static mazes except we indicate a single position which we draw in the maze instead of a full path
    def draw_path(self, position): # modified drawing function to go based on a single position
        self.x = 0 # reset x for drawing
        self.y = 0 # reset y for drawing
        screen = self.display
        size = self.dim

        # use the global tracking obstacles to draw
        tracking_array = self.tracking_obstacles
        curr = None # this is where we will pop one element at a time for the array
        
        # there is only position so curr would be that position
        curr = position
        tracking_array[curr[0]][curr[1]] = 3
        
        # same premise as in build function except drawing the path now
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
                    pygame.draw.rect(screen, RED, cell)
                elif tracking_array[k][b] == 3:
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLUE, cell)
                else:
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLACK, cell, 1)
                pygame.display.update()
                self.x += 20

# this is where we will house the logic for strategy 3 visualization
def strategy_3():
    # command line arguments
    dim = int(sys.argv[1])
    probability = float(sys.argv[2])

    # inital conditions to start pygame
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1000, 1000))
    screen.fill('white')
    pygame.display.set_caption("Python Maze Generator")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Comic Sans MS', 30)

    maze = MazeGUI()
    print(maze.build_maze(screen, dim, probability))

    maze.etf()

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

# this is where strategy 3 method will be launched from
if __name__ == "__main__":
    strategy_3()
