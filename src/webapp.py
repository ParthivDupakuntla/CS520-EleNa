# Entry point for the application.
# from src.View.MapView import MapView
from . import app
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import googlemaps
# from src.Controller.RouteController import RouteController
import json

gmaps = googlemaps.Client(key='AIzaSyB_uAGX5M9hc8MdLnocMFJML4yaxAg9HsU')

@app.route("/")
def home():
	return render_template("index.html")

# @app.route('/<request>', methods=['GET'])
# def index(request):
# 	if bool(request):
#
# 		request = request.replace("%2C", "," )
# 		request = request.replace("%20", " " )
# 		fromm, to, percent, maxmin, algo = request.split(":")
# 		print("User Inputs Registered:")
# 		print(fromm)
# 		print(to)
# 		print(percent)
# 		print(maxmin)
# 		print(algo)
#
# 		from_cds = [gmaps.geocode(fromm)[0]['geometry']['location']['lat'], gmaps.geocode(fromm)[0]['geometry']['location']['lng']]
# 		to_cds = [gmaps.geocode(to)[0]['geometry']['location']['lat'], gmaps.geocode(to)[0]['geometry']['location']['lng']]
#
# 		view = MapView()
# 		controller = RouteController()
# 		controller.get_final_path(from_cds, to_cds, percent, maxmin, algo, view)
# 		route_coordinates, total_distance, elevation = view.get_route_params()
# 		route_coordinates = [i[::-1] for i in route_coordinates]
# 		path = [[]]
# 		route_cds = []
# 		c = 0
# 		print("Route Statistics:")
# 		print(len(route_coordinates), route_coordinates)
#
# 		for cord in route_coordinates:
# 			if c == 23:
# 				c = 0
# 				path.append([])
# 			path[-1].append(cord)
# 			c += 1
# 		print("elevation", elevation)
# 	return jsonify(origin=from_cds, des=to_cds,path=path, dis=total_distance, elev=elevation)