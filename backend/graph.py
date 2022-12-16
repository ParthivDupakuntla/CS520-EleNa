import osmnx as ox
import networkx as nx
import numpy as np
import pickle as p
import os


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

    
    def calculate_spherical_distance(self, lat1, lon1, lat2, lon2, r=6371008.8):
        # Convert degrees to radians
        coordinates = lat1, lon1, lat2, lon2
        # radians(c) is same as c*pi/180
        phi1, lambda1, phi2, lambda2 = [
            np.radians(c) for c in coordinates
        ]
        # Apply the haversine formula
        a = (np.square(np.sin((phi2-phi1)/2)) + np.cos(phi1) * np.cos(phi2) * 
            np.square(np.sin((lambda2-lambda1)/2)))
        d = 2*r*np.arcsin(np.sqrt(a))
        return d

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
            #print("-----------------", node,data,lat1,lon1,lat2,lon2,distance)        
            data['distFromDest'] = self.calculate_spherical_distance(lat1,lon1,lat2,lon2)
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