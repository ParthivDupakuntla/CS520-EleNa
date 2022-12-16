import osmnx as ox
import networkx as nx
from heapq import *
import collections
import numpy as np

# Algorithms class consists of two algorithms - Astar and Dijkstra's and necessary helper functions to calculate the shortest route w.r.t elevation.
class Algorithms:
    def __init__(self, G, pl, mode = "maximize"):
        """
        Parameters : 
        G -> Graph Object
        mode -> chosen mode of elevation
        pl -> Path Limit
        startNode, endNode -> source, destination
        bestPath -> best path returned
        """
      
        self.G = G
        self.mode = mode
        self.pl = pl
        self.bestPath = [[], 0.0, float('-inf'), 0.0]
        self.startNode, self.endNode = None, None

#Helper Functions : getCost, getElevation, getRoute, pathRebuild
    def getCost(self, n1, n2, mode = "vanilla"):
        """ defines the cost between two nodes """
        G = self.G
        if n1 is None or n2 is None : return
        if mode == "gain":
            return max(0.0, G.nodes[n2]["elevation"] - G.nodes[n1]["elevation"])
        elif mode == "drop":
            if G.nodes[n2]["elevation"] - G.nodes[n1]["elevation"] > 0:
                return 0.0
            else:
                return G.nodes[n1]["elevation"] - G.nodes[n2]["elevation"]
        
        else:
            return abs(G.nodes[n1]["elevation"] - G.nodes[n2]["elevation"])
    
    
    def getElevation(self, route, mode, pairFlag = False):
        """ Computes the cost of a route which is the elevation of the route.
        Parameters:
            route -> List of Node IDs
            mode -> mode of elevation 
            pairFlag -> boolean to indicate if individual cost between the nodes needs to be returned
        Returns:
            total -> total cost of the route
            pairElevList -> list of individual costs of the route [Optional]
        """
        total = 0
        if pairFlag : pairElevList = []
        for i in range(len(route)-1):
            if mode == "gain":
                diff = self.getCost(route[i],route[i+1],"gain")
            elif mode == "vanilla":
                diff = self.getCost(route[i],route[i+1],"vanilla")
            else:
                diff = self.getCost(route[i],route[i+1],"drop")
            total += diff
            if pairFlag : pairElevList.append(diff)
        if pairFlag:
            return total, pairElevList
        else:
            return total

    def getRoute(self, parentDict, dest):
        """ The final path between a parent and destination is returned
        Parameters : 
            parentDict -> given parent mapping
            dest -> final destination node
        Returns :
            res -> path from parent to dest
        """
        res = [dest]
        current = parentDict[dest]
        while current!=-1:
            res.append(current)
            current = parentDict[current]
        return res[::-1]


    def pathRebuild(self, fromDict, current):
        """ Reconstructs the path from dictionary of nodes
        Parameters : 
            fromDict -> dict containing best prvs node for the current node
            current -> current node
        """
        if not fromDict or not current : return
        total_path = [current]
        while current in fromDict:
            current = fromDict[current]
            total_path.append(current)
        self.bestPath = [total_path[:], self.getElevation(total_path, "vanilla"), self.getElevation(total_path, "gain"), self.getElevation(total_path, "drop")]
        return

#A STAR ALGORITHM
    def a_star(self):
        """ Returns a list of nodes that minimize/maximize change in elevation between start and destination using the A* Algorithm [ F(x) = G(x) + H(x)]
        Heuristic used -> distance from end node (H(x))
        Parameters : 
            startNode, endNode -> source and destination node IDs
            G -> graph object
            mode -> mode of elevation
        Returns :
            List of latitude and longitude pairs of all the nodes in that route
        """
        G, shortest = self.G, self.shortestDist
        pl, mode = self.pl, self.mode
        startNode, endNode = self.startNode, self.endNode
        if startNode is None or endNode is None:
            return
        closedList = []
        openList = []
        openList.append(startNode)
        fromDict = {} #dict containing best prvs node for the current node
        gScore = {}
        for node in G.nodes():
            gScore[node] = float("inf")
        gScore[startNode] = 0 
        gScorePl = {} # to consider path limit
        for node in G.nodes():
            gScorePl[node] = float("inf")
        gScorePl[startNode] = 0
        fScore = {} # To consider both weights and  heuristics. f(x) = g(x) + h(x)
        fScore[startNode] = G.nodes[startNode]['distFromDest'] # g(x) = 0 
        
        while len(openList):
            current = min([(node,fScore[node]) for node in openList], key=lambda t: t[1])[0]            
            if current == endNode:
                self.pathRebuild(fromDict, current)
                return
            openList.remove(current)
            closedList.append(current)
            for nei in G.neighbors(current):
                if nei in closedList:
                    continue 
                tempgScore = gScore[current] + self.getCost(current, nei, "gain")
                tempgScorePl = gScorePl[current] + self.getCost(current, nei, "vanilla")                
                if nei not in openList and tempgScorePl <= (1 + pl) * shortest:
                    openList.append(nei)
                else:
                    if tempgScore >= gScore[nei] or tempgScorePl >= ( 1 + pl) * shortest:#Stop searching along this path if distance exceed 2 times shortest path
                        continue                 
                fromDict[nei] = current
                gScore[nei] = tempgScore
                gScorePl[nei] = tempgScorePl
                fScore[nei] = gScore[nei] + G.nodes[nei]['distFromDest']

