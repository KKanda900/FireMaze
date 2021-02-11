import pygame, sys, re, random, numpy, math
from pygame_widgets import Button
from collections import deque, OrderedDict
import threading

# Color Graphics used in the Maze Visualizer
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


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
    dim = 0
    tracking_obstacles = []
    display = None

    def build_maze(self, screen, size, probability):
        self.dim = size
        self.display = screen
        obstacle_num = 0  # See if the amount of obstacles required are 0 or not
        obstacles = int((size * size) * probability)  # if the maze area is 100 then there should be only 10 obstacles
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

        for k in range(0, size):
            self.x = 20
            self.y += 20
            for b in range(0, size):
                if k == 0 and b == 0:  # this is what we will define as a start node with yellow
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, YELLOW, cell)
                elif k == size - 1 and b == size - 1:
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

    def check_valid_bounds(self, i, j, pop_value, arr):
        i = pop_value[0] + i
        j = pop_value[1] + j
        if i >= 0 and i < len(arr) and j >= 0 and j < len(arr):
            return True
        else:
            return False

    def bfs_tree_search(self):
        arr = self.tracking_obstacles

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
                path.reverse()
                # now that we found the end node, let's perform a recursive backtracking algorithm to find the actual path
                bfs_route = []
                while path[0] != start:
                    new_curr = path.pop(0)
                    if not bfs_route:
                        bfs_route.append(new_curr)
                    # top
                    elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] + 1 and new_curr[0] == \
                            bfs_route[len(bfs_route) - 1][0]:
                        bfs_route.append(new_curr)
                    # right
                    elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] and new_curr[0] == \
                            bfs_route[len(bfs_route) - 1][0] + 1:
                        bfs_route.append(new_curr)
                    # bottom
                    elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] - 1 and new_curr[0] == \
                            bfs_route[len(bfs_route) - 1][0]:
                        bfs_route.append(new_curr)
                    # left
                    elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] and new_curr[0] == \
                            bfs_route[len(bfs_route) - 1][0] - 1:
                        bfs_route.append(new_curr)

                bfs_route.append(start)
                bfs_route.reverse()
                self.draw_path(list(bfs_route))
            else:
                # first check the up direction
                if self.check_valid_bounds(-1, 0, current, arr) and arr[current[0] - 1][current[1]] == 0 and \
                        visited[current[0] - 1][current[1]] == False and (current[0] - 1, current[1]) not in fringe:
                    fringe.append((current[0] - 1, current[1]))
                    if current not in path:
                        path.append(current)

                # now check the down direction
                if self.check_valid_bounds(1, 0, current, arr) and arr[current[0] + 1][current[1]] == 0 and \
                        visited[current[0] + 1][current[1]] == False and (current[0] + 1, current[1]) not in fringe:
                    fringe.append((current[0] + 1, current[1]))
                    if current not in path:
                        path.append(current)

                # now we can check the left direction
                if self.check_valid_bounds(0, -1, current, arr) and arr[current[0]][current[1] - 1] == 0 and \
                        visited[current[0]][current[1] - 1] == False and (current[0], current[1] - 1) not in fringe:
                    fringe.append((current[0], current[1] - 1))
                    if current not in path:
                        path.append(current)

                # finally check the right side
                if self.check_valid_bounds(0, 1, current, arr) and arr[current[0]][current[1] + 1] == 0 and \
                        visited[current[0]][current[1] + 1] == False and (current[0], current[1] + 1) not in fringe:
                    fringe.append((current[0], current[1] + 1))
                    if current not in path:
                        path.append(current)

        return []

    def draw_path(self, arr):  # arr contains the coordinates of the path to draw
        self.x = 0
        self.y = 0
        screen = self.display
        size = self.dim
        tracking_array = self.tracking_obstacles
        curr = None

        for i in range(0, len(tracking_array)):
            for j in range(0, len(tracking_array)):
                if len(arr) > 0:
                    curr = arr.pop(0)
                tracking_array[curr[0]][curr[1]] = 2

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
                else:
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLACK, cell, 1)
                pygame.display.update()
                self.x += 20

    def a_star(self):
        arr = self.tracking_obstacles
        start = (0, 0)
        end = (len(arr)-1, len(arr)-1)
        endNode = Node((len(arr)-1, len(arr)-1))
        visited = numpy.zeros((len(arr), len(arr)), dtype=bool)

        openset = []
        closedset = []
        parent = []

        openset.append(Node(start))

        while len(openset) > 0:
            currentNode = openset.pop(0)
            visited[currentNode.position[0]][currentNode.position[1]] = True
            closedset.append(currentNode)

            for nodes in openset:
                if nodes.f < currentNode.f:
                    currentNode = nodes

            if currentNode.position == end:
                """ for paths in parent:
                    print(paths.position) """
                parent.append(currentNode.position)
                parent.reverse()
                a_star_route = []
                while parent[0] != start:
                    new_curr = parent.pop(0)
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
                print(a_star_route)
                return True

            if check_valid_bounds(1, 0, currentNode, arr) and visited[currentNode.position[0]+1][currentNode.position[1]] == False and arr[currentNode.position[0]+1][currentNode.position[1]] != 1 and Node((currentNode.position[0]+1, currentNode.position[1])) not in openset:
                temp = Node((currentNode.position[0]+1, currentNode.position[1]))
                currentNode.children.append(temp)

            if check_valid_bounds(-1, 0, currentNode, arr) and visited[currentNode.position[0]-1][currentNode.position[1]] == False and arr[currentNode.position[0]-1][currentNode.position[1]] != 1 and Node((currentNode.position[0]-1, currentNode.position[1])) not in openset:
                temp = Node((currentNode.position[0]-1, currentNode.position[1]))
                currentNode.children.append(temp)

            if check_valid_bounds(0, 1, currentNode, arr) and visited[currentNode.position[0]][currentNode.position[1]+1] == False and arr[currentNode.position[0]][currentNode.position[1]+1] != 1 and Node((currentNode.position[0], currentNode.position[1]+1)) not in openset:
                temp = Node((currentNode.position[0], currentNode.position[1]+1))
                currentNode.children.append(temp)

            if check_valid_bounds(0, -1, currentNode, arr) and visited[currentNode.position[0]][currentNode.position[1]-1] and arr[currentNode.position[0]][currentNode.position[1]-1] != 1 and Node((currentNode.position[0], currentNode.position[1]-1)) not in openset:
                temp = Node((currentNode.position[0], currentNode.position[1]-1))
                currentNode.children.append(temp)

            for child in currentNode.children:
                if child in closedset:
                    continue

                child.g = currentNode.g + 1
                child.h = distance_calculator(child.position, endNode.position)
                child.f = child.g + child.h

                if child in openset and child.g > (currentNode.g + distance_calculator(currentNode.position, child.position)):
                    continue
                openset.append(child)
                if currentNode not in parent:
                    parent.append(currentNode.position)

        return []

    def distance_calculator(self, start, end):
        x_diff = ((start[0] - end[0])**2)
        y_diff = ((start[1] - end[1])**2)
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


def start():

    # command line arguments
    dim = 10
    probability = .2

    # inital conditions to start pygame
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((600, 600))
    screen.fill('white')
    pygame.display.set_caption("Python Maze Generator")
    clock = pygame.time.Clock()

    maze = MazeGUI()
    maze.build_maze(screen, dim, probability)
    #print(maze.bfs_tree_search())
    maze.a_star()


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
