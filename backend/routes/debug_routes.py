from flask import Blueprint, jsonify
from db.database import init_db

debug_bp = Blueprint("debug_bp", __name__)

@debug_bp.get("/init-db")
def initdb():
    init_db()
    return jsonify({"ok": True, "message": "DB initialized"})
