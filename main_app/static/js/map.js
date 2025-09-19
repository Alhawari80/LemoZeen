// static/js/map.js
// Dynamic Google Maps loader + initMap + helpers
// Usage (in template):
// <script src="{% static 'js/map.js' %}" data-google-maps-api-key="{{ google_maps_api_key }}"></script>

(function () {
  // Safety: avoid module scope pitfalls; attach needed things to window
  const SCRIPT_MARKER = 'gmaps-dynamic-loaded';
  const CALLBACK_NAME = 'initMap';

  // Utility
  function safeEl(id) { return document.getElementById(id); }
  function exists(selector) { return document.querySelector(selector) !== null; }

  // Expose a place to store map/services so other scripts can use them
  if (!window._gm) window._gm = {};

  // Main global callback used by Google to begin initialization
  window[CALLBACK_NAME] = function () {
    try {
      const mapEl = safeEl('map');
      if (!mapEl) {
        console.warn('initMap: #map element not found; aborting map initialization.');
        return;
      }

      // Default center (tweak to your country/city)
      const defaultCenter = { lat: 25.282, lng: 51.531 };

      const map = new google.maps.Map(mapEl, {
        center: defaultCenter,
        zoom: 13,
        mapTypeControl: false,
        fullscreenControl: false,
      });

      const directionsService = new google.maps.DirectionsService();
      const directionsRenderer = new google.maps.DirectionsRenderer({
        map,
        suppressMarkers: false,
      });

      // store globally for debugging or other scripts
      window._gm.map = map;
      window._gm.directionsService = directionsService;
      window._gm.directionsRenderer = directionsRenderer;

      // Wire up autocompletes if inputs exist
      const originInput = safeEl('origin-input');
      const destinationInput = safeEl('destination-input');

      let originAutocomplete = null;
      let destinationAutocomplete = null;

      if (originInput && destinationInput && google.maps.places) {
        originAutocomplete = new google.maps.places.Autocomplete(originInput, {
          fields: ['place_id','geometry','formatted_address','name'],
        });
        destinationAutocomplete = new google.maps.places.Autocomplete(destinationInput, {
          fields: ['place_id','geometry','formatted_address','name'],
        });

        // update hidden lat/lng whenever place chosen
        originAutocomplete.addListener('place_changed', () => {
          const p = originAutocomplete.getPlace();
          if (!p || !p.geometry) return;
          setHidden('origin-lat', p.geometry.location.lat());
          setHidden('origin-lng', p.geometry.location.lng());
          // optional: keep formatted address
          originInput.value = p.formatted_address || p.name || originInput.value;
        });

        destinationAutocomplete.addListener('place_changed', () => {
          const p = destinationAutocomplete.getPlace();
          if (!p || !p.geometry) return;
          setHidden('destination-lat', p.geometry.location.lat());
          setHidden('destination-lng', p.geometry.location.lng());
          destinationInput.value = p.formatted_address || p.name || destinationInput.value;
        });
      }

      // helper to set hidden fields
      function setHidden(id, value) {
        const el = safeEl(id);
        if (el) el.value = (value === undefined || value === null) ? '' : value;
      }

      // Central route calculation - returns a Promise
      function calculateRoute({ origin, destination, travelMode = 'DRIVING' } = {}) {
        return new Promise((resolve, reject) => {
          if (!origin || !destination) {
            reject(new Error('origin and destination required'));
            return;
          }

          const request = {
            origin,
            destination,
            travelMode: google.maps.TravelMode[travelMode] || google.maps.TravelMode.DRIVING,
            provideRouteAlternatives: false,
          };

          directionsService.route(request, (result, status) => {
            if (status === 'OK') {
              directionsRenderer.setDirections(result);

              const route = result.routes[0];
              const leg = route.legs[0];

              // Fill hidden inputs if present
              if (leg) {
                setHidden('origin-lat', leg.start_location.lat());
                setHidden('origin-lng', leg.start_location.lng());
                setHidden('destination-lat', leg.end_location.lat());
                setHidden('destination-lng', leg.end_location.lng());
                setHidden('distance-text', leg.distance ? leg.distance.text : '');
                setHidden('duration-text', leg.duration ? leg.duration.text : '');
                setHidden('route-polyline', route.overview_polyline ? route.overview_polyline.points : '');
              }

              resolve({ result, route });
            } else {
              reject(new Error(status || 'Directions request failed'));
            }
          });
        });
      }

      // Wire the "Get route" button
      const routeBtn = safeEl('get-route');
      if (routeBtn) {
        routeBtn.addEventListener('click', function (ev) {
          ev.preventDefault();
          const originVal = originInput ? originInput.value : null;
          const destVal = destinationInput ? destinationInput.value : null;
          if (!originVal || !destVal) {
            alert('Please fill origin and destination using the suggestions.');
            return;
          }
          // If Autocomplete produced place objects, prefer their place_id
          const originPlace = originAutocomplete ? originAutocomplete.getPlace() : null;
          const destPlace = destinationAutocomplete ? destinationAutocomplete.getPlace() : null;

          let originForReq = originVal;
          let destForReq = destVal;
          if (originPlace && originPlace.place_id) originForReq = { placeId: originPlace.place_id };
          if (destPlace && destPlace.place_id) destForReq = { placeId: destPlace.place_id };

          calculateRoute({ origin: originForReq, destination: destForReq })
            .catch(err => {
              console.error('Route error', err);
              alert('Could not calculate route: ' + (err.message || err));
            });
        });
      }

      // If the server rendered a saved trip (window._savedTrip), show it
      if (window._savedTrip && window._savedTrip.origin_lat) {
        try {
          const o = { lat: parseFloat(window._savedTrip.origin_lat), lng: parseFloat(window._savedTrip.origin_lng) };
          const d = { lat: parseFloat(window._savedTrip.destination_lat), lng: parseFloat(window._savedTrip.destination_lng) };
          // center map between the points
          map.setCenter(o);
          calculateRoute({ origin: o, destination: d }).catch(e => console.warn('Saved trip route failed', e));
        } catch (e) {
          console.warn('initMap: invalid window._savedTrip', e);
        }
      }

      // Expose helper for other scripts to call directly
      window._gm.calculateRoute = calculateRoute;

      // signal ready
      document.dispatchEvent(new CustomEvent('gmaps:ready', { detail: { map, directionsService, directionsRenderer } }));

    } catch (err) {
      console.error('initMap error', err);
    }
  }; // end initMap

  // Dynamic loader: inject Google Maps script if not present
  function loadGoogleMapsScript(apiKey, options = {}) {
    return new Promise((resolve, reject) => {
      if (!apiKey) {
        const msg = 'Google Maps API key missing. Provide it via data-google-maps-api-key on the <script> tag or window.GOOGLE_MAPS_API_KEY';
        console.error(msg);
        reject(new Error(msg));
        return;
      }

      // If google.maps already loaded, resolve immediately
      if (window.google && window.google.maps) {
        console.info('Google Maps already present.');
        resolve();
        return;
      }

      // Avoid injecting twice
      if (document.querySelector(`script[data-${SCRIPT_MARKER}]`)) {
        // Wait for global callback to fire (or poll until google.maps exists)
        const timeout = options.timeout || 10000;
        const start = Date.now();
        const checker = setInterval(() => {
          if (window.google && window.google.maps) {
            clearInterval(checker);
            resolve();
          } else if (Date.now() - start > timeout) {
            clearInterval(checker);
            reject(new Error('Timeout waiting for existing Google Maps script to initialize'));
          }
        }, 200);
        return;
      }

      // Construct URL
      const libs = options.libraries || 'places';
      const url = `https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(apiKey)}&libraries=${encodeURIComponent(libs)}&callback=${CALLBACK_NAME}`;

      const s = document.createElement('script');
      s.async = true;
      s.defer = true;
      s.type = 'text/javascript';
      s.src = url;
      // mark so that subsequent loaders know the script exists
      s.setAttribute(`data-${SCRIPT_MARKER}`, '1');

      s.onerror = function (err) {
        console.error('Failed loading Google Maps script', err);
        reject(new Error('Google Maps script failed to load'));
      };

      // append and let the callback initMap resolve everything
      s.onload = function () {
        // onload fires BEFORE callback (sometimes) or after; either way we resolve when google.maps becomes available
        const waitStart = Date.now();
        const waitFor = options.timeout || 10000;
        (function waitForMaps() {
          if (window.google && window.google.maps) {
            resolve();
          } else if (Date.now() - waitStart > waitFor) {
            reject(new Error('Google Maps loaded but google.maps not available in time'));
          } else {
            setTimeout(waitForMaps, 100);
          }
        })();
      };

      document.head.appendChild(s);
    });
  }

  // Auto-boot logic: find the <script> tag that loaded this file and read the data attribute
  (function autoBoot() {
    // Many browsers support document.currentScript; fallbacks included
    let loaderScript = document.currentScript;
    if (!loaderScript) {
      // try to find script tag that references this file path (best-effort)
      const scripts = Array.from(document.getElementsByTagName('script'));
      loaderScript = scripts.find(s => (s.src || '').indexOf('static/js/map.js') !== -1 || s.hasAttribute('data-google-maps-api-key'));
    }

    const keyFromAttr = loaderScript ? (loaderScript.dataset && (loaderScript.dataset.googleMapsApiKey || loaderScript.dataset.googleMapsApiKey)) : null;
    const key = keyFromAttr || window.GOOGLE_MAPS_API_KEY || null;

    if (key) {
      // kick off loading but don't block. apps can also call window.loadGoogleMaps manually.
      loadGoogleMapsScript(key).catch(err => {
        console.error('loadGoogleMapsScript failed', err);
      });
    } else {
      // no key auto-provided. we leave a loader function for manual invocation.
      console.warn('No Google Maps API key detected in data-google-maps-api-key or window.GOOGLE_MAPS_API_KEY. Call window.loadGoogleMaps(YOUR_KEY) to load map.');
    }
  })();

  // Provide a manual entrypoint
  window.loadGoogleMaps = function (apiKey, options) {
    return loadGoogleMapsScript(apiKey, options);
  };

})();
