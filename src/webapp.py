# Entry point for the application.
# from src.View.MapView import MapView
from . import app
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import googlemaps
import osmnx as ox
# from src.Controller.RouteController import RouteController
import json
from backend.algorithms import Algorithms
from backend.graph import Model


gmaps = googlemaps.Client(key='AIzaSyB_uAGX5M9hc8MdLnocMFJML4yaxAg9HsU')
app = Flask(__name__, static_url_path = '', static_folder = "./static", template_folder = "./templates")
app.config.from_object(__name__)

app.config.from_envvar('APP_CONFIG_FILE', silent=True)

init = False
G, M, algorithms = None, None, None

def create_geojson(coordinates):
    geojson = {}
    geojson["properties"] = {}
    geojson["type"] = "Feature"
    geojson["geometry"] = {}
    geojson["geometry"]["type"] = "LineString"
    geojson["geometry"]["coordinates"] = coordinates

    return geojson

def create_data(start_location, end_location, pl, min_max,algorithm):
    """
    Prepares the data for the routes to be plotted. 
    """
    global init, G, M, algorithms
    
    M = Model()
    G = M.get_graph(start_location, end_location)
    algorithms = Algorithms(G, pl = pl, mode = min_max)
    shortestPath, elevPath = algorithms.shortest_path(start_location, end_location, pl,algo=algorithm, mode = min_max, log=True)
    print("create_data shortestPath:: ", shortestPath)
    print("-----------------------------------------------------------------------------------------------------------------")
    print("create_data elevPath:: ", elevPath)
    
    if shortestPath is None and elevPath is None:
        data = {"elevation_route" : [] , "shortest_route" : []}        
        data["shortDist"] = 0
        data["gainShort"] = 0
        data["dropShort"] = 0
        data["elenavDist"]  = 0
        data["gainElenav"] = 0
        data["dropElenav"] = 0
        data["popup_flag"] = 0 
        return data
    data = {"elevation_route" : create_geojson(elevPath[0]), "shortest_route" : create_geojson(shortestPath[0])}
    data["shortDist"] = shortestPath[1]
    data["gainShort"] = shortestPath[2]
    data["dropShort"] = shortestPath[3]  
    data["elenavDist"] = elevPath[1]
    data["gainElenav"] = elevPath[2]
    data["dropElenav"] = elevPath[3] 
    if len(elevPath[0])==0:
        data["popup_flag"] = 1        
    else:
        data["popup_flag"] = 2    
    return data

@app.route("/")
def home():
	return render_template("index.html")

@app.route('/test', methods=['POST'])
def test():
    try:
        data = request.json
    except:
        return "Bad Request"
    try:
        source = data['source']
        destination = data['dest']
        pathlimit = float(data['percent'])
        algorithm = data['algo']
        elevationmode = data['elevationtype']
        #print(source, destination,pathlimit,algorithm,elevationmode)
        assert(algorithm in {"astar","dijkstra"})
        assert(elevationmode in {"minimize","maximize"})
        
        source_coordinates = (gmaps.geocode(source)[0]['geometry']['location']['lat'], gmaps.geocode(source)[0]['geometry']['location']['lng'])
        destination_coordinates = (gmaps.geocode(destination)[0]['geometry']['location']['lat'], gmaps.geocode(destination)[0]['geometry']['location']['lng'])
        #print("Coordinates :: ", source_coordinates, destination_coordinates)
        data = create_data(source_coordinates,destination_coordinates,pathlimit,elevationmode,algorithm)
    except:
        return "Bad Request"
    return json.dumps(data)


@app.route('/route',methods=['POST'])
def get_route():  
    """
    Prepares data required by the POST.
    Dumped as a JSON.
    """  
    data=request.get_json(force=True)
    route_data = create_data((data['start_location']['lat'],data['start_location']['lng']),(data['end_location']['lat'],data['end_location']['lng']),data['x'],data['min_max'])
    return json.dumps(route_data)
