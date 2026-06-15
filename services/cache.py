"""
Tiny local cache so CivicLens doesn't re-call the AI API every time someone
reloads a bill page. Stored in a SQLite file under data/ (gitignored) -
no external database needed.
"""

import json
import os
import sqlite3
from datetime import datetime, timezone

from config import CACHE_DB_PATH


def _connect():
    os.makedirs(os.path.dirname(CACHE_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(CACHE_DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS summaries (
            bill_id TEXT PRIMARY KEY,
            summary_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    return conn


def get_summary(bill_id):
    """Return a cached AI summary dict for bill_id, or None if not cached."""
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT summary_json FROM summaries WHERE bill_id = ?", (bill_id,)
        ).fetchone()
    finally:
        conn.close()
    return json.loads(row[0]) if row else None


def save_summary(bill_id, summary):
    """Store an AI summary dict for bill_id."""
    conn = _connect()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO summaries (bill_id, summary_json, created_at) VALUES (?, ?, ?)",
            (bill_id, json.dumps(summary), datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
    finally:
        conn.close()


def clear():
    """Wipe the cache. Useful if you change the AI prompt and want fresh summaries."""
    conn = _connect()
    try:
        conn.execute("DELETE FROM summaries")
        conn.commit()
    finally:
        conn.close()
