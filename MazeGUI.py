import pygame
from pygame_widgets import Button
import sys, re, random, numpy

# Color Graphics used in the Maze Visualizer
BLACK = (0, 0, 0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)

class MazeGUI:
    x, y = 0, 0
    cell_size = 20

    def build_maze(self, screen, size, probability):
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

        counter = 0  # to count the obstacles
        for i in range(0, size):
            for j in range(0, size):
                if tracking_array[i][j] == 1:
                    counter += 1


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
    screen = pygame.display.set_mode((500, 500))
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