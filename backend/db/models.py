'''
# backend/db/models.py

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS business_profiles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  business_type TEXT,
  budget TEXT,
  address TEXT,
  lat REAL,
  lng REAL,
  shop_size TEXT,
  experience TEXT,
  target_customers TEXT,
  primary_goal TEXT,
  revenue_target TEXT,
  focus_areas TEXT,
  goal_notes TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS forecasts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  business_profile_id INTEGER,
  lat REAL,
  lng REAL,
  mode TEXT, -- monthly/yearly
  revenue REAL,
  expenses REAL,
  profit REAL,
  breakeven_months INTEGER,
  inflation_json TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY(business_profile_id) REFERENCES business_profiles(id) ON DELETE SET NULL
);
"""
'''

# backend/db/models.py

CREATE_TABLES_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ✅ sessions table (needed for login token)
CREATE TABLE IF NOT EXISTS sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  token TEXT NOT NULL UNIQUE,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ✅ password_resets table (needed for forgot/reset flow)
CREATE TABLE IF NOT EXISTS password_resets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  code TEXT NOT NULL,
  verified INTEGER DEFAULT 0,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS business_profiles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  business_type TEXT,
  budget TEXT,
  address TEXT,
  lat REAL,
  lng REAL,
  shop_size TEXT,
  experience TEXT,
  target_customers TEXT,
  primary_goal TEXT,
  revenue_target TEXT,
  focus_areas TEXT,
  goal_notes TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS forecasts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  business_profile_id INTEGER,
  lat REAL,
  lng REAL,
  mode TEXT,
  revenue REAL,
  expenses REAL,
  profit REAL,
  breakeven_months INTEGER,
  inflation_json TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY(business_profile_id) REFERENCES business_profiles(id) ON DELETE SET NULL
);
"""
