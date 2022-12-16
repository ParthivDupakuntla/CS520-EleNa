from . import app
from flask import Flask, render_template, request
import osmnx as ox
from backend.algorithms import Algorithms
from backend.graph_utils import GraphUtils

app = Flask(__name__, static_url_path = '', static_folder = "./static", template_folder = "./templates")
app.config.from_object(__name__)

app.config.from_envvar('APP_CONFIG_FILE', silent=True)

init = False
G, graphUtils, algorithms = None, None, None

def initializeAllModules():
    global graphUtils, init
    if init is False:
        graphUtils = GraphUtils()
        init = True


@app.route("/")
def home():
    initializeAllModules()
    return render_template("index.html")

@app.route('/test', methods=['POST'])
def test():
    global init, G, graphUtils, algorithms
    initializeAllModules()
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
        assert(algorithm in {"astar","dijkstra"})
        assert(elevationmode in {"minimize","maximize"})
    except:
        return "Bad Request"

    try:
        source_coordinates = graphUtils.get_location_from_address(source)
        destination_coordinates = graphUtils.get_location_from_address(destination)
        #print("Coordinates :: ", source_coordinates, destination_coordinates)
        
        G = graphUtils.get_graph(source_coordinates, destination_coordinates)
        algorithms = Algorithms(G, pl = pathlimit, mode = elevationmode)
        shortestPath, elevPath = algorithms.shortest_path(source_coordinates, 
                                destination_coordinates, 
                                pathlimit ,
                                algo=algorithm, 
                                mode = elevationmode, 
                                log=True)
    except:
        return "Bad Request"
    try:
        if shortestPath is None and elevPath is None:
            data = {"elevation_route" : [] , 
                    "shortest_route" : [],
                    "shortDist" : 0,
                    "gainShort" : 0,
                    "dropShort" : 0,
                    "elenavDist" : 0,
                    "gainElenav" : 0,
                    "dropElenav" :0
                    }
            return data
        data = {"elevation_route" : elevPath[0], 
                "shortest_route" : shortestPath[0],
                "shortDist" : shortestPath[1],
                "gainShort" : shortestPath[2],
                "dropShort" : shortestPath[3],
                "elenavDist" : elevPath[1],
                "gainElenav" : elevPath[2],
                "dropElenav" : elevPath[3]
                }
        return data
    except:
        return "Bad Request"