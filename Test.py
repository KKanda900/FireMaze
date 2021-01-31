import Queue

def tree_search(start, goal):
    fringe = []
    fringe.append(start)
    while fringe is not empty:
        current = Queue.pop(0)
        if current is goal:
            return True
        else:
            generate children of current
            put valid children on fringe

    return False
