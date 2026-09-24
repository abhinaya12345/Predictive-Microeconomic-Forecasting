import { createStars, showToast } from "./utils.js";
import { safeJSONParse } from "./utils.js";

(() => {
  createStars("stars", 150);

  // Example: location dashboard can read same saved business location
  const saved = safeJSONParse(localStorage.getItem("businessSetupData"), null);
  if (saved?.lat && saved?.lng) {
    // you can initialize a Leaflet map or charts here
    // This is a placeholder to show integration:
    console.log("Loaded business location:", saved.lat, saved.lng, saved.address);
  }
})();
