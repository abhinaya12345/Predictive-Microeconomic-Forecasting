import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("BI_SECRET_KEY", "businessinsights_secret_123")
    DB_PATH = os.environ.get("BI_DB_PATH", os.path.join(BASE_DIR, "instance", "businessinsights.db"))
