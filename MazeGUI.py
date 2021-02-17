import pygame, sys, random, numpy, math, time, threading
from collections import deque
import Strategy_1 as s1
import Strategy2 as s2
import Strategy_3 as s3

'''
This is the main code where we will run the visualizing for the various graph algorithms for dfs, bfs, a star
and this is where the calls to strategy 1, 2, 3 will happen.
'''

# Color Graphics used in the Maze Visualizer
BLACK = (0, 0, 0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)

class MazeGUI:
    x, y = 0, 0
    cell_size = 10
    dim = 10
    tracking_obstacles = []
    display = None

    # this is where the logic to build the maze is based to create based on a certain obstacle density
    def build_maze(self, screen, size, probability):
        self.x = 0 # reset x upon creating the maze again
        self.y = 0 # reset y upon creating the maze again
        self.dim = size
        self.display = screen
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
            self.x = 10
            self.y += 10
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
                self.x += 10

        self.tracking_obstacles = tracking_array
        return self.tracking_obstacles
    
    # this is for dfs only because it creates a path to start from and a path to end
    def create_maze_dfs(self, screen, size, probability, start, ending):
        # variables to create the visual
        self.x = 0  # reset x on creation
        self.y = 0 # reset y on creation
        self.dim = size
        self.display = screen

        # lets create a tuple for the starting and ending positions
        S = start.split(",") # start is a string input
        G = ending.split(",") # ending is also a string input
        S_T = (int(S[0]), int(S[1]))
        G_T = (int(G[0]), int(G[1]))
        
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

        for k in range(0, size):
            self.x = 10
            self.y += 10
            for b in range(0, size):
                if k == S_T[0] and b == S_T[1]:  # this is what we will define as a start node with yellow
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, YELLOW, cell)
                elif k == G_T[0] and b == G_T[1]:
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, GREEN, cell)
                elif tracking_array[k][b] == 1:
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLACK, cell)
                else:
                    cell = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLACK, cell, 1)
                pygame.display.update()
                self.x += 10

        self.tracking_obstacles = tracking_array
        return self.tracking_obstacles

    def distance_calculator(self, start, end):  # calculates the eucledian distance between current point and goal
        x_diff = abs(start[0] - end[0])
        y_diff = abs(start[1] - end[1])
        return math.sqrt(x_diff**2 + y_diff**2)

    def sorting(self, fringe, child, cost):  # puts the new child in the priority queue depending on it's cost to get there and distance to goal
        return_array = []
        child_dist = self.distance_calculator(child[0])

        if len(fringe) == 0:
            fringe.append(child[0])
            return fringe

        for i in range(0, len(fringe)):
            curr_child_dist = self.distance_calculator(fringe[i])
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

    def a_star(self):  # A* algo
        maze_array = self.tracking_obstacles
        fringe = []  # priority queue
        visited = [[-1, -1, -1]]   # keeps track of all the visited spots
        child1 = []
        child2 = []
        child3 = []
        child4 = []
        n = len(maze_array)
        start = [0, 0]
        cost = numpy.zeros([n, n])
        goal = [n - 1, n - 1]
        tracker = []  # array for final path
        fringe.append(start)
        parent = numpy.zeros([n, n])  # 1 top, 2 right, 3 bottom, 4 left - to keep track of the parent of current node
        while len(fringe) > 0:
            current = fringe.pop(0)  # take out the child with highes priority
            if len(child1) != 0:
                child1.pop()
            if len(child2) != 0:
                child2.pop()
            if len(child3) != 0:
                child3.pop()
            if len(child4) != 0:
                child4.pop()
            if current not in visited:  # only continue if the current node is not visited before
                if not fringe:  # if the fringe is empty do not check for child in fringe
                    if current[0] != 0 and maze_array[current[0] - 1][current[1]] != 1:
                        child1.append([current[0] - 1, current[1]])  # top cell
                        if child1[0] not in visited and cost[current[0] - 1][[current[1]]] >= cost[current[0]][
                            [current[1]]] + 1 or cost[current[0] - 1][[current[1]]] == 0:
                            cost[current[0] - 1][[current[1]]] = cost[current[0]][[current[1]]] + 1
                            fringe = self.sorting(fringe, child1, cost)
                            parent[current[0] - 1][[current[1]]] = 3
                    if current[1] != n - 1 and maze_array[current[0]][current[1] + 1] != 1:
                        child2.append([current[0], current[1] + 1])  # right cell
                        if child2[0] not in visited and cost[current[0]][[current[1] + 1]] >= cost[current[0]][
                            [current[1]]] + 1 or cost[current[0]][[current[1] + 1]] == 0:
                            cost[current[0]][[current[1] + 1]] = cost[current[0]][[current[1]]] + 1
                            fringe = self.sorting(fringe, child2, cost)
                            parent[current[0]][[current[1] + 1]] = 2
                    if current[0] != n - 1 and maze_array[current[0] + 1][current[1]] != 1:
                        child3.append([current[0] + 1, current[1]])  # bottom cell
                        if child3[0] not in visited and cost[current[0] + 1][[current[1]]] >= cost[current[0]][
                            [current[1]]] + 1 or cost[current[0] + 1][[current[1]]] == 0:
                            cost[current[0] + 1][[current[1]]] = cost[current[0]][[current[1]]] + 1
                            fringe = self.sorting(fringe, child3, cost)
                            parent[current[0] + 1][[current[1]]] = 1
                    if current[1] != 0 and maze_array[current[0]][current[1] - 1] != 1:
                        child4.append([current[0], current[1] - 1])  # left cell
                        if child4[0] not in visited and cost[current[0]][[current[1] - 1]] >= cost[current[0]][
                            [current[1]]] + 1 or cost[current[0]][[current[1] - 1]] == 0:
                            cost[current[0]][[current[1] - 1]] = cost[current[0]][[current[1]]] + 1
                            fringe = self.sorting(fringe, child4, cost)
                            parent[current[0]][[current[1] - 1]] = 4
                else:
                    if current not in fringe:  # if current is not in fringe we go through it's neighbours
                        if current[0] != 0 and maze_array[current[0] - 1][current[1]] != 1:
                            child1.append([current[0] - 1, current[1]])  # top cell
                            if child1[0] not in visited and child1[0] not in fringe and cost[current[0] - 1][
                                [current[1]]] >= cost[current[0]][[current[1]]] + 1 or cost[current[0] - 1][
                                [current[1]]] == 0:
                                cost[current[0] - 1][[current[1]]] = cost[current[0]][[current[1]]] + 1
                                fringe = self.sorting(fringe, child1, cost)
                                parent[current[0] - 1][[current[1]]] = 3
                        if current[1] != n - 1 and maze_array[current[0]][current[1] + 1] != 1:
                            child2.append([current[0], current[1] + 1])  # right cell
                            if child2[0] not in visited and child2[0] not in fringe and cost [current[0]][
                                [current[1] + 1]] >= cost[current[0]][[current[1]]] + 1 or cost[current[0]][
                                [current[1] + 1]] == 0:
                                cost[current[0]][[current[1] + 1]] = cost[current[0]][[current[1]]] + 1
                                fringe = self.sorting(fringe, child2, cost)
                                parent[current[0]][[current[1] + 1]] = 2
                        if current[0] != n - 1 and maze_array[current[0] + 1][current[1]] != 1:
                            child3.append([current[0] + 1, current[1]])  # bottom cell
                            if child3[0] not in visited and child3[0] not in fringe and cost[current[0] + 1][
                                [current[1]]] >= cost[current[0]][[current[1]]] + 1 or cost[current[0] + 1][
                                [current[1]]] == 0:
                                cost[current[0] + 1][[current[1]]] = cost[current[0]][[current[1]]] + 1
                                fringe = self.sorting(fringe, child3, cost)
                                parent[current[0] + 1][[current[1]]] = 1
                        if current[1] != 0 and maze_array[current[0]][current[1] - 1] != 1:
                            child4.append([current[0], current[1] - 1])  # left cell
                            if child4[0] not in visited and child4[0] not in fringe and cost[current[0]][
                                [current[1] - 1]] >= cost[current[0]][[current[1]]] + 1 or cost[current[0]][
                                [current[1] - 1]] == 0:
                                cost[current[0]][[current[1] - 1]] = cost[current[0]][[current[1]]] + 1
                                fringe = self.sorting(fringe, child4, cost)
                                parent[current[0]][[current[1] - 1]] = 4
                    visited.append(current)

            if current == goal:  # takes the "parent" array and tracks back to the start using the cell value
                y = n - 1
                x = n - 1
                tracker.append([y, x])
                while True:
                    if parent[y][x] == 1:  # parent is top cell
                        tracker.append([y - 1, x])
                        y -= 1
                    elif parent[y][x] == 2:  # parent is right cell
                        tracker.append([y, x - 1])
                        x -= 1
                    elif parent[y][x] == 3:  # parent is bottom cell
                        tracker.append([y + 1, x])
                        y += 1
                    elif parent[y][x] == 4:  # parent is left cell
                        tracker.append([y, x + 1])
                        x += 1
                    if x == 0 and y == 0:  # when it reaches start it breaks out of the loop
                        break

                tracker.reverse()

                self.draw_path(tracker)  # draws the path
                return True

        return False

    # check if the bounds are valid for the given maze
    def check_valid_bounds(self, i, j, pop_value, arr):
        i = pop_value[0] + i # arg i indicate direction +1 or -1 for up and down
        j = pop_value[1] + j # arg j indicates direction +1 or -1 for left and right
        if i >= 0 and i < len(arr) and j >= 0 and j < len(arr):
            return True # in bounds, return true
        else:
            return False # not in bounds, return false
    
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
                self.bfs_nodes = len(path)
                path.reverse()
                # now that we found the end node, let's perform a recursive backtracking algorithm to find the actual path
                bfs_route = []
                while path[0] != start:
                    new_curr = path.pop(0)
                    if not bfs_route:
                        bfs_route.append(new_curr)
                    # check if its a straight path up
                    elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] + 1 and new_curr[0] == bfs_route[len(bfs_route) - 1][0]:
                        bfs_route.append(new_curr)
                    # check if its a straight path right
                    elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] and new_curr[0] == bfs_route[len(bfs_route) - 1][0] + 1:
                        bfs_route.append(new_curr)
                    # check if its a straight path down
                    elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] - 1 and new_curr[0] == bfs_route[len(bfs_route) - 1][0]:
                        bfs_route.append(new_curr)
                    # check if its a straight path left
                    elif new_curr[1] == bfs_route[len(bfs_route) - 1][1] and new_curr[0] == bfs_route[len(bfs_route) - 1][0] - 1:
                        bfs_route.append(new_curr)

                # append the last node because that won't be included (we check until the starting node)
                bfs_route.append(start)
                bfs_route.reverse()
                self.draw_path(bfs_route) # once the final path is recieved, draw it for the visualization
                return bfs_route

            else:
                # first check the up direction
                if self.check_valid_bounds(-1, 0, current, arr) and arr[current[0] - 1][current[1]] == 0 and visited[current[0] - 1][current[1]] == False and (current[0] - 1, current[1]) not in fringe:
                    fringe.append((current[0] - 1, current[1]))
                    if current not in path: # only append the parent if its not seen in the path already
                        path.append(current)

                # now check the down direction
                if self.check_valid_bounds(1, 0, current, arr) and arr[current[0] + 1][current[1]] == 0 and visited[current[0] + 1][current[1]] == False and (current[0] + 1, current[1]) not in fringe:
                    fringe.append((current[0] + 1, current[1]))
                    if current not in path: # only append the parent if its not seen in the path already
                        path.append(current)

                # now we can check the left direction
                if self.check_valid_bounds(0, -1, current, arr) and arr[current[0]][current[1] - 1] == 0 and visited[current[0]][current[1] - 1] == False and (current[0], current[1] - 1) not in fringe:
                    fringe.append((current[0], current[1] - 1))
                    if current not in path: # only append the parent if its not seen in the path already
                        path.append(current)

                # finally check the right side
                if self.check_valid_bounds(0, 1, current, arr) and arr[current[0]][current[1] + 1] == 0 and visited[current[0]][current[1] + 1] == False and (current[0], current[1] + 1) not in fringe:
                    fringe.append((current[0], current[1] + 1))
                    if current not in path: # only append the parent if its not seen in the path already
                        path.append(current)
        
        # for no given path return [] indicating a blocked route or no path
        return []

    def dfs(self, maze, beginning, goal):
        # based on the maze created this will always be the dim size
        dim = self.dim

        #Tracking items for DFS
        fringe = []
        visited = []
        child1=[]
        child2=[]
        child3=[]
        child4=[]

        #start coordinates
        first=beginning.split(",")
        #end coordinates
        second=goal.split(",")
        #x,y coordinates of start ordered pair
        i= int(first[0]) 
        j =int(first[1])
        #ordered pair (x,y) of end
        target=(int(second[0]),int(second[1]))
        #add start coordinates to the fringe
        fringe.append((i,j))
        while len(fringe) > 0:
            #resetting all children nodes
            if len(child1) !=0:
                child1.pop()
            if len(child2)!=0:
                child2.pop()
            if len(child3)!=0:
                child3.pop()
            if len(child4)!=0:
                child4.pop()
            #Popping topmost node from fringe
            current = fringe.pop()
            #Terminating case
            if current == target:
                return True
            #Current node not equivalent to target node
            else:
                #Start Node or Target Node is Blocked
                if maze[i][j]==1 or maze[int(second[0])][int(second[1])]==1:
                    return False
                #Current Node hasn't been explored and current is empty (not blocked)
                if current not in visited and maze[current[0]][current[1]]==0:
                    #x,y coordinates of Current Node
                    a=current[0]
                    b=current[1]
                    #Current node is in 0th column (leftmost) and right node of current is valid (no bounds error) and empty
                    if current[1] == 0 and maze[a][b+1]!=1 and ((a and b+1) in range(0,dim)):
                        child1.append((current[0], current[1]+1))
                        #Current node not in last row and bottom node of current is valid (no bounds error) and empty   
                        if current[0] != dim-1 and maze[a+1][b]!=1 and ((a+1 and b) in range(0,dim)):
                            child2.append((current[0]+1, current[1]))
                        #Current node not in 0th row (topmost) and top node of current is valid (no bounds error) and empty
                        if current[0] !=0 and maze[a-1][b]!=1 and ((a-1 and b) in range(0,dim)):
                            child2.append((current[0]-1, current[1]))
                    #Current node is not in 0th most column (1 to rightmost)
                    else:
                        #Current node is in row 0 (topmost) but columns (1 to rightmost) or Current is in row dim-1 (bottom most) but columns (1 to rightmost)
                        if (current[0] == 0 and current[1] != 0) or (current[0]==dim-1 and current[1]!=0):
                            #Current's left node is empty and it is valid
                            if maze[a][b-1] !=1:
                                if  ((a and b-1) in range(0,dim)):
                                    child1.append((current[0],current[1]-1))
                                else:
                                    pass
                            #Current node is in 0th row (topmost) and bottom node is valid and empty
                            if current[0] == 0 and maze[a+1][b]!=1 and ((a+1 and b) in range(0,dim)):
                                child2.append((current[0]+1, current[1]))
                            #Current node is in last row and top node valid and empty
                            elif current[0] == dim-1 and maze[a-1][b]!=1 and ((a-1 and b) in range(0,dim)):
                                child2.append((current[0]-1, current[1]))
                            #Current node is not in last column and right node and right node empty and valid 
                            if current[1] != dim-1 and maze[a][b+1]!=1:
                                if ((a and b+1) in range(0,dim)):
                                    child3.append((current[0], current[1]+1))
                                else:
                                    pass
                            #Child3 not in fringe,not visited and has at least 1 element    
                            if len(child3)>0 and child3[0] not in fringe and child3[0] not in visited:
                                    fringe.append((child3[len(child3)-1]))
                        else:
                            #Current node column not rightmost one
                            if current[1]!=dim-1:
                                if maze[a][b-1]!=1 and  ((a and b-1) in range(0,dim)):
                                    child1.append((current[0],current[1]-1))
                                if maze[a-1][b]!=1 and ((a-1 and b) in range(0,dim)):
                                    child2.append((current[0]-1,current[1]))
                                if maze[a][b+1]!=1 and ((a and b+1) in range(0,dim)):
                                    child3.append((current[0],current[1]+1))
                                if maze[a+1][b]!=1 and ((a+1 and b) in range(0,dim)):
                                    child4.append((current[0]+1,current[1]))
                                if len(child3)>0 and child3[0] not in fringe and child3[0] not in visited:
                                    fringe.append((child3[len(child3) - 1]))
                            else:
                                if maze[a][b-1]!=1 and ((a and b-1) in range(0,dim)):
                                    child1.append((current[0], current[1] - 1))
                                if maze[a-1][b]!=1 and ((a-1 and b) in range(0,dim)):    
                                    child2.append((current[0] - 1, current[1]))
                                if maze[a+1][b]!=1 and ((a+1 and b) in range(0,dim)):
                                    child4.append((current[0] + 1, current[1]))
                            if len(child4)>0 and child4[0] not in fringe and child4[0] not in visited:
                                fringe.append((child4[len(child4) - 1]))
                    if len(child1)>0 and child1[0] not in fringe and child1[0] not in visited:
                        fringe.append((child1[len(child1)-1]))

                    if len(child2)>0 and child2[0] not in fringe and child2[0] not in visited:
                        fringe.append((child2[len(child2)-1]))

                    visited.append(current)
        return False
    
    # this method draws the path given by bfs or a star
    def draw_path(self, arr): # arr contains the coordinates of the path to draw
        self.x = 0 # reset x for drawing
        self.y = 0 # reset y for drawing
        screen = self.display
        size = self.dim

        # use the global tracking obstacles to draw
        tracking_array = self.tracking_obstacles
        curr = None # this is where we will pop one element at a time for the array
        
        # pop one element at a time and store that element inside tracking array to draw the path
        for i in range(0, len(tracking_array)):
            for j in range(0, len(tracking_array)):
                if len(arr) > 0:
                    curr = arr.pop(0)
                tracking_array[curr[0]][curr[1]] = 2
        
        # same mechanism as in drawing the maze but now it just includes drawing the full path given by one of the algos used
        for k in range(0, size):
            self.x = 10
            self.y += 10
            for b in range(0, size):
                if k == 0 and b == 0:  # this is what we will define as a start node with yellow
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, YELLOW, cell)
                elif k == size - 1 and b == size - 1: # this is what we will define as a ending node with green
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, GREEN, cell)
                elif tracking_array[k][b] == 1: # this is the cell we will define to be an obstacle
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLACK, cell)
                elif tracking_array[k][b] == 2: # these are the cells that correspond to the path
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLUE, cell)
                else:
                    cell = pygame.Rect(
                        self.x, self.y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLACK, cell, 1)
                pygame.display.update()
                self.x += 10

