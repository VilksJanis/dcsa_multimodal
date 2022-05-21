
let map;

updatePosition = async (new_data, channel) => {
  const location = window.location.hostname;
  const settings = {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(new_data)
  };
  try {
    const fetchResponse = await fetch(`http://${location}:5000/events/${channel}`, settings);
    const data = await fetchResponse.json();
    return data;
  } catch (e) {
    return e;
  }
}

const ships = [
  { id: 9074729, name: "Test Ship", position: { lat: 52.3545561, lng: 4.9571214 } }
]



const ship_a = { id: 9074729 };
const locks = [
  { id: 101, name: "Kreekraksluizen", position: { lat: 51.689589, lng: 4.406006 }, timeout: null, priorities: [] },
  { id: 102, name: "Volkeraksluizen", position: { lat: 51.446432, lng: 4.231381 }, timeout: null, priorities: [] },
  { id: 103, name: "Prinses Beatrixluizen", position: { lat: 52.015109, lng: 5.110054 }, timeout: null, priorities: [] },
  { id: 104, name: "Muiden", position: { lat: 52.330141, lng: 5.068903 }, timeout: null, priorities: [] },
]

function initMap() {
  const pos = { lat: 52.3545561, lng: 4.9571214 };

  // MAP
  map = new google.maps.Map(document.getElementById("map"), {
    center: pos,
    zoom: 12,
    disableDefaultUI: true
  });

  // LOCKS
  locks.forEach((lock) => {
    var radius = ((Math.random() * 2) + 5) * 1000
    lock_marker = new google.maps.Marker({
      position: lock.position,
      map,
      label: {
        text: "\ueb98",
        fontFamily: "Material Icons",
        fontSize: "18px"
      },
      draggable: true,
      title: "Lock",
    });

    var lock_circle = new google.maps.Circle({
      fillColor: '#F5F5F5',
      strokeColor: '#528BE2',
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillOpacity: 0.15,
      map,
      center: lock.position,
      radius: radius,
    });
    lock_circle.bindTo('center', lock_marker, 'position');

    lock_marker.addListener('dragstart', (event) => {
      lock_circle.setOptions({ fillColor: '#FF0000', });
    });


    lock_marker.addListener('dragend', (event) => {
      lock_circle.setOptions({
        fillColor: '#F5F5F5',
        strokeColor: '#528BE2',
      });
      updatePosition({ type: "lock", id: lock.id, lat: event.latLng.lat(), lon: event.latLng.lng(), radius: radius }, 'move')
    });

    ship_position_broadcast = setInterval(() => {
      lock_circle.setOptions({ fillColor: '#00FF00' });
      updatePosition({ type: "lock", id: lock.id, lat: lock_marker.position.lat(), lon: lock_marker.position.lng() }, 'broadcast');
      setTimeout(function () {
        if (lock_marker.dragging) {
          lock_circle.setOptions({ fillColor: '#FF0000' });
        } else {
          lock_circle.setOptions({ fillColor: '#F5F5F5' });
        }
      }, 150);
    }, (Math.random() * 3000) + 5000);

    infowindow = new google.maps.InfoWindow({
      content: ""
    });

    lock.marker = lock_marker;
    lock.circle = lock_circle;
    lock.infowindow = infowindow;
    lock.map = map;

    updatePosition({ type: "lock", id: lock.id, lat: lock.position.lat, lon: lock.position.lng, radius: radius }, 'move')

  })


  // SHIPS
  ships.forEach((ship) => {
    var radius = ((Math.random() * 3) + 4) * 1000

    // MARKER
    var ship_marker = new google.maps.Marker({
      position: ship.position,
      map,
      label: {
        text: "\ue532",
        fontFamily: "Material Icons",
        color: "#314354",
        fontSize: "16px",

      },
      draggable: true,
      title: "Ship",
    });

    // CIRCLE
    var ship_circle = new google.maps.Circle({
      fillColor: '#F5F5F5',
      strokeColor: '#528BE2',
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillOpacity: 0.15,
      map,
      center: ship.position,
      radius: radius,
    });

    ship_circle.bindTo('center', ship_marker, 'position');

    // EVENT LISTENERS
    ship_marker.addListener('dragend', (event) => {
      ship_circle.setOptions({
        fillColor: '#F5F5F5',
        strokeColor: '#528BE2',
      });
      updatePosition({ type: "ship", id: ship.id, lat: event.latLng.lat(), lon: event.latLng.lng(), radius: radius }, 'move')
    });

    ship_marker.addListener('dragstart', (event) => {
      ship_circle.setOptions({ fillColor: '#0000FF', });
    });

    // POSITION BROADCAST
    ship_position_broadcast = setInterval(() => {
      ship_circle.setOptions({ fillColor: '#00FF00' });
      updatePosition({ type: "ship", id: ship.id, lat: ship_marker.position.lat(), lon: ship_marker.position.lng() }, 'broadcast');
      setTimeout(function () {
        if (ship_marker.dragging) {
          ship_circle.setOptions({ fillColor: '#0000FF', });
        } else {
          ship_circle.setOptions({ fillColor: '#F5F5F5' });
        }
      }, 150);
    }, 1500);

    updatePosition({ type: "ship", id: ship.id, lat: ship.position.lat, lon: ship.position.lng, radius: radius }, 'move')
  })










}




window.initMap = initMap;