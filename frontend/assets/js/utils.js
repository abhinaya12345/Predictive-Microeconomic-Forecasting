// utils.js - shared helpers

export function createStars(containerId = "stars", count = 150) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = "";
  for (let i = 0; i < count; i++) {
    const star = document.createElement("div");
    star.className = "star";
    star.style.left = Math.random() * 100 + "%";
    star.style.top = Math.random() * 100 + "%";
    star.style.animationDelay = Math.random() * 3 + "s";
    star.style.opacity = (0.25 + Math.random() * 0.75).toFixed(2);
    el.appendChild(star);
  }
}

let toastTimer = null;
export function showToast(msg, toastId = "toast", ms = 2200) {
  const toast = document.getElementById(toastId);
  if (!toast) return alert(msg);
  toast.textContent = msg;
  toast.classList.add("show");
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), ms);
}

export function clamp(n, a, b) {
  return Math.max(a, Math.min(b, n));
}

export function fmtMoney(n) {
  const val = Number(n || 0);
  return "$" + Math.round(val).toLocaleString();
}

export function safeJSONParse(str, fallback = null) {
  try { return JSON.parse(str); } catch { return fallback; }
}
