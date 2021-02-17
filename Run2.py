
import sys, random, numpy, math, time, threading
from collections import deque
import pandas as pd
import matplotlib.pyplot as plt

'''
The purpose of Run_Tests.py is to conduct tests on the various algorithms we implemented in 
specific scenerios.
'''

class Maze:
    x, y = 0, 0
    cell_size = 3
    dim = 10
    tracking_obstacles = []
    display = None
    bfs_nodes = 0
    a_star_nodes = 0
    tracking_array=[]
    fringe = []
    visited = []
    child1=[]
    child2=[]
    child3=[]
    child4=[]
    probability=0
    def build_maze(self, size, probability):
        self.x = 0 
        self.y = 0
        self.dim = size
        self.probability=probability
        obstacle_num = 0  # See if the amount of obstacles required are 0 or not
        obstacles = (size*size)*probability  # if the maze area is 100 then there should be only 10 obstacles
        self.tracking_array = numpy.zeros((size, size))  # track where the obstacles are places so it doesn't double count
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
                if random.choice(arr) == 0 and obstacles != 0 and self.tracking_array[i][j] == 0:
                    self.tracking_array[i][j] = 1
                    obstacles -= 1

        return self.tracking_array

    def distance_calculator(self, start, end):
        x_diff = abs(start[0] - end[0])
        y_diff = abs(start[1] - end[1])
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

        
    def check_valid_bounds(self, i, j, pop_value, arr):
        i = pop_value[0] + i
        j = pop_value[1] + j
        if i >= 0 and i < len(arr) and j >= 0 and j < len(arr):
            return True
        else:
            return False
    
    def dfs(self, beginning, goal):
        #start coordinates
        #first=beginning.split(",")
        #end coordinates
        #second=goal.split(",")
        #x,y coordinates of start ordered pair
        i= int(beginning[0]) 
        j =int(beginning[1])
        #ordered pair (x,y) of end
        target=(goal[0],goal[1])
        #add start coordinates to the fringe
        self.fringe.append((i,j))
        while len(self.fringe) > 0:
            #resetting all children nodes
            if len(self.child1) !=0:
                self.child1.pop()
            if len(self.child2)!=0:
                self.child2.pop()
            if len(self.child3)!=0:
                self.child3.pop()
            if len(self.child4)!=0:
                self.child4.pop()
            #Popping topmost node from fringe
            current = self.fringe.pop()
            #Terminating case
            if current == target:
                return True
            #Current node not equivalent to target node
            else:
                #Start Node or Target Node is Blocked
                if self.tracking_array[i][j]==1 or self.tracking_array[target[0]][target[1]]==1:
                    return False
                #Current Node hasn't been explored and current is empty (not blocked)
                if current not in self.visited and self.tracking_array[current[0]][current[1]]==0:
                    #x,y coordinates of Current Node
                    a=current[0]
                    b=current[1]
                    #print(a,b)
                    #Current node is in 0th column (leftmost) and right node of current is valid (no bounds error) and empty
                    if current[1] == 0 and self.tracking_array[a][b+1]!=1 and ((a and b+1) in range(0,self.dim)):
                        self.child1.append((current[0], current[1]+1))
                        #Current node not in last row and bottom node of current is valid (no bounds error) and empty   
                        if current[0] != self.dim-1 and self.tracking_array[a+1][b]!=1 and ((a+1 and b) in range(0,self.dim)):
                            self.child2.append((current[0]+1, current[1]))
                        #Current node not in 0th row (topmost) and top node of current is valid (no bounds error) and empty
                        if current[0] !=0 and self.tracking_array[a-1][b]!=1 and ((a-1 and b) in range(0,self.dim)):
                            self.child2.append((current[0]-1, current[1]))
                    #Current node is not in 0th most column (1 to rightmost)
                    else:
                        #Current node is in row 0 (topmost) but columns (1 to rightmost) or Current is in row dim-1 (bottom most) but columns (1 to rightmost)
                        if (current[0] == 0 and current[1] != 0) or (current[0]==self.dim-1 and current[1]!=0):
                            #Current's left node is empty and it is valid
                            if self.tracking_array[a][b-1] !=1:
                                if  ((a and b-1) in range(0,self.dim)):
                                    self.child1.append((current[0],current[1]-1))
                                else:
                                    pass
                            #Current node is in 0th row (topmost) and bottom node is valid and empty
                            if current[0] == 0 and self.tracking_array[a+1][b]!=1 and ((a+1 and b) in range(0,self.dim)):
                                self.child2.append((current[0]+1, current[1]))
                            #Current node is in last row and top node valid and empty
                            elif current[0] == self.dim-1 and self.tracking_array[a-1][b]!=1 and ((a-1 and b) in range(0,self.dim)):
                                self.child2.append((current[0]-1, current[1]))
                            #Current node is not in last column and right node and right node empty and valid 
                            if current[1] != self.dim-1 and self.tracking_array[a][b+1]!=1:
                                if ((a and b+1) in range(0,self.dim)):
                                    self.child3.append((current[0], current[1]+1))
                                else:
                                    pass
                            #Child3 not in fringe,not visited and has at least 1 element    
                            if len(self.child3)>0 and self.child3[0] not in self.fringe and self.child3[0] not in self.visited:
                                    self.fringe.append((self.child3[len(self.child3)-1]))
                        else:
                            #Current node column not rightmost one
                            if current[1]!=self.dim-1:
                                if self.tracking_array[a][b-1]!=1 and  ((a and b-1) in range(0,self.dim)):
                                    self.child1.append((current[0],current[1]-1))
                                if self.tracking_array[a-1][b]!=1 and ((a-1 and b) in range(0,self.dim)):
                                    self.child2.append((current[0]-1,current[1]))
                                if self.tracking_array[a][b+1]!=1 and ((a and b+1) in range(0,self.dim)):
                                    self.child3.append((current[0],current[1]+1))
                                if self.tracking_array[a+1][b]!=1 and ((a+1 and b) in range(0,self.dim)):
                                    self.child4.append((current[0]+1,current[1]))
                                if len(self.child3)>0 and self.child3[0] not in self.fringe and self.child3[0] not in self.visited:
                                    self.fringe.append((self.child3[len(self.child3) - 1]))
                            else:
                                if self.tracking_array[a][b-1]!=1 and ((a and b-1) in range(0,self.dim)):
                                    self.child1.append((current[0], current[1] - 1))
                                if self.tracking_array[a-1][b]!=1 and ((a-1 and b) in range(0,self.dim)):    
                                    self.child2.append((current[0] - 1, current[1]))
                                if self.tracking_array[a+1][b]!=1 and ((a+1 and b) in range(0,self.dim)):
                                    self.child4.append((current[0] + 1, current[1]))
                            if len(self.child4)>0 and self.child4[0] not in self.fringe and self.child4[0] not in self.visited:
                                self.fringe.append((self.child4[len(self.child4) - 1]))
                    if len(self.child1)>0 and self.child1[0] not in self.fringe and self.child1[0] not in self.visited:
                        self.fringe.append((self.child1[len(self.child1)-1]))

                    if len(self.child2)>0 and self.child2[0] not in self.fringe and self.child2[0] not in self.visited:
                        self.fringe.append((self.child2[len(self.child2)-1]))

                    self.visited.append(current)
        return False

