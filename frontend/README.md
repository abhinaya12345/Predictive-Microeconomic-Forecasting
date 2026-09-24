# BusinessInsights Frontend (Static UI)

This folder contains all your UI pages (HTML) + shared assets (CSS/JS/images).

## Folder Layout
- `pages/` → all HTML files (home, login, signup, dashboards, etc.)
- `assets/css/` → common + page-specific CSS
- `assets/js/` → page logic + API calls to Flask backend

## How to Run (IMPORTANT)
Because we use ES Modules (`type="module"` with import/export), you **must** run using a local server.

### Option A: VS Code Live Server (Recommended)
1. Open the project folder in VS Code
2. Go to: `frontend/pages/`
3. Right click `home.html` → **Open with Live Server**

### Option B: Python HTTP Server
From inside `frontend/pages/`:
```bash
python -m http.server 5500


---

## ✅ `BusinessInsights/run_backend.md`
```md
# Run Backend (Flask)

## 1) Go to backend folder
```bash
cd BusinessInsights/backend


---

## ✅ `BusinessInsights/README.md`
```md
# BusinessInsights (Full Project)

## Tech Stack
- Frontend: HTML / CSS / JavaScript (Leaflet + UI dashboards)
- Backend: Python Flask (REST API)
- Database: SQLite (`backend/instance/businessinsights.db`)
- ML Module: Regression + Time-Series styled demo predictions

---

## Folder Structure
- `frontend/` → all UI pages + assets
- `backend/` → Flask app, routes, DB, ML module
- `run_frontend.md` → how to run UI
- `run_backend.md` → how to run backend

---

## How to Run
### 1) Start Backend
Follow: `run_backend.md`

### 2) Start Frontend
Follow: `run_frontend.md`

---

## Location Sync (Set Up → Profit & Loss)
When you choose a location in **Set Up Your Business** and click Submit:
- saved to `localStorage.businessSetupData`
- saved to SQLite database (if logged in)

In **Profit Loss Forecast**, the map auto-loads:
1. localStorage location first  
2. backend DB location if not found

---

## Notes
- Password reset is demo-based (verification code returned from API)
- You can upgrade it later by emailing OTP (SMTP) or using Twilio
