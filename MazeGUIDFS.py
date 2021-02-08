import pygame
from pygame_widgets import Button
import sys, re, random, numpy

#DFS Lists
fringe = []
visited = []
child1=[]
child2=[]
child3=[]
child4=[]
# Color Graphics used in the Maze Visualizer
BLACK = (0, 0, 0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
dim = int(input("Enter a dimension (max of 40)"))
probability = float(input("Enter probability (between 0 and 1)"))
tracking_array = numpy.zeros((dim, dim)) # track where the obstacles are places so it doesn't double count
class MazeGUI:
    x, y = 0, 0
    cell_size = 20

    def build_maze(self, screen, size, probability):
        obstacle_num = 0  # See if the amount of obstacles required are 0 or not
        obstacles = int((size*size)*probability)  # if the maze area is 100 then there should be only 10 obstacles
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

def dfs(maze, beginning, goal):
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
def start():

    #if(len(sys.argv) != 3):
       # print("Incorrect Usage: python MazeGUI.py <dim> <probability>")
       # sys.exit(1)

   
    # command line arguments
    #dim = int(sys.argv[1])
    #probability = float(sys.argv[2])

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
    answer = input("Do you want to run DFS on this generated maze for any two points: type yes or no")
    if answer.lower() == "yes":
        beginning=input("Enter a start node in the form of x,y")
        goal=input("Enter a final node in the form of x,y")
        print(dfs(tracking_array,beginning,goal))
    else:
        pass
if __name__ == "__main__":
    start()
