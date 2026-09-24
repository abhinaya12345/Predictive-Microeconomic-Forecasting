# backend/db/database.py
import sqlite3
from pathlib import Path
from flask import current_app, g

from .models import CREATE_TABLES_SQL


def _db_path() -> Path:
    # backend/instance/businessinsights.db
    instance_dir = Path(current_app.instance_path)
    instance_dir.mkdir(parents=True, exist_ok=True)
    return instance_dir / "businessinsights.db"


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        db_file = _db_path()
        conn = sqlite3.connect(db_file, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        g.db = conn
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(CREATE_TABLES_SQL)
    db.commit()


def register_db(app):
    app.teardown_appcontext(close_db)