# DIJKSTRA's ALGORITHM
    def dijkstra(self):
        """ Similar functionality like A* function but implements Dijkstra's
        Returns :
            currPriority -> priority of destination node in the heap
            currDist -> Distance calculated from start to end node yet
            parentDict -> Dictionary that maps a node to it's previous child
        """
        G, pl, shortest, mode = self.G, self.pl, self.shortestDist, self.mode
        startNode, endNode = self.startNode, self.endNode
        if startNode is None or endNode is None:
            return
        q, visited, minDict = [(0.0, 0.0, startNode)], set(), {startNode: 0}
        
        parentDict = collections.defaultdict(int)
        parentDict[startNode] = -1
        while q:
            currPriority, currDist, node = heappop(q)
            
            if node not in visited:
                visited.add(node)
                if node == endNode:
                    return currPriority, currDist, parentDict

                for nei in G.neighbors(node):
                    if nei in visited: continue
                    prev = minDict.get(nei, None)
                    length = self.getCost(node, nei, "vanilla")
                    if mode == "maximize":
                        next = length - self.getCost(node, nei, "gain")
                    else:
                        next = length - self.getCost(node, nei, "drop")
                    
                    next += currPriority
                    nextDist = currDist + length
                    if nextDist <= shortest*(1.0+pl) and (prev is None or next < prev):
                        parentDict[nei] = node
                        minDict[nei] = next
                        heappush(q, (next, nextDist, nei))        
        
        return None, None, None

    def returnDijkstra(self):
        """ Returns the best path to self.bestPath after running Dijkstra's"""
        startNode, endNode = self.startNode, self.endNode
        if startNode is None or endNode is None:
            return
        temp, currDist, parentDict = self.dijkstra()
        route = self.getRoute(parentDict, endNode)
        elevDist, dropDist = self.getElevation(route, "gain"), self.getElevation(route, "drop")            
        if self.mode == "maximize":
            if (elevDist > self.bestPath[2]) or (elevDist == self.bestPath[2] and currDist < self.bestPath[1]):
                self.bestPath = [route[:], currDist, elevDist, dropDist]
        else:
            if (elevDist < self.bestPath[2]) or (elevDist == self.bestPath[2] and currDist < self.bestPath[1]):
                self.bestPath = [route[:], currDist,  elevDist, dropDist]
        return 

#FINAL SHORTEST PATH 
    def shortest_path(self, start_location, end_location, pl, algo = "dijkstra", mode = "maximize", log = True):
        """ Returns the final shortest path route and its corresponding statistics"""
        G = self.G
        self.pl = pl/100.0
        self.mode = mode
        self.startNode, self.endNode = None, None
        if mode == "maximize" : self.bestPath = [[], 0.0, float('-inf'), float('-inf')]
        else : self.bestPath = [[], 0.0, float('inf'), float('-inf')]
        self.startNode, d1 = ox.distance.nearest_nodes(G, start_location[1], start_location[0], return_dist=True)
        self.endNode, d2 = ox.distance.nearest_nodes(G, end_location[1], end_location[0], return_dist=True)
        if d1 > 100 or d2 > 100:
            if log : print("Nodes are too far away")
            return None, None
        self.shortestRoute = ox.distance.shortest_path(G, orig=self.startNode, dest=self.endNode)
        self.shortestDist  = sum(ox.utils_graph.get_route_edge_attributes(G, self.shortestRoute, 'length'))
        if algo == "astar" or mode=="minimize":
            if log : print("astar")
            self.a_star()        
        if log : print("dijkstra")
        self.returnDijkstra()
        shortestLatLong = [[G.nodes[route_node]['y'],G.nodes[route_node]['x']] for route_node in self.shortestRoute]
        shortestPathStats = [shortestLatLong, self.shortestDist, \
                            self.getElevation(self.shortestRoute, "gain"), self.getElevation(self.shortestRoute, "drop")]
        if (self.mode == "maximize" and self.bestPath[2] == float('-inf')) or (self.mode == "minimize" and self.bestPath[3] == float('-inf')):            
            return shortestPathStats, [[], 0.0, 0, 0]
        self.bestPath[0] = [[G.nodes[route_node]['y'],G.nodes[route_node]['x']] for route_node in self.bestPath[0]]
        
        print("===>end", self.bestPath[1:])
        return shortestPathStats, self.bestPath