def run_tests():
    Run_Tests = Maze()
    tests = [(100, 0.1), (100, 0.2), (100, 0.3), (100, 0.4), (100, 0.5)]

    while len(tests) != 0:
        q=0
        print("ITERATION")
        curr_test = tests.pop(0)
        maze = Run_Tests.build_maze(curr_test[0], curr_test[1])
        dimensions=curr_test[0]
        probability=curr_test[1]
        start_x=int(random.uniform(0,dimensions-1))
        start_y=int(random.uniform(0,dimensions-1))
        end_x=int(random.uniform(0,dimensions-1))
        end_y=int(random.uniform(0,dimensions-1))
        name=Run_Tests.dfs((start_x,start_y),(end_x,end_y))
        f = open("Density_vs_Success.txt", "a")
        if(name==True):
            q=1
        elif (name==False):
            q=0
        print(q)
        f.write(str(curr_test[1]) + " " + str(q) + '\n')

    plot = pd.read_csv('Density_vs_Success.txt', sep='\s+', header=None)
    plot = pd.DataFrame(plot)
    x = plot[0]
    y1 = plot[1]
    #print("Values",x,y1)
    plt.plot(x, y1, label='Density and Percentage Of Success')
    plt.xlabel('Density')
    plt.ylabel('Percentage')
    plt.title('Obstacle Desnity vs Probability Of Success')
    plt.legend()
    plt.savefig('plot.png')
    plt.show()
    exit(0)

def largest_dfs():
    Run_Tests = Maze()

    Running = True
    start_time = 0
    end_time = 0
    while Running:
        start_time = time.time()
        maze = Run_Tests.build_maze(2000, 0.3)
        bfs = Run_Tests.dfs((0,0), (9,9))
        if bfs != [] or bfs == []:
            end_time = time.time()
            Running = False
            break
    
    elapsed_time = end_time-start_time

    if elapsed_time <= 60.0:
        return elapsed_time
    
    return elapsed_time

if __name__ == "__main__":
    print(largest_dfs())

