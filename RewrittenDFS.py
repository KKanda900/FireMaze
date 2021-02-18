class Maze:
    x, y = 0, 0
    cell_size = 3
    dim = 10
    display = None
    tracking_array=[]
    fringe = []
    visited = []
    probability=0

    def dfs(self, beginning, goal):
        if self.tracking_array[int(beginning[0])][int(beginning[1])]==1 or self.tracking_array[goal[0]][goal[1]]==1:
            return False
        self.fringe.append((int(beginning[0]) ,int(beginning[1])))
        while len(self.fringe) > 0:
            current = self.fringe.pop()
            if current == (goal[0],goal[1]):
                return True
            else:
                if current not in self.visited:
                    if current==(0,0) or current==(0,self.dim-1) or current==(self.dim-1,0) or current==(self.dim-1,self.dim-1):
                        if current[1]==0:
                            if self.tracking_array[current[0]][current[1]+1]==0 and (current[0],current[1]+1) not in self.fringe and (current[0],current[1]+1) not in self.visited:
                                self.fringe.append((current[0], current[1]+1))
                            if current[0]!=self.dim-1 and self.tracking_array[current[0]+1][current[1]]==0 and (current[0]+1,current[1]) not in self.fringe and (current[0]+1,current[1]) not in self.visited:
                                self.fringe.append((current[0]+1, current[1]))
                            elif current[0]==self.dim-1 and self.tracking_array[current[0]-1][current[1]]==0 and (current[0]-1,current[1]) not in self.fringe and (current[0]-1,current[1]) not in self.visited:
                                self.fringe.append((current[0]-1, current[1]))
                        else:
                            if self.tracking_array[current[0]][current[1]-1]==0 and (current[0],current[1]-1) not in self.fringe and (current[0],current[1]-1) not in self.visited:    
                                self.fringe.append((current[0], current[1]-1))
                            if current[0]!=self.dim-1 and self.tracking_array[current[0]+1][current[1]]==0 and (current[0]+1,current[1]) not in self.fringe and (current[0]+1,current[1]) not in self.visited:
                                self.fringe.append((current[0]+1, current[1]))  
                            elif current[0]==self.dim-1 and self.tracking_array[current[0]-1][current[1]]==0 and (current[0]-1,current[1]) not in self.fringe and (current[0]-1,current[1]) not in self.visited:
                                self.fringe.append((current[0]-1, current[1])) 
                    else:
                        if current[0]==0:
                            if self.tracking_array[current[0]][current[1]+1]==0 and (current[0],current[1]+1) not in self.fringe and (current[0],current[1]+1) not in self.visited:
                                self.fringe.append((current[0], current[1]+1))
                            if self.tracking_array[current[0]][current[1]-1]==0 and (current[0],current[1]-1) not in self.fringe and (current[0],current[1]-1) not in self.visited:    
                                self.fringe.append((current[0], current[1]-1))
                            if self.tracking_array[current[0]+1][current[1]]==0 and (current[0]+1,current[1]) not in self.fringe and (current[0]+1,current[1]) not in self.visited:    
                                self.fringe.append((current[0]+1, current[1]))
                        elif current[0]==self.dim-1:
                            if self.tracking_array[current[0]][current[1]+1]==0 and (current[0],current[1]+1) not in self.fringe and (current[0],current[1]+1) not in self.visited:
                                self.fringe.append((current[0], current[1]+1))
                            if self.tracking_array[current[0]][current[1]-1]==0 and (current[0],current[1]-1) not in self.fringe and (current[0],current[1]-1) not in self.visited:    
                                self.fringe.append((current[0], current[1]-1))
                            if self.tracking_array[current[0]-1][current[1]]==0 and (current[0]-1,current[1]) not in self.fringe and (current[0]-1,current[1]) not in self.visited:    
                                self.fringe.append((current[0]-1, current[1]))
                        else:
                            if current[1]+1<self.dim and self.tracking_array[current[0]][current[1]+1]==0 and (current[0],current[1]+1) not in self.fringe and (current[0],current[1]+1) not in self.visited:
                                self.fringe.append((current[0], current[1]+1))
                            if current[1]-1>=0 and self.tracking_array[current[0]][current[1]-1]==0 and (current[0],current[1]-1) not in self.fringe and (current[0],current[1]-1) not in self.visited:    
                                self.fringe.append((current[0], current[1]-1))
                            if self.tracking_array[current[0]+1][current[1]]==0 and (current[0]+1,current[1]) not in self.fringe and (current[0]+1,current[1]) not in self.visited:    
                                self.fringe.append((current[0]+1, current[1]))
                            if self.tracking_array[current[0]-1][current[1]]==0 and (current[0]-1,current[1]) not in self.fringe and (current[0]-1,current[1]) not in self.visited:    
                                self.fringe.append((current[0]-1, current[1]))
                    self.visited.append(current)
                    
        return False        

def largest_dfs():
    Run_Tests = Maze()
    Running = True
    start_time = 0
    end_time = 0
    while Running:
        start_time = time.time()
        maze = Run_Tests.build_maze(300, 0.3)
        one=(int(random.uniform(0,300)),int(random.uniform(0,300)))
        two=(int(random.uniform(0,300)),int(random.uniform(0,300)))
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
