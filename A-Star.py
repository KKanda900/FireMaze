'''
This is my version of A*, if previous version is
fixed just ignore this at the end.
'''

import math, random, numpy

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


def build_maze(size, probability):
    obstacle_num = 0  # See if the amount of obstacles required are 0 or not
    # if the maze area is 100 then there should be only 10 obstacles
    obstacles = int((size * size) * probability)
    # track where the obstacles are places so it doesn't double count
    tracking_array = numpy.zeros((size, size))
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
    print(tracking_array)
    return tracking_array

def check_valid_bounds(i, j, pop_value, arr):
    i = pop_value.position[0] + i
    j = pop_value.position[1] + j
    if i >= 0 and i < len(arr) and j >= 0 and j < len(arr):
        return True
    else:
        return False

def distance_calculator(start, end):
    x_diff = start[0] - end[0]
    y_diff = start[1] - end[1]
    return math.sqrt((x_diff**2) + (y_diff**2))

def a_star(arr):
    start = (0, 0)
    end = (len(arr)-1, len(arr)-1)
    endNode = Node((len(arr)-1, len(arr)-1))
    visited = numpy.zeros((len(arr), len(arr)), dtype=bool)

    openset = []
    closedset = []
    parent = []

    openset.append(Node(start))

    while len(openset) > 0:
        print(len(openset))
        currentNode = openset.pop(0)
        closedset.append(currentNode)

        for nodes in openset:
            if nodes.f < currentNode.f:
                currentNode = nodes
            
        if currentNode.position == end:
            print(len(openset))
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
        
        if check_valid_bounds(1, 0, currentNode, arr) and arr[currentNode.position[0]+1][currentNode.position[1]] != 1 and Node((currentNode.position[0]+1, currentNode.position[1])) not in openset:
            temp = Node((currentNode.position[0]+1, currentNode.position[1]))
            currentNode.children.append(temp)

        if check_valid_bounds(-1, 0, currentNode, arr) and arr[currentNode.position[0]-1][currentNode.position[1]] != 1 and Node((currentNode.position[0]-1, currentNode.position[1])) not in openset:
            temp = Node((currentNode.position[0]-1, currentNode.position[1]))
            currentNode.children.append(temp)

        if check_valid_bounds(0, 1, currentNode, arr) and arr[currentNode.position[0]][currentNode.position[1]+1] != 1 and Node((currentNode.position[0], currentNode.position[1]+1)) not in openset:
            temp = Node((currentNode.position[0], currentNode.position[1]+1))
            currentNode.children.append(temp)

        if check_valid_bounds(0, -1, currentNode, arr) and arr[currentNode.position[0]][currentNode.position[1]-1] != 1 and Node((currentNode.position[0], currentNode.position[1]-1)) not in openset:
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

if __name__ == "__main__":
    arr = build_maze(100, .1)
    print(a_star(arr))


            
        

