import { createStars, showToast, safeJSONParse, clamp, fmtMoney } from "./utils.js";
import { forecastProfitLoss, loadBusinessSetup } from "./api.js";

(() => {
  createStars("stars", 150);

  const toastId = "toast";

  // ---------- MAP
  const defaultCenter = [13.0827, 80.2707]; // fallback Chennai
  const map = L.map("map", { zoomControl: false }).setView(defaultCenter, 13);

  const osm = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19, attribution: "&copy; OpenStreetMap contributors"
  }).addTo(map);

  const esriSat = L.tileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    { maxZoom: 19, attribution: "Tiles &copy; Esri" }
  );

  const storeIcon = L.icon({
    iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
    shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
    iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
  });

  const marker = L.marker(defaultCenter, { draggable: true, icon: storeIcon }).addTo(map);

  // ---------- mode
  let mode = "yearly";
  const modeMonthlyBtn = document.getElementById("modeMonthly");
  const modeYearlyBtn = document.getElementById("modeYearly");

  function setMode(next) {
    mode = next;
    modeMonthlyBtn?.classList.toggle("active", mode === "monthly");
    modeYearlyBtn?.classList.toggle("active", mode === "yearly");

    const ll = marker.getLatLng();
    updateFromBackend(ll.lat, ll.lng);
  }

  modeMonthlyBtn?.addEventListener("click", () => setMode("monthly"));
  modeYearlyBtn?.addEventListener("click", () => setMode("yearly"));

  // ---------- map interactions
  map.on("click", (e) => {
    marker.setLatLng(e.latlng);
    updateFromBackend(e.latlng.lat, e.latlng.lng);
  });

  marker.on("dragend", () => {
    const ll = marker.getLatLng();
    updateFromBackend(ll.lat, ll.lng);
  });

  // UI buttons (if present)
  document.getElementById("zoomIn")?.addEventListener("click", () => map.zoomIn());
  document.getElementById("zoomOut")?.addEventListener("click", () => map.zoomOut());

  document.getElementById("btnCenter")?.addEventListener("click", () => {
    map.panTo(marker.getLatLng(), { animate: true, duration: .5 });
  });

  document.getElementById("btnMyLoc")?.addEventListener("click", () => {
    if (!navigator.geolocation) return showToast("Geolocation not supported", toastId);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const ll = { lat: pos.coords.latitude, lng: pos.coords.longitude };
        map.setView([ll.lat, ll.lng], 14, { animate: true });
        marker.setLatLng(ll);
        updateFromBackend(ll.lat, ll.lng);
      },
      () => showToast("Could not access location", toastId),
      { enableHighAccuracy: true, timeout: 8000 }
    );
  });

  // Satellite toggle (if present)
  const tabMap = document.getElementById("tabMap");
  const tabSat = document.getElementById("tabSat");

  tabMap?.addEventListener("click", () => {
    tabMap.classList.add("active");
    tabSat?.classList.remove("active");
    map.removeLayer(esriSat);
    osm.addTo(map);
  });

  tabSat?.addEventListener("click", () => {
    tabSat.classList.add("active");
    tabMap?.classList.remove("active");
    map.removeLayer(osm);
    esriSat.addTo(map);
  });

  // ---------- KPI refs
  const netProfitEl = document.getElementById("netProfit");
  const revenueEl = document.getElementById("revenue");
  const expensesEl = document.getElementById("expenses");
  const breakevenMonthsEl = document.getElementById("breakevenMonths");

  const profitPredEl = document.getElementById("profitPred");
  const profitPredSub = document.getElementById("profitPredSub");
  const beBig = document.getElementById("beBig");
  const beBigSub = document.getElementById("beBigSub");

  // ---- update UI
  function applyForecast(f) {
    if (!f) return;

    revenueEl.textContent = fmtMoney(f.revenue);
    expensesEl.textContent = fmtMoney(f.expenses);
    netProfitEl.textContent = fmtMoney(f.profit);
    breakevenMonthsEl.textContent = String(f.breakeven_months);

    profitPredEl.textContent = "+ " + fmtMoney(f.predicted_profit);
    profitPredSub.textContent = (mode === "yearly")
      ? "Projected additional profit for this year based on current trends."
      : "Projected profit for next month based on current trends.";

    beBig.textContent = String(f.breakeven_months);
    beBigSub.textContent = `You will cover initial costs and break even in ${f.breakeven_months} months.`;
  }

  // ---------- call backend forecast API (preferred)
  async function updateFromBackend(lat, lng) {
    try {
      const data = await forecastProfitLoss({ lat, lng, mode });
      applyForecast(data.forecast);
    } catch (e) {
      // fallback: still update numbers simply
      const scale = (mode === "yearly") ? 12 : 1;
      const seed = Math.floor(lat * 1000 + lng * 1000);
      const demand = clamp((Math.sin(seed) + 1) / 2, 0, 1);
      const revenue = (35000 + demand * 85000) * scale;
      const expenses = (21000 + demand * 52000) * scale;
      const profit = Math.max(0, revenue - expenses);
      applyForecast({
        revenue, expenses, profit,
        breakeven_months: clamp(Math.round(240000 / Math.max(1000, profit / scale)), 2, 18),
        predicted_profit: profit * 0.12
      });
    }
  }

  // ---------- load saved location and set map
  async function boot() {
    // 1) localStorage
    const local = safeJSONParse(localStorage.getItem("businessSetupData"), null);
    if (local?.lat && local?.lng) {
      map.setView([local.lat, local.lng], 13);
      marker.setLatLng([local.lat, local.lng]);
      updateFromBackend(local.lat, local.lng);
      setTimeout(() => map.invalidateSize(), 250);
      return;
    }

    // 2) backend profile
    try {
      const data = await loadBusinessSetup();
      const p = data?.profile;
      if (p?.lat && p?.lng) {
        localStorage.setItem("businessSetupData", JSON.stringify(p));
        map.setView([p.lat, p.lng], 13);
        marker.setLatLng([p.lat, p.lng]);
        updateFromBackend(p.lat, p.lng);
      } else {
        updateFromBackend(defaultCenter[0], defaultCenter[1]);
      }
    } catch {
      updateFromBackend(defaultCenter[0], defaultCenter[1]);
    }

    setTimeout(() => map.invalidateSize(), 250);
  }

  setMode("yearly");
  boot();
})();
