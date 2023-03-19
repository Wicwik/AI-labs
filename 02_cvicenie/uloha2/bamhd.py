import json
from collections import deque


class BaMHD(object):
    def __init__(self, db_file='ba_mhd_db.json'):
        # Initialize BaMHD object, load data from json file
        self.data = json.load(open(db_file, 'r'))

    def neighbors(self, stop):
        # Return neighbors for a given stop
        return self.data['neighbors'][stop]

    def stops(self):
        # Return list of all stops (names only)
        return self.data['neighbors'].keys()


class BusStop(object):
    # Object representing node in graph traversal. Includes name and parent node.
    def __init__(self, name, parent = None, depth = None):
        self.name = name
        self.parent = parent
        self.depth = depth

    def traceBackPath(self):
        # Returns path represented by this node as list of node names (bus stop names).
        if self.parent == None:
            return [self.name]
        else:
            path = self.parent.traceBackPath()
            path.append(self.name)
            return path

def findPathBFS(bamhd, stopA, stopB):
    # Implement Breadth-first search to find the shortest path between two MHD stops in Bratislava.
    
    ### Your code here ###
    visited = []
    queue = [BusStop(stopA)]

    current = queue.pop(0)

    while current.name != stopB:
        queue += [BusStop(neigh, current) for neigh in bamhd.neighbors(current.name) if neigh not in visited]
        visited.append(current.name)
        
        current = queue.pop(0)

    return current.traceBackPath()


def findPathDFS(bamhd, stopA, stopB):
    # Implement Depth-first search to find a path between two MHD stops in Bratislava.

    ### Your code here ###
    visited = []
    queue = [BusStop(stopA)]

    current = queue.pop()

    while current.name != stopB:
        queue += [BusStop(neigh, current) for neigh in bamhd.neighbors(current.name) if neigh not in visited]
        visited.append(current.name)
        
        current = queue.pop()

    return current.traceBackPath()


def findPathIDDFS(bamhd, stopA, stopB):
    # Implement Iterative deepening depth-first search to find the shortest path between two MHD stops in Bratislava.
    maxDepth = 100

    ### Your code here ###
    for depth in range(maxDepth):
        visited = []
        queue = [BusStop(stopA, depth=0)]
        
        current = queue.pop()

        while current.name != stopB:            
            queue += [BusStop(neigh, current, current.depth+1) for neigh in bamhd.neighbors(current.name) if (((neigh, current.depth+1) not in visited) or ((neigh, current.depth-1) not in visited)) and (current.depth < depth)]
            visited.append((current.name, current.depth))
            
            if queue == []:
                break

            current = queue.pop()

        if current.name == stopB:
            break

    return current.traceBackPath()



if __name__ == "__main__":
    # Initialization
    bamhd = BaMHD()

    # # Examples of function usage:
    # # -> accessing the list of bus stops (is 'Zoo' a bus stop?)
    # print('Zoo' in bamhd.stops())
    # # -> get neighbouring bus stops
    # print(bamhd.neighbors('Zochova'))
    # # -> get whole path from last node of search algorithm
    # s1 = BusStop('Zoo')     # some dummy data
    # s2 = BusStop('Lafranconi', s1)
    # s3 = BusStop('Park kultury', s2)
    # print(s3.traceBackPath())
    # # -> using stack
    # stack = []
    # stack.append('a'); stack.append('b'); stack.append('c')
    # print('Retrieving from stack: {}, {}, {}'.format(stack.pop(), stack.pop(), stack.pop()))
    # # -> using queue
    # queue = deque()
    # queue.append('a'); queue.append('b'); queue.append('c')
    # print('Retrieving from queue: {}, {}, {}'.format(queue.popleft(), queue.popleft(), queue.popleft()))


    # Your task: find best route between two stops with IDDFS/BFS/DFS
    # Zoo - Aupark
    print('IDDFS Zoo - Aupark:')
    path = findPathIDDFS(bamhd, 'Zoo', 'Aupark')
    print('\tpath length: {}\n\tpath: {}'.format(len(path), path))  

    print('BFS Zoo - Aupark:')
    path = findPathBFS(bamhd, 'Zoo', 'Aupark')
    print('\tpath length: {}\n\tpath: {}'.format(len(path), path))  

    print('DFS Zoo - Aupark:')
    path = findPathDFS(bamhd, 'Zoo', 'Aupark')
    print('\tpath length: {}\n\tpath: {}\n'.format(len(path), path))

    # VW - Astronomicka
    print('IDDFS VW - Astronomicka:')
    path = findPathIDDFS(bamhd, 'Volkswagen', 'Astronomicka')
    print('\tpath length: {}\n\tpath: {}'.format(len(path), path))  
  
    print('BFS VW - Astronomicka:')
    path = findPathBFS(bamhd, 'Volkswagen', 'Astronomicka')
    print('\tpath length: {}\n\tpath: {}'.format(len(path), path))  
    
    print('DFS VW - Astronomicka:')
    path = findPathDFS(bamhd, 'Volkswagen', 'Astronomicka')
    print('\tpath length: {}\n\tpath: {}'.format(len(path), path))  

