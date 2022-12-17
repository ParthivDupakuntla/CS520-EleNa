import pytest
from backend.algorithms import *
from backend.utils.algo_utils import *
from backend.utils.astar import *
from backend.utils.dijkstra import *
from backend.graph_utils import *
import pickle as p
import osmnx as ox
import networkx as nx


@pytest.fixture
def input_for_test():
    """Create a dummy graph with the locations for testing and custom edges and elevations"""
    G = nx.Graph()
    start = (42.350693, -72.5273722)#162
    end = (42.3576022, -72.5171551)#groff park
    for i in range(6):
        G.add_node(i, elevation = 0.0)
    edges = [(0,1,6.0), (1,2,1), (0,2,1.8), (0,3,1.7), (0,5,8), (2,5,4), (2,3,1.6), (3,4,1.9), (3,5,4), (4,5,2)]
    G.add_weighted_edges_from(edges)
    elevations = [0.0, 1.0, 0.0, 2.0, 3.0, 6.0]
    for i,e in enumerate(elevations):
        G.nodes[i]["elevation"] = e
    A = Algorithms(G, pl = 0.0)
    return start, end, G, A

def test_get_graph_multi(input_for_test):
    """test to check if there are multiple edges"""
    grph = GraphUtils()
    start, end, G1, A = input_for_test
    G = grph.getGraphOject(start, end)
    assert isinstance(G, nx.classes.multidigraph.MultiGraph)

def test_get_graph_di(input_for_test):
    """test to check for directed graph"""
    grph = GraphUtils()
    start, end, G1, A = input_for_test
    G = grph.getGraphOject(start, end)
    assert isinstance(G, nx.classes.multidigraph.DiGraph)

def test_optimalPath(input_for_test):
    """Testing Algorithmic Correctness"""
    start, end, G, A = input_for_test
    grph = GraphUtils()
    start, end, G1, A = input_for_test
    G = grph.getGraphOject(start, end)
    A = Algorithms(G, pl = 200.0)
    A.startNode, A.endNode = start, end
    spStats, bestPath = A.optimalPath(start_location=start, end_location= end, pl = 200.0, algo = "astar", mode = "maximize")
    assert bestPath[1:] == [12.321999999999996, 6.201999999999998, 6.119999999999997]


#2 TESTS TO CHECK IF CORRECT ROUTE IS DERIVED
def test_getRoute1(input_for_test):
    start, end, G, A = input_for_test
    parent = {5:3, 3:2, 2:0, 0:-1}
    dest = 5
    route = getRoute(parentDict=parent, dest=dest)
    assert route == [0,2,3,5]

def test_getRoute2(input_for_test):
    start, end, G, A = input_for_test
    parent = {5:2, 2:1, 1:0, 0:-1}
    dest = 5
    route = getRoute(parentDict=parent, dest=dest)
    assert route == [0,1,2,5]

def test_getRoute3(input_for_test):
    start, end, G, A = input_for_test
    parent = {5:4, 4:3, 3:2, 2:1, 1:0, 0:-1}
    dest = 5
    route = getRoute(parentDict=parent, dest=dest)
    assert route == [0,1,2,3,4,5]

# 2 TESTS TO CHECK CORRECT PATH RECONSTRUCTION
def test_pathRebuild1(input_for_test):
    start, end, G, A = input_for_test
    fromDict = {5:4, 4:3, 3:2, 2:1, 1:0}
    curr = 5
    bestpathRebuilt = pathRebuild(G=G, fromDict=fromDict, current=curr)
    assert bestpathRebuilt == [[5, 4, 3, 2, 1, 0], 8.0, 1.0, 7.0]

def test_pathRebuild2(input_for_test):
    start, end, G, A = input_for_test
    fromDict = {5:2, 2:1, 1:0}
    curr = 5
    bestpathRebuilt = pathRebuild(G=G, fromDict=fromDict, current=curr)
    assert bestpathRebuilt == [[5, 2, 1, 0], 8.0, 1.0, 7.0]

#3 TESTS TO CHECK IF ELEVATION IS COMPUTED CORRECTLY
def test_getElevation1(input_for_test):
    start, end, G, A = input_for_test
    route = [0,1,2,3,4,5]
    elev = getElevation(G=G, route=route, mode='vanilla', pairFlag=False)
    assert elev == 8.0

def test_getElevation2(input_for_test):
    start, end, G, A = input_for_test
    route = [0,1,2,3,4,5]
    elev = getElevation(G=G, route=route, mode='gain', pairFlag=False)
    assert elev == 7.0

def test_getElevation3(input_for_test):
    start, end, G, A = input_for_test
    route = [0,1,2,4]
    elev = getElevation(G=G, route=route, mode='gain', pairFlag=False)
    assert elev == 4.0

#4 TESTS TO COVER ALL COST SCENARIOS
def test_getCost1(input_for_test):
    start, end, G, A = input_for_test
    costRes = getCost(G=G, n1= 1, n2=3, mode="vanilla")
    print(costRes)
    assert costRes == 1.0


def test_getCost2(input_for_test):
    start, end, G, A = input_for_test
    costRes = getCost(G=G, n1= 0, n2=2, mode="vanilla")
    print(costRes)
    assert costRes == 0

def test_getCost3(input_for_test):
    start, end, G, A = input_for_test
    costRes = getCost(G=G, n1= 4, n2=3, mode="drop")
    print(costRes)
    assert costRes == 1.0


def test_getCost4(input_for_test):
    start, end, G, A = input_for_test
    costRes = getCost(G=G, n1= 5, n2=0, mode="drop")
    print(costRes)
    assert costRes == 6.0




    

