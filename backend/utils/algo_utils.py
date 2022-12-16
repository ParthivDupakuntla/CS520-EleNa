import osmnx as ox
import networkx as nx
from heapq import *
import numpy as np

#Helper Functions : getCost, getElevation, getRoute, pathRebuild
def getCost(G, n1, n2, mode = "vanilla"):
    """ defines the cost between two nodes """
    
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
    
    
    
def getElevation(G, route, mode, pairFlag = False):
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
            diff = getCost(G, route[i],route[i+1],"gain")
        elif mode == "vanilla":
            diff = getCost(G, route[i],route[i+1],"vanilla")
        else:
            diff = getCost(G, route[i],route[i+1],"drop")
        total += diff
        if pairFlag : pairElevList.append(diff)
    if pairFlag:
        return total, pairElevList
    else:
        return total

def getRoute(parentDict, dest):
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


def pathRebuild(G, fromDict, current):
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
    bestPath = [total_path[:], getElevation(G, total_path, "vanilla"), 
                getElevation(G, total_path, "gain"), getElevation(G, total_path, "drop")]
    return bestPath

def reInit(G): #For testing
    G = G