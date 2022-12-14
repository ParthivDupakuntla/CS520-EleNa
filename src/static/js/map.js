var map;
function initAutocomplete() {
  directionsService = new google.maps.DirectionsService;
  directionsDisplay = new google.maps.DirectionsRenderer({
    polylineOptions: {
      strokeColor: "red"
    }
  });
  markers = new Map();
  var bounds = new google.maps.LatLngBounds();

  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 42.3732, lng: -72.5199 },
    zoom: 13,
    mapTypeId: "roadmap",
  });

  directionsDisplay.setMap(map);

  // Create the search box and link it to the UI element.
  var start = document.getElementById("start");
  var end = document.getElementById("end");

  addMarkerOnMap(start, map, markers, bounds, 'start');
  addMarkerOnMap(end, map, markers, bounds, 'end');
}

function addMarkerOnMap(input, map, markers, bounds, key) {

var autocomplete = new google.maps.places.Autocomplete(input);
autocomplete.bindTo('bounds', map);

google.maps.event.addListener(autocomplete, 'place_changed', function () {
  var place = autocomplete.getPlace();

  const icon = {
    url: place.icon,
    size: new google.maps.Size(71, 71),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(17, 34),
    scaledSize: new google.maps.Size(25, 25),
  };

  var marker = new google.maps.Marker({
      map,
      icon,
      title: place.name,
      position: place.geometry.location,
    });

  var infowindow = new google.maps.InfoWindow();
  google.maps.event.addListener(marker, 'click', (function(marker) {
    return function() {
      infowindow.setContent(place.name);
      infowindow.open(map, marker);
    }
  })(marker));

  // Create a marker for each place.
  
  if(markers.has(key)) {
      //alert(markers.get(box));
      markers.get(key).setMap(null);
      markers.delete(key);
  }  
  markers.set(key, marker);
  //alert(markers.get('a'));
  //markers.set('a', marker)
  bounds.extend(marker.position);
  map.fitBounds(bounds);  
  var zoom = map.getZoom();
  map.setZoom(zoom > 13 ? 13 : zoom);
  });
}

function removeMarker() {
  markers.get('start').setMap(null);
  markers.get('end').setMap(null);
  markers.clear();
  map.setCenter({lat:42.3732, lng:-72.5199});
  map.setZoom(13);
  directionsDisplay.setMap(map);
}

function removePathFromMap(){
  directionsDisplay.setDirections({routes: []});
  directionsDisplay.setMap(null);
  directionsDisplay.setPanel(null);
  directionsService = new google.maps.DirectionsService;
  directionsDisplay = new google.maps.DirectionsRenderer({
    polylineOptions: {
      strokeColor: "red"
    }
  });
  directionsDisplay.setMap(map);
}

function reset() {
    resetRouteStatistics()
    removeMarker();
    removePathFromMap();
    document.getElementById("dataForm").reset();
}

function showPathOnMap(start, end, path, distance, elevation){
  waypts = []
  for (let i = 3; i < path.length-3; i++){
    waypts.push({
      location: new google.maps.LatLng(path[i][0], path[i][1]),
      stopover: false,
    });
  }

  directionsService.route({
    origin: new google.maps.LatLng(start[0], start[1]),
    destination: new google.maps.LatLng(end[0], end[1]),
    waypoints: waypts,
    // optimizeWaypoints: true,
    travelMode: 'WALKING'
  }, function(response, status) {
    if (status === 'OK') {
      directionsDisplay.setDirections(response);
      setRouteStatistics(distance, elevation);
    } else {
      window.alert('Directions request failed due to ' + status);
    }
  });

}


function submit(){
  // print("inside submit")
  console.log("inside submit!!")
  // if(!formValidation()){
  //     return;
  // }

  var best_path;

  $.ajax({
    type: "POST",
    url: "/test",
    data: JSON.stringify({ 
      start: document.getElementById("start").value,
      end: document.getElementById("end").value,
      algo: document.getElementById("algo").value,
      percent: document.getElementById("percent").value,
      elevationtype: document.getElementById("elevation").value
    }),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(result) {
      best_path = result['elevation_route']['geometry']['coordinates']
      distance=result['shortDist']
      gainShort = result['gainShort']
      elevation=result['elenavDist']
      //console.log(best_path)
      console.log(typeof best_path)

      var start = best_path[best_path.length-1]
      var end = best_path[0]
      var pointA = new google.maps.LatLng(start['0'], start['1']);
      var pointB = new google.maps.LatLng(end['0'], end['1']);
      console.log(start)
      
      const waypts = [];
    
      for (let i = best_path.length-1; i >=0 ; i--) {
          waypts.push({
            location: new google.maps.LatLng(best_path[i]['0'], best_path[i]['1']),
            stopover: false,
          });
      }

      initMap(pointA, pointB, waypts)
      showPathOnMap(start, end, best_path, distance, elevation);
      
    },
    error: function(result) {
        alert('Bad Request !!!');
    }
});




  // $.get("http://127.0.0.1:5000/"+ encodeURIComponent($("#start").val()) + ":" 
  // + encodeURIComponent($("#end").val()) + ":" 
  // + encodeURIComponent($("#percent").val()) + ":" 
  // + encodeURIComponent($("#elevation").val()) + ":" 
  // + encodeURIComponent($("#algo").val())).done(function (data) {
  //   start = data.origin;
  //   end = data.des
  //   path = data.path;
  //   distance = data.dis;
  //   elevation = data.elev;
    
     
  //   for(var i =0; i < path.length; i++)
  //   {
  //     showPathOnMap(start, end, path[i], distance, elevation); 
  //   }
    
  // })
}

// https://jsfiddle.net/u9no8te4/
function initMap(pointA, pointB, waypts) {
      var myOptions = {
          zoom: 7,
          center: pointA
      },
      // map = new google.maps.Map(document.getElementById('map-canvas'), myOptions),
      // Instantiate a directions service.
      directionsService = new google.maps.DirectionsService,
      directionsDisplay = new google.maps.DirectionsRenderer({
          map: map
      });

  // get route from A to B
  calculateAndDisplayRoute(directionsService, directionsDisplay, pointA, pointB, waypts);

}



function calculateAndDisplayRoute(directionsService, directionsDisplay, pointA, pointB, waypts) {
  directionsService.route({
      origin: pointA,
      destination: pointB,
      waypoints: waypts,
      travelMode: google.maps.TravelMode.WALKING
  }, function (response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
          directionsDisplay.setDirections(response);
      } else {
          window.alert('Directions request failed due to ' + status);
      }
  });
}




function formValidation(){
  var start = document.getElementById("start").value;
  var end = document.getElementById("end").value;

  if(start==""){
    window.alert("Start Location is required.");
    return false;
  }

  if(end==""){
    window.alert("End Location is required.");
    return false;
  }
  return true;
}

function setRouteStatistics(distance, elevation) {
  var routeStats = "Total Distance: " + distance + "<br>Elevation Gain: " + elevation;
  document.getElementById("statistics").innerHTML = routeStats;
  document.getElementById("statistics").style["display"]='block';
  document.getElementById("map-row").classList.remove("col-lg-12");
  document.getElementById("map-row").classList.add("col-lg-9");
}

function resetRouteStatistics() {
  document.getElementById("statistics").innerHTML = "";
  document.getElementById("statistics").style["display"]='none'
  document.getElementById("map-row").classList.remove("col-lg-9");
    document.getElementById("map-row").classList.add("col-lg-12");
}