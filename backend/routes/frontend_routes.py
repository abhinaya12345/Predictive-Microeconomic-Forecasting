'''
# backend/routes/frontend_routes.py
from flask import Blueprint, send_from_directory, current_app
from pathlib import Path

frontend_bp = Blueprint("frontend_bp", __name__)

def _pages_dir() -> Path:
    return Path(current_app.config["FRONTEND_PAGES_DIR"]).resolve()

@frontend_bp.get("/")
def home():
    # default landing page
    return send_from_directory(_pages_dir(), "home.html")

# clean routes (recommended)
@frontend_bp.get("/home")
def home_alias():
    return send_from_directory(_pages_dir(), "home.html")

@frontend_bp.get("/login")
def login():
    return send_from_directory(_pages_dir(), "login.html")

@frontend_bp.get("/signup")
def signup():
    return send_from_directory(_pages_dir(), "signup.html")

@frontend_bp.get("/forgot-password")
def forgot_password():
    return send_from_directory(_pages_dir(), "forgot-password.html")

@frontend_bp.get("/verification")
def verification():
    return send_from_directory(_pages_dir(), "verification.html")

@frontend_bp.get("/reset-password")
def reset_password():
    return send_from_directory(_pages_dir(), "reset-password.html")

@frontend_bp.get("/setup-business")
def setup_business():
    # If your file name contains spaces, keep it exactly like below:
    return send_from_directory(_pages_dir(), "set-up-your-business.html")

@frontend_bp.get("/profit-loss")
def profit_loss():
    return send_from_directory(_pages_dir(), "profit-loss-forecast.html")

@frontend_bp.get("/location-dashboard")
def location_dashboard():
    return send_from_directory(_pages_dir(), "location-analysis-dashboard.html")

# fallback: allow direct loading like /pages/anyfile.html
@frontend_bp.get("/pages/<path:filename>")
def pages_any(filename):
    return send_from_directory(_pages_dir(), filename)
'''

# backend/routes/frontend_routes.py
from flask import Blueprint, send_from_directory, current_app
from pathlib import Path

frontend_bp = Blueprint("frontend_bp", __name__)

def pages_dir():
    return str(Path(current_app.config["FRONTEND_PAGES_DIR"]).resolve())

# ---------- Home ----------
@frontend_bp.get("/")
@frontend_bp.get("/home")
def home():
    return send_from_directory(pages_dir(), "home.html")

# ---------- Auth ----------
@frontend_bp.get("/login")
def login():
    return send_from_directory(pages_dir(), "login.html")

@frontend_bp.get("/signup")
def signup():
    return send_from_directory(pages_dir(), "signup.html")

@frontend_bp.get("/forgot-password")
def forgot_password():
    return send_from_directory(pages_dir(), "forgot-password.html")

@frontend_bp.get("/verification")
def verification():
    return send_from_directory(pages_dir(), "verification.html")

@frontend_bp.get("/reset-password")
def reset_password():
    return send_from_directory(pages_dir(), "reset-password.html")

# ---------- Business Flow ----------
@frontend_bp.get("/set-up-your-business")
def setup_business():
    return send_from_directory(pages_dir(), "set-up-your-business.html")

@frontend_bp.get("/profit-loss-forecast")
def profit_loss():
    return send_from_directory(pages_dir(), "profit-loss-forecast.html")

@frontend_bp.get("/location-analysis-dashboard")
def location_dashboard():
    return send_from_directory(pages_dir(), "location-analysis-dashboard.html")

# ---------- Fallback (optional, for direct file access) ----------
@frontend_bp.get("/pages/<path:filename>")
def pages_any(filename):
    return send_from_directory(pages_dir(), filename)
