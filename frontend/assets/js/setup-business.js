import { createStars, showToast, safeJSONParse } from "./utils.js";
import { saveBusinessSetup, loadBusinessSetup } from "./api.js";

// avoid "Cannot redeclare..." by scoping everything
(() => {
  createStars("stars", 150);

  const toastId = "toast";

  // --- STATE
  const state = {
    businessType: "",
    budget: "",
    address: "",
    lat: null,
    lng: null,
    shopSize: "",
    experience: "Intermediate",
    targetCustomers: "",
    primaryGoal: "",
    revenueTarget: "",
    focusAreas: [],
    goalNotes: ""
  };

  // --- UI refs
  const addressInput = document.getElementById("addressInput");
  const coordsText = document.getElementById("coordsText");
  const confirmLocationBtn = document.getElementById("confirmLocationBtn");
  const useMyLocationBtn = document.getElementById("useMyLocationBtn");

  // address suggestion UI
  const suggestBox = document.createElement("div");
  suggestBox.className = "suggestBox";
  // you should wrap address input with .addressSuggest in HTML.
  // If not, we still try to insert it.
  if (addressInput) {
    const wrapper = addressInput.parentElement;
    wrapper?.classList.add("addressSuggest");
    wrapper?.appendChild(suggestBox);
    addressInput.removeAttribute("readonly"); // ✅ editable
  }

  // --- MAP
  const defaultCenter = [13.0827, 80.2707]; // Chennai

  const map = L.map("map", { zoomControl: true }).setView(defaultCenter, 12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap contributors"
  }).addTo(map);

  const marker = L.marker(defaultCenter, { draggable: true }).addTo(map);

  async function reverseGeocode(lat, lng) {
    const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lng)}`;
    try {
      const res = await fetch(url, { headers: { "Accept": "application/json" } });
      if (!res.ok) throw new Error("Reverse failed");
      const data = await res.json();
      return data.display_name || "";
    } catch {
      return "";
    }
  }

  async function forwardGeocode(q) {
    const url = `https://nominatim.openstreetmap.org/search?format=jsonv2&q=${encodeURIComponent(q)}&limit=5`;
    const res = await fetch(url, { headers: { "Accept": "application/json" } });
    if (!res.ok) return [];
    return await res.json();
  }

  let geocodeTimer = null;
  function setLocation(lat, lng, pan = true) {
    state.lat = lat;
    state.lng = lng;

    coordsText.textContent = `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
    marker.setLatLng([lat, lng]);
    if (pan) map.panTo([lat, lng]);

    if (geocodeTimer) clearTimeout(geocodeTimer);
    geocodeTimer = setTimeout(async () => {
      if (!addressInput) return;
      addressInput.value = "Finding address...";
      const addr = await reverseGeocode(lat, lng);
      state.address = addr || "";
      addressInput.value = addr || "";
    }, 350);
  }

  map.on("click", (e) => setLocation(e.latlng.lat, e.latlng.lng, false));
  marker.on("dragend", () => {
    const p = marker.getLatLng();
    setLocation(p.lat, p.lng, false);
  });

  confirmLocationBtn?.addEventListener("click", () => {
    if (!state.lat || !state.lng) return showToast("Pick a location first", toastId);
    showToast("Location saved ✅", toastId);
  });

  useMyLocationBtn?.addEventListener("click", () => {
    if (!navigator.geolocation) return showToast("Geolocation not supported", toastId);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        map.setView([lat, lng], 15);
        setLocation(lat, lng, false);
        showToast("Using your location ✅", toastId);
      },
      () => showToast("Permission denied / unavailable", toastId),
      { enableHighAccuracy: true, timeout: 8000 }
    );
  });

  // --- Address typing => suggestions => marker updates
  let suggestTimer = null;
  addressInput?.addEventListener("input", () => {
    const q = addressInput.value.trim();
    if (suggestTimer) clearTimeout(suggestTimer);
    if (q.length < 3) {
      suggestBox.classList.remove("show");
      suggestBox.innerHTML = "";
      return;
    }
    suggestTimer = setTimeout(async () => {
      const results = await forwardGeocode(q);
      if (!results.length) {
        suggestBox.classList.remove("show");
        suggestBox.innerHTML = "";
        return;
      }
      suggestBox.innerHTML = results.map(r => `
        <div class="suggestItem" data-lat="${r.lat}" data-lon="${r.lon}">
          ${r.display_name}
        </div>
      `).join("");
      suggestBox.classList.add("show");

      [...suggestBox.querySelectorAll(".suggestItem")].forEach(item => {
        item.addEventListener("click", () => {
          const lat = Number(item.dataset.lat);
          const lon = Number(item.dataset.lon);
          addressInput.value = item.textContent.trim();
          state.address = addressInput.value;
          setLocation(lat, lon, true);
          suggestBox.classList.remove("show");
        });
      });
    }, 400);
  });

  document.addEventListener("click", (e) => {
    if (!suggestBox.contains(e.target) && e.target !== addressInput) {
      suggestBox.classList.remove("show");
    }
  });

  // --- Save to localStorage & backend when Submit clicked
  const submitBtn = document.getElementById("submitBtn");
  submitBtn?.addEventListener("click", async () => {
    // collect minimal values from your existing page IDs
    state.address = addressInput?.value.trim() || state.address;
    const setupData = { ...state };

    localStorage.setItem("businessSetupData", JSON.stringify(setupData));

    // also save into DB if token exists
    try {
      await saveBusinessSetup(setupData);
    } catch (e) {
      // backend optional - UI can still work
    }

    showToast("Saved ✅ Redirecting...", toastId);
    window.location.href = "Profit Loss Forecast.html";
  });

  // --- On load: try load from backend, else localStorage
  async function boot() {
    const local = safeJSONParse(localStorage.getItem("businessSetupData"), null);
    if (local?.lat && local?.lng) {
      Object.assign(state, local);
      setLocation(state.lat, state.lng, true);
      if (addressInput) addressInput.value = state.address || addressInput.value;
      return;
    }

    // if user logged in, load profile from backend
    try {
      const data = await loadBusinessSetup();
      if (data?.profile?.lat && data?.profile?.lng) {
        Object.assign(state, data.profile);
        localStorage.setItem("businessSetupData", JSON.stringify(state));
        setLocation(state.lat, state.lng, true);
        if (addressInput) addressInput.value = state.address || "";
      } else {
        setLocation(defaultCenter[0], defaultCenter[1], false);
      }
    } catch {
      setLocation(defaultCenter[0], defaultCenter[1], false);
    }
  }

  boot();
})();
