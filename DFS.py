fringe = []
visited = []
child1=[]
child2=[]
child3=[]
child4=[]
dim=int(input("Enter a dimension"))
start=input("Enter a start node in the form of x,y")
goal=input("Enter a final node in the form of x,y")
def dfs(start, goal):
    first=start.split(",")
    second=goal.split(",")
    target=(int(second[0]),int(second[1]))
    fringe.append((int(first[0]),int(first[1])))
    while len(fringe) > 0:
        if len(child1) and len(child2) !=0:
            child1.pop()
            child2.pop()
            if len(child3)!=0:
                child3.pop()
            if len(child4)!=0:
                child4.pop()
        current = fringe.pop()
        if current == target:
            return True
        else:
            if current not in visited:
                if current[1] == 0:
                    child1.append((current[0], current[1]+1))
                    if current[0] != dim-1:
                        child2.append((current[0]+1, current[1]))
                    else:
                        child2.append((current[0]-1, current[1]))
                else:
                    if (current[0] == 0 and current[1] != 0) or (current[0]==dim-1 and current[1]!=0):
                        child1.append((current[0], current[1]-1))
                        if current[0] == 0:
                            child2.append((current[0]+1, current[1]))
                        elif current[0] == dim-1:
                            child2.append((current[0]-1, current[1]))
                        if current[1] != dim-1:
                            child3.append((current[0], current[1]+1))
                            if child3[0] not in fringe and child3[0] not in visited:
                                fringe.append((child3[len(child3)-1]))
                    else:
                        if current[1]!=dim-1:
                            child1.append((current[0],current[1]-1))
                            child2.append((current[0]-1,current[1]))
                            child3.append((current[0],current[1]+1))
                            child4.append((current[0]+1,current[1]))
                            if child3[0] not in fringe and child3[0] not in visited:
                                fringe.append((child3[len(child3) - 1]))
                        else:
                            child1.append((current[0], current[1] - 1))
                            child2.append((current[0] - 1, current[1]))
                            child4.append((current[0] + 1, current[1]))
                        if child4[0] not in fringe and child4[0] not in visited:
                            fringe.append((child4[len(child4) - 1]))
                if child1[0] not in fringe and child1[0] not in visited:
                    fringe.append((child1[len(child1)-1]))

                if child2[0] not in fringe and child2[0] not in visited:
                    fringe.append((child2[len(child2)-1]))

                visited.append(current)



    return False
print(dfs(start,goal))
