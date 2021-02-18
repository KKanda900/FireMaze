import sys, random, numpy, math, time, threading


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
        if self.tracking_array[int(beginning[0])][int(beginning[1])]==1 or self.tracking_array[goal[0]][goal[1]]==1:
            return False 
        self.fringe.append((int(beginning[0]) ,int(beginning[1])))
        while len(self.fringe) > 0:
            current = self.fringe.pop()
            #print(current)
            if current == (goal[0],goal[1]):
                return True
            else:
                if current not in self.visited:
                    if current[1]>0:
                        if self.tracking_array[current[0]][current[1]-1]==0 and (current[0],current[1]-1) not in self.fringe and (current[0],current[1]-1) not in self.visited:
                            self.fringe.append((current[0],current[1]-1))
                        if current[0]!=self.dim-1 and self.tracking_array[current[0]+1][current[1]]==0 and (current[0]+1,current[1]) not in self.fringe and (current[0]+1,current[1]) not in self.visited:
                            self.fringe.append((current[0]+1,current[1]))
                        if current[1]!=self.dim-1 and self.tracking_array[current[0]][current[1]+1]==0 and (current[0],current[1]+1) not in self.fringe and (current[0],current[1]+1) not in self.visited:
                            self.fringe.append((current[0],current[1]+1))
                        if current[0]==self.dim-1 and self.tracking_array[current[0]-1][current[1]]==0 and (current[0]-1,current[1]) not in self.fringe and (current[0]-1,current[1]) not in self.visited:
                            self.fringe.append((current[0]-1,current[1]))
                    else:
                        if current[0]!=self.dim-1 and self.tracking_array[current[0]+1][current[1]]==0 and (current[0]+1,current[1]) not in self.fringe and (current[0]+1,current[1]) not in self.visited:
                            self.fringe.append((current[0]+1,current[1]))
                        if self.tracking_array[current[0]][current[1]+1]==0 and (current[0],current[1]+1) not in self.fringe and (current[0],current[1]+1) not in self.visited:
                            self.fringe.append((current[0],current[1]+1))
                        if current[0]==self.dim-1 and self.tracking_array[current[0]-1][current[1]]==0 and (current[0]-1,current[1]) not in self.fringe and (current[0]-1,current[1]) not in self.visited:
                            self.fringe.append((current[0]-1,current[1]))
                        
                self.visited.append(current)

        return False        

def largest_dfs():
    Run_Tests = Maze()
    Running = True
    start_time = 0
    end_time = 0
    while Running:
        start_time = time.time()
        maze = Run_Tests.build_maze(20, 0.3)
        print(maze)
        """ one=(0,0)
        two=(199,199) """
        one=(int(random.uniform(0,20)),int(random.uniform(0,20)))
        two=(int(random.uniform(0,20)),int(random.uniform(0,20)))
        print(one)
        print(two)
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
    largest_dfs()
