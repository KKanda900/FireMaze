import pygame
from pygame_widgets import Button
import sys, re, random

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
        obstacles = (size[0]*size[1])*probability # if the maze area is 100 then there should be only 10 obstacles generated
        for i in range(0,size[0]):
            self.x = 20
            self.y += 20
            for j in range(0,size[1]):
                if i == 0 and j == 0: # this is what we will define as a start node with yellow
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size) 
                    pygame.draw.rect(screen, YELLOW, cell)
                elif i == size[1]-1 and j == size[1]-1:
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size) 
                    pygame.draw.rect(screen, GREEN, cell)
                else:
                    arr = [0,1] # these will represent random choices
                    if random.choice(arr) == 0 and obstacles != 0:
                        cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size) 
                        pygame.draw.rect(screen, BLACK, cell)
                        obstacles -= 1
                    else: 
                        cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size) 
                        pygame.draw.rect(screen, BLACK, cell, 1) 
                pygame.display.update()
                self.x+=20

def start():

    if(len(sys.argv) != 4):
        print("Incorrect Usage: python MazeGUI.py <rows> <cols> <probability>")
        sys.exit(1)

    # command line arguments
    dim = [int(sys.argv[1]), int(sys.argv[2])]
    probability = float(sys.argv[3])

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