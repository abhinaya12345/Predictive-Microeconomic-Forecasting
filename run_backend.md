# Run Backend (Flask)

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
python app.py



---

## ✅ `README.md` (project overview)
```md
# BusinessInsights

Frontend: HTML/CSS/JS (Leaflet, Chart-ready)  
Backend: Python Flask API  
ML: Regression + Time-series style deterministic forecast  
DB: SQLite

## Run steps
1) Start backend
- follow `run_backend.md`

2) Start frontend
- follow `run_frontend.md`

## Location Sync
- "Set Up Your Business" saves location to:
  - localStorage `businessSetupData`
  - AND Flask DB if logged in

- "Profit Loss Forecast" loads location from:
  - localStorage first
  - else backend profile
