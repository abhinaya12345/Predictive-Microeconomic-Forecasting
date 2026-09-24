// frontend/assets/js/api.js
window.API = {
  base: "/api",

  async json(url, options = {}) {
    const res = await fetch(url, {
      headers: { "Content-Type": "application/json", ...(options.headers || {}) },
      ...options,
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data?.error || data?.message || `HTTP ${res.status}`);
    return data;
  },

  // Business profile
  saveSetup(payload) {
    return this.json(`${this.base}/business/save-setup`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  loadSetup(userId = 1) {
    return this.json(`${this.base}/business/load-setup/${userId}`);
  },

  // Forecast
  forecastProfitLoss(payload) {
    return this.json(`${this.base}/forecast/profit-loss`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
};
