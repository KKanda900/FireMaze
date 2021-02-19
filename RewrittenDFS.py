import sys, random, numpy, math, time, threading
from collections import deque
import pandas as pd
import matplotlib.pyplot as plt


class Maze:
    x, y = 0, 0
    cell_size = 3
    dim = 10
    display = None
    tracking_array=[]
    fringe = []
    visited = []
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

    def dfs(self, beginning, goal):

        #checks whether either the goal or beginning points are blocked, if so return false
        if self.tracking_array[int(beginning[0])][int(beginning[1])]==1 or self.tracking_array[goal[0]][goal[1]]==1:
            return False 

        #If they are the same point then return true 
        if beginning==goal:
            self.fringe.clear
            self.visited.clear
            return True

        #If not false, then add the beginning point to the fringe
        self.fringe.append((int(beginning[0]) ,int(beginning[1])))

        #loops through the fringe
        while len(self.fringe) > 0:

            #sets current to the topmost element of the fringe
            current = self.fringe.pop()

            #Terminating case in which current is equal to the goal
            if current == (goal[0],goal[1]):
                return True

            #Current not equal to goal
            else:
                #current has not been explored yet (haven't added surrounding valid children to the fringe)
                if current not in self.visited:
                    #All columns other than the first column
                    if current[1]>0:

                        #Checks validity of left child
                        if self.tracking_array[current[0]][current[1]-1]==0 and (current[0],current[1]-1) not in self.fringe and (current[0],current[1]-1) not in self.visited:
                            self.fringe.append((current[0],current[1]-1)) #left child is valid

                        #Checks whether the row is not the last row and also validity of bottom child
                        if current[0]!=self.dim-1 and self.tracking_array[current[0]+1][current[1]]==0 and (current[0]+1,current[1]) not in self.fringe and (current[0]+1,current[1]) not in self.visited:
                            self.fringe.append((current[0]+1,current[1])) #bottom child is valid

                        #Checks whether the column is not the last column and validity of right child
                        if current[1]!=self.dim-1 and self.tracking_array[current[0]][current[1]+1]==0 and (current[0],current[1]+1) not in self.fringe and (current[0],current[1]+1) not in self.visited:
                            self.fringe.append((current[0],current[1]+1)) #right child is valid

                        #Checks whether the row is not the first row and validity of top child
                        if current[0]!=0 and self.tracking_array[current[0]-1][current[1]]==0 and (current[0]-1,current[1]) not in self.fringe and (current[0]-1,current[1]) not in self.visited:
                            self.fringe.append((current[0]-1,current[1])) #top child is valid

                    #The first column
                    else:
                        #Checks whether the row is not the last row and also validity of bottom child
                        if current[0]!=self.dim-1 and self.tracking_array[current[0]+1][current[1]]==0 and (current[0]+1,current[1]) not in self.fringe and (current[0]+1,current[1]) not in self.visited:
                            self.fringe.append((current[0]+1,current[1])) #bottom child is valid

                        #Checks validity of right child
                        if self.tracking_array[current[0]][current[1]+1]==0 and (current[0],current[1]+1) not in self.fringe and (current[0],current[1]+1) not in self.visited:
                            self.fringe.append((current[0],current[1]+1)) #right child is valid

                        #Checks whether the row is not the first row and validity of top child
                        if current[0]!=0 and self.tracking_array[current[0]-1][current[1]]==0 and (current[0]-1,current[1]) not in self.fringe and (current[0]-1,current[1]) not in self.visited:
                            self.fringe.append((current[0]-1,current[1])) #top child is valid

                #Adds the current node to visited (all valid children have been added to the fringe) 
                self.visited.append(current) 
        self.fringe.clear
        self.visited.clear
        #In the case that the fringe is empty and you could not find a path
        return False 

def run_tests():
    Run_Tests = Maze()
    tests = [(300, 0.1), (300, 0.2), (300, 0.3), (300, 0.4), (300, 0.5)]

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
    plt.title('Obstacle Density vs Probability Of Success')
    plt.legend()
    plt.savefig('plot.png')
    plt.show()
    exit(0)






def largest_dfs():
    Run_Tests = Maze()
    Running = True
    start_time = 0
    end_time = 0
    number=int(sys.argv[1])
    one=(random.randint(0,number-1),random.randint(0,number-1))
    two=(random.randint(0,number-1),random.randint(0,number-1))
    maze = Run_Tests.build_maze(number, 0.3)
    while Running:
        start_time = time.time()
        bfs = Run_Tests.dfs(one,two)
        print(bfs)
        if bfs != [] or bfs == []:
            end_time = time.time()
            Running = False
            break
    
    elapsed_time = end_time-start_time

    if elapsed_time <= 60.0:
        print(elapsed_time)
        return elapsed_time
    print(elapsed_time)
    return elapsed_time
    


if __name__ == "__main__":
    run_tests()
