"""Database connection and initialization module for Quorum-Zeolite.

Connects to SQLite by default (quorum_zeolite.db in repo root) or PostgreSQL
if DATABASE_URL environment variable is provided and reachable.
"""

from __future__ import annotations
import os
import sqlite3
import json
from pathlib import Path
from typing import Any

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "quorum_zeolite.db")

def get_connection():
    """Get a database connection (SQLite by default)."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables from schema.sql and apply schema migrations."""
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with get_connection() as conn:
        conn.executescript(schema_sql)
        try:
            conn.execute("ALTER TABLE subjobs ADD COLUMN snapshots_json TEXT")
        except Exception:
            pass
        conn.commit()

init_db()
