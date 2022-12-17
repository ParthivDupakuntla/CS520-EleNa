import osmnx as ox
import networkx as nx
from heapq import *
import collections
import numpy as np
from backend.utils.algo_utils import getCost, getElevation, getRoute, pathRebuild

# DIJKSTRA's ALGORITHM
def dijkstra_helper(G, pl, shortestDist, mode, startNode, endNode):
    """ Similar functionality like A* function but implements Dijkstra's
    Returns :
        currPriority -> priority of destination node in the heap
        currDist -> Distance calculated from start to end node yet
        parentDict -> Dictionary that maps a node to it's previous child
    """
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
                print("helloooooo ", currDist)
                return currPriority, currDist, parentDict

            for nei in G.neighbors(node):
                if nei in visited: continue
                prev = minDict.get(nei, None)
                length = getCost(G, node, nei, "vanilla")
                if mode == "maximize":
                    next = length - getCost(G, node, nei, "gain")
                else:
                    next = length - getCost(G, node, nei, "drop")
                
                next += currPriority
                nextDist = currDist + length
                if nextDist <= shortestDist*(1.0+pl) and (prev is None or next < prev):
                    parentDict[nei] = node
                    minDict[nei] = next
                    heappush(q, (next, nextDist, nei))        
    
    return None, None, None

def Dijkstra(G, startNode, endNode, mode, bestPath, pl, shortestDist):
    """ Returns the best path to self.bestPath after running Dijkstra's"""
    if startNode is None or endNode is None:
        return
    temp, currDist, parentDict = dijkstra_helper(G, pl, shortestDist, mode, startNode, endNode)
    route = getRoute(parentDict, endNode)
    elevDist, dropDist = getElevation(G, route, "gain"), getElevation(G, route, "drop")            
    if mode == "maximize":
        if (elevDist > bestPath[2]) or (elevDist == bestPath[2] and currDist < bestPath[1]):
            bestPath = [route[:], currDist, elevDist, dropDist]
    else:
        if (elevDist < bestPath[2]) or (elevDist == bestPath[2] and currDist < bestPath[1]):
            bestPath = [route[:], currDist,  elevDist, dropDist]
    return bestPath