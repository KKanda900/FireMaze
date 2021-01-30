import pygame
from pygame_widgets import Button
import sys, re

# Color Graphics used in the Maze Visualizer
BLACK = (0, 0, 0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)

class MazeGUI:
    x, y = 0, 0
    cell_size = 20

    def build_maze(self, screen, size):
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
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size) 
                    pygame.draw.rect(screen, BLACK, cell, 1) # the 1 here is to define thickness of the cell
                pygame.display.update()
                self.x+=20

def start():

    if(len(sys.argv) != 4):
        print("Incorrect Usage: python MazeGUI.py <rows> <cols> <probability>")
        sys.exit(1)

    dim = [int(sys.argv[1]), int(sys.argv[2])]

    # inital conditions to start pygame
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1000, 1000))
    screen.fill('white')
    pygame.display.set_caption("Python Maze Generator")
    clock = pygame.time.Clock()
    
    # buttons to conduct various graphing algorithms: dfs, bfs, and a*
    dfs = Button(screen, 5, 500, 100, 30, text='Run DFS', fontSize=20, margin=20, inactiveColour=RED, pressedColour=BLUE, radius=20, onClick=None)
    dfs.draw()
    bfs = Button(screen, 60, 500, 100, 30, text='Run BFS', fontSize=20, margin=20, inactiveColour=RED, pressedColour=BLUE, radius=20, onClick=None)
    bfs.draw()
    a_star = Button(screen, 100, 500, 100, 30, text='Run A*', fontSize=20, margin=20, inactiveColour=RED, pressedColour=BLUE, radius=20, onClick=None)
    a_star.draw() 

    maze = MazeGUI()
    maze.build_maze(screen, dim)
    running = True
    index = 0
    while running:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # listen for events
        dfs.listen(events)
        bfs.listen(events)
        a_star.listen(events)

        # update pygame's display to display everything
        pygame.display.update()

if __name__ == "__main__":
    start()