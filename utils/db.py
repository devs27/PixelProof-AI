import sqlite3
import os
import tempfile
from flask import g
from werkzeug.security import generate_password_hash

def _get_db_path():
    env_path = os.environ.get("DATABASE_PATH")
    if env_path:
        return env_path
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_path = os.path.join(base_dir, "pixelproof.db")
    
    # If running in serverless environment (Vercel) or root is read-only
    if os.environ.get("VERCEL") or not os.access(base_dir, os.W_OK):
        return os.path.join(tempfile.gettempdir(), "pixelproof.db")
    
    return target_path

DB_PATH = _get_db_path()

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    # Ensure parent directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            preview_filename TEXT,
            label TEXT NOT NULL,
            confidence REAL NOT NULL,
            patch_scores TEXT,
            locked INTEGER NOT NULL DEFAULT 0,
            scanned_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    
    # Seed demo account if users table is empty
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                       ("demo", generate_password_hash("demo123")))
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                       ("admin", generate_password_hash("admin123")))
    
    db.commit()
    db.close()
