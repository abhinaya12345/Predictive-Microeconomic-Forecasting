# backend/routes/auth_routes.py
import uuid
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db.database import get_db

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/signup")
def signup():
    data = request.get_json(force=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "").strip()

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    db = get_db()

    try:
        db.execute(
            "INSERT INTO users(name, email, password_hash) VALUES (?,?,?)",
            (name or "User", email, generate_password_hash(password))
        )
        db.commit()
    except Exception:
        return jsonify({"error": "Email already exists"}), 400

    user = db.execute("SELECT id, name, email FROM users WHERE email=?", (email,)).fetchone()

    token = str(uuid.uuid4())
    db.execute("INSERT INTO sessions(user_id, token) VALUES (?,?)", (user["id"], token))
    db.commit()

    return jsonify({"token": token, "user": {"id": user["id"], "email": user["email"], "name": user["name"]}})

@auth_bp.post("/login")
def login():
    data = request.get_json(force=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "").strip()

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = str(uuid.uuid4())
    db.execute("INSERT INTO sessions(user_id, token) VALUES (?,?)", (user["id"], token))
    db.commit()

    return jsonify({"token": token, "user": {"id": user["id"], "email": user["email"], "name": user["name"]}})

@auth_bp.post("/forgot-password")
def forgot_password():
    data = request.get_json(force=True) or {}
    email = (data.get("email") or "").strip().lower()
    if not email:
        return jsonify({"error": "Email required"}), 400

    # demo code (in real life email it)
    code = "123456"

    db = get_db()
    db.execute("INSERT INTO password_resets(email, code, verified) VALUES (?,?,0)", (email, code))
    db.commit()

    return jsonify({"message": "Verification code generated (demo)", "demo_code": code})

@auth_bp.post("/verify-code")
def verify_code():
    data = request.get_json(force=True) or {}
    email = (data.get("email") or "").strip().lower()
    code = (data.get("code") or "").strip()

    db = get_db()
    row = db.execute("""
        SELECT * FROM password_resets
        WHERE email=? AND code=?
        ORDER BY id DESC LIMIT 1
    """, (email, code)).fetchone()

    if not row:
        return jsonify({"error": "Invalid code"}), 400

    db.execute("UPDATE password_resets SET verified=1 WHERE id=?", (row["id"],))
    db.commit()

    return jsonify({"message": "Code verified"})

@auth_bp.post("/reset-password")
def reset_password():
    data = request.get_json(force=True) or {}
    email = (data.get("email") or "").strip().lower()
    code = (data.get("code") or "").strip()
    new_password = (data.get("new_password") or "").strip()

    if not new_password:
        return jsonify({"error": "New password required"}), 400

    db = get_db()
    row = db.execute("""
        SELECT * FROM password_resets
        WHERE email=? AND code=? AND verified=1
        ORDER BY id DESC LIMIT 1
    """, (email, code)).fetchone()

    if not row:
        return jsonify({"error": "Code not verified"}), 400

    db.execute(
        "UPDATE users SET password_hash=? WHERE email=?",
        (generate_password_hash(new_password), email)
    )
    db.commit()

    return jsonify({"message": "Password updated"})
