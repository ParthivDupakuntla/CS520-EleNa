var map;
var markers;

function initAutocomplete() {
  service = new google.maps.DirectionsService;
  renderer = new google.maps.DirectionsRenderer({
    polylineOptions: {
      strokeColor: "red"
    }
  });

  var bounds = new google.maps.LatLngBounds();

  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 42.3832, lng: -72.5299 },
    zoom: 12,
    mapTypeId: "roadmap",
  });

  renderer.setMap(map);

  var source = document.getElementById("source");
  var dest = document.getElementById("dest");
  markers = new Map();
  addMarker(source, map, markers, bounds, 'source');
  addMarker(dest, map, markers, bounds, 'dest');
}

function addMarker(point, map, markers, bounds, key_val) {

    var auto = new google.maps.places.Autocomplete(point);
    auto.bindTo('bounds', map);

    google.maps.event.addListener(auto, 'place_changed', function () {
      var place = auto.getPlace();

      const icon = {
        url: place.icon,
        size: new google.maps.Size(73, 73),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(24, 24),
      };

      var marker = new google.maps.Marker({
        map,
        icon,
        title: place.name,
        position: place.geometry.location,
      });

      var info = new google.maps.InfoWindow();
      google.maps.event.addListener(marker, 'click', (function(marker) {
        return function() {
            info.setContent(place.name);
            info.open(map, marker);
        }
      })(marker));

      if(markers.has(key_val)) {
        markers.get(key_val).setMap(null);
        markers.delete(key_val);
      }
      markers.set(key_val, marker);
      bounds.extend(marker.position);
      map.fitBounds(bounds);

      var zoom = map.getZoom();
      map.setZoom(zoom > 12 ? 12 : zoom);
    });
}

function removeMarker() {
  initAutocomplete();

}

function removePath() {
  renderer.setDirections({routes: []});
  renderer.setMap(null);
  renderer.setPanel(null);
  service = new google.maps.DirectionsService;
  renderer = new google.maps.DirectionsRenderer({
    polylineOptions: {
      strokeColor: "red"
    }
  });
  renderer.setMap(map);
}

function reset() {
    document.getElementById("userForm").reset();
    resetStatistics();
    removeMarker();
    removePath();

}

function showPathOnMap(source, dest, path, distance, elevation) {
  path_points = []
  for (let i = 3; i < path.length-3; i++){
    var lat = path[i][0];
    var long= path[i][1];
    path_points.push({
      location: new google.maps.LatLng(lat,long),
      stopover: false,
    });
  }

  service.route({
    origin: new google.maps.LatLng(source[0], source[1]),
    destination: new google.maps.LatLng(dest[0], dest[1]),
    waypoints: path_points,
    travelMode: 'WALKING'
  }, function(response, status) {
    if (status === 'OK') {
      renderer.setDirections(response);
      setStatistics(distance, elevation);
    } else {
      window.alert('Request failed with error ' + status);
    }
  });

}


function submit(){
    var best_path;
    var validation = formValidation();

    if(validation == true) {
        initAutocomplete();
          $.ajax({
            type: "POST",
            url: "/test",
            data: JSON.stringify({
              source: document.getElementById("source").value,
              dest: document.getElementById("dest").value,
              algo: document.getElementById("algo").value,
              percent: document.getElementById("percent").value,
              elevationtype: document.getElementById("elevation").value
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(result) {
              best_path = result['elevation_route']['geometry']['coordinates']
              distance = result['shortDist']
              gainShort = result['gainShort']
              elevation = result['elenavDist']

              console.log(typeof best_path)

              var len = best_path.length-1

              var source = best_path[0]
              var dest = best_path[len]

              var ptA = new google.maps.LatLng(source['0'], source['1']);
              var ptB = new google.maps.LatLng(dest['0'], dest['1']);

              const path_points = [];

              for (let i = len; i >=0 ; i--) {
                  var lat = best_path[i]['0']
                  var long = best_path[i]['1']
                  path_points.push({
                    location: new google.maps.LatLng(lat, long),
                    stopover: false,
                  });
              }

              initMap(ptA, ptB, path_points)
              showPathOnMap(source, dest, best_path, distance, elevation);

            },
            error: function(result) {
                alert('Bad Request !!!');
            }
        });
    }
}

function initMap(ptA, ptB, path_points) {
    var myOptions = {
        zoom: 7,
        center: ptA
    },
    // Instantiate a directions service.
    service = new google.maps.DirectionsService,
    renderer = new google.maps.DirectionsRenderer({
        map: map
    });

    // get route from A to B
    displayRoute(service, renderer, ptA, ptB, path_points);
}

function displayRoute(service, renderer, ptA, ptB, path_points) {
  service.route({
      origin: ptA,
      destination: ptB,
      waypoints: path_points,
      travelMode: google.maps.TravelMode.WALKING
  }, function (response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
          renderer.setDirections(response);
      } else {
          window.alert('Directions request failed due to ' + status);
      }
  });
}

function formValidation(){
  var source = document.getElementById("source").value;
  var dest = document.getElementById("dest").value;
  var algo = document.getElementById("algo").value;
  var elevation_type = document.getElementById("elevation").value;

  if(source == "") {
    window.alert("Source Location is required.");
    return false;
  }

  if(dest == "") {
    window.alert("Destination Location is required.");
    return false;
  }

  if(algo == "Select Algorithm") {
    window.alert("Algorithm is required.");
    return false;
  }

  if(elevation_type == "Select Elevation") {
      window.alert("Elevation is required.");
      return false;
  }

  return true;
}

function setStatistics(distance, elevation) {
  var routeStats = "<h1> Route Statistics </h1> <br> Total Distance: " + distance.toFixed(4) + " m<br><br>Elevation Gain: " + elevation.toFixed(4) +" m";
  document.getElementById("statistics").innerHTML = routeStats;
  document.getElementById("statistics").style["display"]='block';
  document.getElementById("map-row").classList.remove("col-lg-12");
  document.getElementById("map-row").classList.add("col-lg-9");
}

function resetStatistics() {
  document.getElementById("statistics").innerHTML = "";
  document.getElementById("statistics").style["display"]='none'
  document.getElementById("map-row").classList.remove("col-lg-9");
  document.getElementById("map-row").classList.add("col-lg-12");
}