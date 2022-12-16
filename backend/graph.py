import osmnx as ox
import networkx as nx
import numpy as np
import pickle as p
import os


def distance_between_locs(lat1,lon1,lat2,lon2):
    R=6371008.8 #radius of the earth
    
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = R * c
    return distance


class Model:
    def __init__(self):
        print("Model Initialized")        
        self.GOOGLEAPIKEY="AIzaSyB_uAGX5M9hc8MdLnocMFJML4yaxAg9HsU"
        if os.path.exists("./graph.p"):
            self.G = p.load( open( "graph.p", "rb" ) )
            self.init = True
            print("Loaded Graph")
        else:
            self.init = False

    def addDistFromDest(self,G,end_location):
        print(end_location)
        nn = ox.distance.nearest_nodes(G, end_location[1], end_location[0], return_dist=False)
        end_node=G.nodes[nn]
        print(end_node)
        
        lat1=end_node['y']
        lon1=end_node['x']
        for node,data in G.nodes(data=True):

            lat2=G.nodes[node]['y']
            lon2=G.nodes[node]['x']
            
            distance = distance_between_locs(lat1,lon1,lat2,lon2)
            #print("-----------------", node,data,lat1,lon1,lat2,lon2,distance)        
            data['distFromDest'] = distance
        return G

    def get_graph(self, start_location, end_location):
        print("Coordinates inside get_graph :: ", start_location, end_location)
        if not self.init:
            print("Downloading Graph")
            self.G = ox.graph_from_point(start_location, dist=30000, dist_type="network", network_type='walk')
            print("get_graph self G :: ", self.G)
            self.G = ox.elevation.add_node_elevations_google(self.G, api_key=self.GOOGLEAPIKEY)
            print("hellop", start_location, self.G)
            p.dump(self.G, open("graph.p", "wb" ) )
            self.init = True
            print("Saved Graph")
        self.G = self.addDistFromDest(self. G,end_location)
        return self.G