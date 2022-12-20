import osmnx as ox
import numpy as np
import pickle as p
import os
import googlemaps


class GraphUtils:
    def __init__(self):
        self.GOOGLEAPIKEY=""
        self.gmaps = googlemaps.Client(key=self.GOOGLEAPIKEY)

    def get_location_from_address(self, address):
        return (self.gmaps.geocode(address)[0]['geometry']['location']['lat'], 
                                self.gmaps.geocode(address)[0]['geometry']['location']['lng'])
    
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

    def getGraphOject(self, start_location, end_location):
        if os.path.exists("./graph.p"):
            self.G = p.load( open( "graph.p", "rb" ) )
            print("Found Existing Graph")
        else:
            print("Did not find existing Graph. Downloading !!!!")
            self.G = ox.graph_from_point(start_location, dist=30000, dist_type="network", network_type='walk')
            self.G = ox.elevation.add_node_elevations_google(self.G, api_key=self.GOOGLEAPIKEY)
            p.dump(self.G, open("graph.p", "wb" ) )
            print("Saved Graph !!!!")
        
        end_node = ox.distance.nearest_nodes(self.G, end_location[1], end_location[0], return_dist=False)
        end_location = self.G.nodes[end_node]        
        lat1=end_location['y']
        lon1=end_location['x']
        for node,data in self.G.nodes(data=True):
            lat2=self.G.nodes[node]['y']
            lon2=self.G.nodes[node]['x']
            data['distFromDest'] = self.calculate_spherical_distance(lat1,lon1,lat2,lon2)
        return self.G
