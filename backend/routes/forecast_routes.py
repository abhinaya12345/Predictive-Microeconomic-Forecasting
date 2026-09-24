# backend/routes/forecast_routes.py
from flask import Blueprint, request, jsonify
import json

from db.database import get_db
from ml.regression import predict_profit_loss
from ml.time_series import predict_inflation_series

forecast_bp = Blueprint("forecast_bp", __name__)

@forecast_bp.post("/profit-loss")
def profit_loss_forecast():
    data = request.get_json(force=True) or {}

    # ✅ validate lat/lng safely
    try:
        lat = float(data.get("lat"))
        lng = float(data.get("lng"))
    except (TypeError, ValueError):
        return jsonify({"ok": False, "error": "lat and lng are required numbers"}), 400

    mode = (data.get("mode") or "yearly").lower().strip()
    if mode not in ("monthly", "yearly"):
        mode = "yearly"

    user_id = int(data.get("user_id", 1))  # demo default

    # ✅ ML predictions
    pred = predict_profit_loss(lat, lng, mode=mode)
    infl = predict_inflation_series(lat, lng, score=pred["score"])

    # ✅ save forecast into DB (if forecasts table exists)
    db = get_db()

    # ✅ Ensure demo user exists (user_id=1)
    existing_user = db.execute("SELECT id FROM users WHERE id=?", (user_id,)).fetchone()
    if not existing_user:
        db.execute(
            "INSERT INTO users (id, name, email, password_hash) VALUES (?, ?, ?, ?)",
            (user_id, "Demo User", "demo@local", "demo")
        )
        db.commit()

    db.execute(
        """
        INSERT INTO forecasts
        (user_id, lat, lng, mode, revenue, expenses, profit, breakeven_months, inflation_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            lat, lng, mode,
            float(pred["revenue"]),
            float(pred["expenses"]),
            float(pred["profit"]),
            int(pred["breakeven_months"]),
            json.dumps(infl)
        )
    )
    db.commit()

    return jsonify({
        "ok": True,
        "forecast": {
            "mode": pred["mode"],
            "score": pred["score"],
            "revenue": pred["revenue"],
            "expenses": pred["expenses"],
            "profit": pred["profit"],
            "breakeven_months": pred["breakeven_months"],
            "inflation": infl
        }
    })
