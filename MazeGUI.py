import pygame, sys, re, random, numpy
from pygame_widgets import Button
from collections import deque

# Color Graphics used in the Maze Visualizer
BLACK = (0, 0, 0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)

class MazeGUI:
    x, y = 0, 0
    cell_size = 20
    dim = 0
    tracking_obstacles = []
    display = None

    def build_maze(self, screen, size, probability):
        self.dim = size
        self.display = screen
        obstacle_num = 0  # See if the amount of obstacles required are 0 or not
        obstacles = int((size*size)*probability)  # if the maze area is 100 then there should be only 10 obstacles
        tracking_array = numpy.zeros((size, size))  # track where the obstacles are places so it doesn't double count
        while obstacles != 0:
            for i in range(0, size):
                for j in range(0, size):
                    if i == 0 and j == 0:  # this is what we will define as a start node with yellow
                        pass
                    elif i == size-1 and j == size-1:
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

        counter = 0  # to count the obstacles
        for i in range(0, size):
            for j in range(0, size):
                if tracking_array[i][j] == 1:
                    counter += 1

    def check_valid_bounds(self, i, j, pop_value, arr):
        i = pop_value[0] + i
        j = pop_value[1] + j
        if i >= 0 and i < len(arr) and j >= 0 and j < len(arr):
            return True
        else:
            return False
    
    def bfs_tree_search(self):
        # now define the start and end node which in our case is the first indicies and the last indicies respectively
        start = (0, 0)
        goal = (len(self.tracking_obstacles) - 1, len(self.tracking_obstacles) - 1)

        # now because we are working with bfs, we know bfs calls for a fringe in the form of a queue because of the queue's policy (FIFO)
        fringe = deque()
        fringe.append(start)

        print(self.tracking_obstacles)

        # keep an self.tracking_obstaclesay to represent the visited self.tracking_obstaclesays
        visited = numpy.zeros((len(self.tracking_obstacles), len(self.tracking_obstacles)), dtype=bool)

        # for this implementation of bfs we want to keep track of the parents to obtain the shortest path
        path = []

        # now iterate through the fringe to check for the path
        while len(fringe) > 0:
            current = fringe.popleft()
            print(current)
            visited[current[0]][current[1]] = True
            if current == goal:
                path.append(current)
                path.reverse()
                # now that we found the end node, let's perform a recursive backtracking algorithm to find the actual path
                bfs_route = []
                while path[0] != start:
                    new_curr = path.pop(0)
                    if new_curr[1] == path[0][1] + 1 and new_curr[0] == path[0][0]:  # top
                        bfs_route.append(new_curr)
                    elif new_curr[1] == path[0][1] and new_curr[0] == path[0][0] + 1:  # right
                        bfs_route.append(new_curr)
                    elif new_curr[1] == path[0][1] - 1 and new_curr[0] == path[0][0]:  # bottom
                        bfs_route.append(new_curr)
                    elif new_curr[1] == path[0][1] and new_curr[0] == path[0][0] - 1:  # left
                        bfs_route.append(new_curr)
                    else:
                        pass
                bfs_route.append(start)
                bfs_route.reverse()
                self.draw_path(list(bfs_route))
                return list(bfs_route)
            else:
                # first check the up direction
                if check_valid_bounds(-1, 0, current, self.tracking_obstacles) and self.tracking_obstacles[current[0] - 1][current[1]] == 0 and visited[current[0] - 1][current[1]] == False:
                    fringe.append((current[0] - 1, current[1]))
                    path.append(current)

                # now check the down direction
                if check_valid_bounds(1, 0, current, self.tracking_obstacles) and self.tracking_obstacles[current[0] + 1][current[1]] == 0 and visited[current[0] + 1][current[1]] == False:
                    fringe.append((current[0] + 1, current[1]))
                    path.append(current)

                # now we can check the left direction
                if check_valid_bounds(0, -1, current, self.tracking_obstacles) and self.tracking_obstacles[current[0]][current[1] - 1] == 0 and visited[current[0]][current[1] - 1] == False:
                    fringe.append((current[0], current[1] - 1))
                    path.append(current)

                # finally check the right side
                if check_valid_bounds(0, 1, current, self.tracking_obstacles) and self.tracking_obstacles[current[0]][current[1] + 1] == 0 and visited[current[0]][current[1] + 1] == False:
                    fringe.append((current[0], current[1] + 1))
                    path.append(current)
        return []
    
    def draw_path(self, arr): # arr contains the coordinates of the path to draw
        self.x = 0
        self.y = 0
        screen = self.display
        size = self.dim
        tracking_array = self.tracking_obstacles
        for k in range(0, size):
            self.x = 20
            self.y += 20
            for b in range(0, size):
                curr = arr.pop()
                if k == 0 and b == 0:  # this is what we will define as a start node with yellow
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, YELLOW, cell)
                elif k == size-1 and b == size-1:
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, GREEN, cell)
                elif tracking_array[k][b] == 1:
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLACK, cell)
                elif k == curr[0] and b == curr[1]:
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLUE, cell)
                else:
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLACK, cell, 1)
                pygame.display.update()
                self.x += 20


def start():

    if(len(sys.argv) != 3):
        print("Incorrect Usage: python MazeGUI.py <dim> <probability>")
        sys.exit(1)

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

    maze = MazeGUI()
    maze.build_maze(screen, dim, probability)
    
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
