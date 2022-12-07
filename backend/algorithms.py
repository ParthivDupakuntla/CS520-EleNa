# def Astar(source, destination, strategy, pathlimit):
#     """
#     source, destination : nodes for which we derive a path
#     strategy : min/max -> minimum elevation or maximum elevation gain in the path
#     pathlimit : the percentage of path that can be exceeded over the shortest path
#     """
    
#     return "test"


# def Dijkstras(source, destination, strategy, pathlimit):
#     return "test"

"""
Graph Object -> list of nodes
                -> Each node : latitude, longitude, distance from end node, elevation data 
"""
""" A Star"""
def __init__(self, go, strategy, pl):
    """
        go -> graph object
        strategy -> elevation gain / elevation drop
        pl -> path limit : percent stretched over the shortest path
    """
    self.go = go
    self.start = None
    self.end = None
    self.strategy = strategy
    self.pl = pl
    self.g = {}
    self.h = {}
    self.f = {}  

def astar(self): #a star basic algorithm, needs to be updated according to the graph object
    """
        params : start, end, f, g, h, go
        returns : list of nodes in the path; each node is associated with a coordinate tuple
    """
    if not self.inputVerifier():
        return
    shortestDist = 0 # need to pass shortest distance
    pathList = [] # used to recreate path finally
    openList = []
    openList.append(self.start)
    closedList = []
    self.g[self.start] = 0
    for node in G.nodes():
        self.g[node] = float("inf")
    self.f[self.start] = self.go[self.start]['heuristic'] #for start node, g  = 0, f = h, only heuristic

    #get current node
    while openList:
        currNode = openList[0]
        currIdx = 0
        for idx, node in enumerate(openList):
            if self.f[node] < self.f[currNode]:
                currNode = node
                currIdx = idx
    
    openList.pop(currIdx)
    closedList.append(currNode)

    # found destination
    if currNode == self.end:
        path = [] #list of list of latitudes and longitudes of each node
        # function to return path
        return path

    # traverse
    for n in self.go.neighbors(currNode):
        for closed_n in closedList:
            if n == closed_n:
                continue
        gTemp = self.g[currNode] + "x" # x is the placeholder for deciding what to add to g 
        if n not in openList and gTemp <= shortestDist * (1+self.pl):
            #Stretching the shortest distance
            openList.append(n)
        elif gTemp >= self.g[n] or gTemp > shortestDist * (1 + self.pl):
            continue
        pathList[n] = currNode
        self.g[n] = gTemp
        # final f score
        self.f[n] = self.g[n] + self.go[n]['heuristic'] # f = g + h



def inputVerifier(self): # verify if we have the source and destination properly
    start = self.start
    end = self.end
    if start == None or end == None:
        return False

def pathGeneration(self):
    return 'generatedpath' #to do

#def dijkstra(self):