# this is how we will start the MazeGUI visualization
def start():
    # inital conditions to start pygame
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((500, 500))
    screen.fill('white')
    pygame.display.set_caption("Python Maze Generator")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Comic Sans MS', 30)

    # this is where the main logic will be setup
    maze = MazeGUI() # we need this to start the GUI up

    # now based on the user's request we will run the specific algorithm if they want to run DFS, BFS, or A Star
    if sys.argv[3] == "bfs": # runs bfs
        maze.build_maze(screen, float(sys.argv[1]), int(sys.argv[2])) # start off with building the maze
        maze.bfs_tree_search()
    elif sys.argv[3] == 'a_star': # runs a star
        maze.build_maze(screen, float(sys.argv[1]), int(sys.argv[2])) # start off with building the maze
        maze.a_star()
    elif sys.argv[3] == 'dfs': # if the user command isn't bfs or a star, it will automatically run dfs
        answer = input("Do you want to run DFS on this generated maze for any two points: type yes or no: ")
        if answer.lower() == "yes":
            beginning=input("Enter a start node in the form of x,y: ")
            goal=input("Enter a final node in the form of x,y: ")
            maze.create_maze_dfs(screen, int(sys.argv[1]), float(sys.argv[2]), beginning, goal)
            print(maze.dfs(maze.tracking_obstacles,beginning,goal)) # prints true or false if there is a given path in the console
    
    # if we reach this point this means that the third argument is a strategy we are running s1, s2, or s3
    if sys.argv[3] == 's1':
        s1.start()
    elif sys.argv[3] == 's2':
        s2.start()
    else:
        s3.strategy_3()

    # pygame variables in order to create the visualization and to run pygame in general
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

# this is where the start method will be launched from
if __name__ == "__main__":

    # check the arguments given (has to start with atleast 4)
    if len(sys.argv[1]) >= 4:
        print("Incorrect Usage: Has to be either python MazeGUI.py <dimension size> <probability of generating an obstacle> <algorithm> or python MazeGUI.py <dimension size> <probability of generating an obstacle> <strategy number> <probability of generating fire>")
        exit(1)
    
    # else start
    start()
