# backend/routes/business_routes.py
from flask import Blueprint, request, jsonify
from db.database import get_db

business_bp = Blueprint("business_bp", __name__)

@business_bp.post("/save-setup")
def save_setup():
    data = request.get_json(force=True) or {}
    user_id = int(data.get("user_id", 1))  # demo default (replace later with session auth)

    # focusAreas can be list or string
    focus_areas = data.get("focusAreas", [])
    if isinstance(focus_areas, list):
        focus_areas = ", ".join([str(x) for x in focus_areas if str(x).strip()])
    else:
        focus_areas = str(focus_areas or "")

    db = get_db()

    db.execute(
        "INSERT OR IGNORE INTO users(id, name, email, password_hash) VALUES (1, 'Demo', 'demo@local', 'demo')"
    )
    db.commit()

    # ✅ Ensure demo user exists (user_id=1)
    existing_user = db.execute("SELECT id FROM users WHERE id=?", (user_id,)).fetchone()
    if not existing_user:
        db.execute(
            "INSERT INTO users (id, name, email, password_hash) VALUES (?, ?, ?, ?)",
            (user_id, "Demo User", "demo@local", "demo")
        )
        db.commit()

    # check if profile exists
    row = db.execute(
        "SELECT id FROM business_profiles WHERE user_id=?",
        (user_id,)
    ).fetchone()

    payload = (
        data.get("businessType"),
        data.get("budget"),
        data.get("address"),
        data.get("lat"),
        data.get("lng"),
        data.get("shopSize"),
        data.get("experience"),
        data.get("targetCustomers"),
        data.get("primaryGoal"),
        data.get("revenueTarget"),
        focus_areas,
        data.get("goalNotes"),
        user_id
    )

    if row:
        db.execute("""
            UPDATE business_profiles
            SET business_type=?,
                budget=?,
                address=?,
                lat=?,
                lng=?,
                shop_size=?,
                experience=?,
                target_customers=?,
                primary_goal=?,
                revenue_target=?,
                focus_areas=?,
                goal_notes=?,
                updated_at=CURRENT_TIMESTAMP
            WHERE user_id=?
        """, payload)
    else:
        db.execute("""
            INSERT INTO business_profiles
            (business_type, budget, address, lat, lng, shop_size, experience,
             target_customers, primary_goal, revenue_target, focus_areas, goal_notes, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, payload)

    db.commit()
    return jsonify({"ok": True})


@business_bp.get("/load-setup/<int:user_id>")
def load_setup(user_id):
    db = get_db()
    row = db.execute("""
        SELECT *
        FROM business_profiles
        WHERE user_id=?
        ORDER BY updated_at DESC
        LIMIT 1
    """, (user_id,)).fetchone()

    if not row:
        return jsonify({"ok": False, "message": "No profile found"}), 404

    return jsonify({"ok": True, "profile": dict(row)})
