# backend/app.py
from flask import Flask, jsonify
from flask_cors import CORS
from pathlib import Path

from routes.auth_routes import auth_bp
from routes.business_routes import business_bp
from routes.forecast_routes import forecast_bp
from routes.frontend_routes import frontend_bp

from routes.debug_routes import debug_bp

from db.database import init_db, register_db  # ✅ add this

def create_app():
    ROOT = Path(__file__).resolve().parents[1]

    FRONTEND_DIR = ROOT / "frontend"
    PAGES_DIR = FRONTEND_DIR / "pages"
    ASSETS_DIR = FRONTEND_DIR / "assets"

    app = Flask(
        __name__,
        static_folder=str(ASSETS_DIR),
        static_url_path="/assets"
    )

    app.config["FRONTEND_PAGES_DIR"] = str(PAGES_DIR)
    app.config["JSON_SORT_KEYS"] = False

    CORS(app)

    # ✅ ADD THIS
    register_db(app)

    # ✅ ADD THIS (THIS IS THE MAIN FIX)
    with app.app_context():
        init_db()

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(business_bp, url_prefix="/api/business")
    app.register_blueprint(forecast_bp, url_prefix="/api/forecast")
    app.register_blueprint(debug_bp, url_prefix="/api/debug")
    app.register_blueprint(frontend_bp)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    return app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="127.0.0.1", port=5000)
