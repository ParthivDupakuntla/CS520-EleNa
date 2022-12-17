from . import app
from flask import Flask, render_template, request, make_response, jsonify
import osmnx as ox
from backend.algorithms import Algorithms
from backend.graph_utils import GraphUtils

app = Flask(__name__, static_url_path = '', static_folder = "./static", template_folder = "./templates")
app.config.from_object(__name__)

app.config.from_envvar('APP_CONFIG_FILE', silent=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/help")
def help():
    return render_template("help.html")

@app.route('/find_route', methods=['POST'])
def findRoute():
    graphUtils = GraphUtils()
    try:
        data = request.json
    except:
        return make_response("The request is not json", 400)

    try:
        print(data)
        source = data['source']
        destination = data['dest']
        pathlimit = float(data['percent'])
        algorithm = data['algo']
        elevationmode = data['elevationtype']
        assert(algorithm in {"astar","dijkstra"})
        assert(elevationmode in {"minimize","maximize"})
    except:
        return make_response("The request does not have all required fields", 400)

    try:
        source_coordinates = graphUtils.get_location_from_address(source)
        destination_coordinates = graphUtils.get_location_from_address(destination)
        graph = graphUtils.getGraphOject(source_coordinates, destination_coordinates)
        algorithms = Algorithms(graph, pl = pathlimit, mode = elevationmode)
        shortestPath, elevPath = algorithms.optimalPath(source_coordinates, 
                                destination_coordinates, 
                                pathlimit ,
                                algo=algorithm, 
                                mode = elevationmode)
    except:
        return make_response("Unable to run algorithms", 400)
    try:
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
        return make_response("Unable to get route", 400)