from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
import geopy
import requests
import json
from pprint import pprint
from algorithms import Astar, Dijkstras


app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World!"


@app.route('/test', methods = ['GET'])
def test():
    geolocator = Nominatim(user_agent=__name__)
    location = geolocator.geocode("175 5th Avenue NYC")
    print(location.address)
    print((location.latitude, location.longitude))
    print(location.raw)
    return location.address


@app.route('/get_route', methods = ['POST'])
def get_route():
    try:
        data = request.json
    except:
        return "Bad Request"
    try:
        source = data['source']
        destination = data['destination']
        strategy = data['strategy']
        pathlimit = data['pathlimit']
        algorithm = data['algorithm']
        assert(algorithm in {"Astar","Dijkstras"})
    except:
        return "Bad Request"
    try :
        route = None
        
        if algorithm == "Astar":
            route = Astar(source=source, destination=destination, strategy=strategy, pathlimit=pathlimit)
        
        if algorithm == "Dijkstras":
            route = Dijkstras(source=source, destination=destination, strategy=strategy, pathlimit=pathlimit)
        
        return route
    except:
        return "Bad Request"

if __name__=="__main__":
    app.run(debug=True)
