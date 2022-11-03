###EleNa - Elevation Based Navigation System
Current routing systems’ shortest path is not necessarily the shortest path with elevation gain considered.
The goal of this project is to design a navigation system that takes the elevation gain in a route into account.
We consider two features of elevation gain - maximum elevation gain and minimum elevation gain.
We introduce a design constraint that limits the resultant route to x% of the shortest path. For instance, a route from source to destination that takes 1 mile in the shortest path can be constrained to a 1.5 mile path with minimum elevation gain. A trade off might occur between the shortest path with desirable elevation v/s the actual shortest path.
