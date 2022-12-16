import osmnx as ox
import networkx as nx
from heapq import *
import collections
import numpy as np
from backend.utils.algo_utils import getCost, getElevation, getRoute, pathRebuild

#A STAR ALGORITHM
def Astar(G, shortestDist, startNode, endNode, mode, pl):
    """ Returns a list of nodes that minimize/maximize change in elevation between start and destination using the A* Algorithm [ F(x) = G(x) + H(x)]
    Heuristic used -> distance from end node (H(x))
    Parameters : 
        startNode, endNode -> source and destination node IDs
        G -> graph object
        mode -> mode of elevation
    Returns :
        List of latitude and longitude pairs of all the nodes in that route
    """
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
            bestPath = pathRebuild(G, fromDict, current)
            return bestPath
        openList.remove(current)
        closedList.append(current)
        for nei in G.neighbors(current):
            if nei in closedList:
                continue 
            tempgScore = gScore[current] + getCost(G, current, nei, "gain")
            tempgScorePl = gScorePl[current] + getCost(G, current, nei, "vanilla")        
            if nei not in openList and tempgScorePl <= (1 + pl) * shortestDist:
                openList.append(nei)
            else:
                if tempgScore >= gScore[nei] or tempgScorePl >= ( 1 + pl) * shortestDist:
                    #Stop searching along this path if distance exceed 2 times shortest path
                    continue                 
            fromDict[nei] = current
            gScore[nei] = tempgScore
            gScorePl[nei] = tempgScorePl
            fScore[nei] = gScore[nei] + G.nodes[nei]['distFromDest']
    return None

