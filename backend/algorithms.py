import osmnx as ox
import networkx as nx
from heapq import *
import collections
import numpy as np
from backend.utils.algo_utils import getCost, getElevation, getRoute, pathRebuild
from backend.utils.dijkstra import Dijkstra
from backend.utils.astar import Astar

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

#FINAL SHORTEST PATH 
    def optimalPath(self, start_location, end_location, pl, algo, mode):
        """ Returns the final shortest path route optimally developed using either astar or dijkstra and its corresponding statistics"""
        defaultSetting = ["astar", "minimize"] # since we are giving these as the default options in the UI
        algo, mode = defaultSetting[0], defaultSetting[1]
        G = self.G
        self.pl = pl/100.0
        self.mode = mode
        self.startNode, self.endNode = None, None
        if mode == "maximize" : 
            self.bestPath = [[], 0.0, float('-inf'), float('-inf')]
        else : 
            self.bestPath = [[], 0.0, float('inf'), float('-inf')]
        self.startNode, d1 = ox.distance.nearest_nodes(G, start_location[1], start_location[0], return_dist=True)
        self.endNode, d2 = ox.distance.nearest_nodes(G, end_location[1], end_location[0], return_dist=True)
        if d1 > 100 or d2 > 100:
            return None, None #Nodes are far
        self.shortestRoute = ox.distance.shortest_path(G, orig=self.startNode, dest=self.endNode)
        self.shortestDist  = sum(ox.utils_graph.get_route_edge_attributes(G, self.shortestRoute, 'length'))
        if algo == "astar":
            self.bestPath = Astar(G, self.shortestDist, self.startNode, self.endNode, mode, pl)
        else:
            self.bestPath =  Dijkstra(G, self.startNode, self.endNode, mode, self.bestPath, pl, self.shortestDist)
        shortestLatLong = [[G.nodes[route_node]['y'],G.nodes[route_node]['x']] for route_node in self.shortestRoute]
        shortestPathStats = [shortestLatLong, self.shortestDist, \
                            getElevation(G, self.shortestRoute, "gain"), getElevation(G, self.shortestRoute, "drop")]
        if (self.mode == "maximize" and self.bestPath[2] == float('-inf')) or (self.mode == "minimize" and self.bestPath[3] == float('-inf')):            
            return shortestPathStats, [[], 0.0, 0, 0]
        self.bestPath[0] = [[G.nodes[route_node]['y'],G.nodes[route_node]['x']] for route_node in self.bestPath[0]]
        return shortestPathStats, self.bestPath