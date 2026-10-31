"""SQLite Database Layer for Blockchain Leak Tracing Web Application."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Base paths
WEBAPP_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = WEBAPP_DIR / "instance"
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = INSTANCE_DIR / "bw_records.db"


def get_db_connection() -> sqlite3.Connection:
    """Create and return a thread-safe connection to the SQLite database."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Initialize SQLite database tables and indexes."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # 1. Examinations Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS examinations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paper_id TEXT UNIQUE NOT NULL,
                course_code TEXT NOT NULL,
                course_title TEXT NOT NULL,
                exam_date TEXT NOT NULL,
                duration_minutes INTEGER NOT NULL,
                max_marks INTEGER NOT NULL,
                raw_text TEXT NOT NULL,
                is_demo INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)

        # 2. Custodians Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS custodians (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                custodian_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                center_code TEXT NOT NULL,
                public_key TEXT NOT NULL,
                private_key TEXT,
                is_demo INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)

        # 3. Fingerprinted Copies Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fingerprinted_copies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                copy_id TEXT UNIQUE NOT NULL,
                paper_id TEXT NOT NULL,
                custodian_id TEXT NOT NULL,
                copy_idx INTEGER NOT NULL,
                syntactic_vector TEXT NOT NULL,
                text_preview TEXT NOT NULL,
                text_file TEXT,
                image_file TEXT,
                is_demo INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY (paper_id) REFERENCES examinations(paper_id) ON DELETE CASCADE,
                FOREIGN KEY (custodian_id) REFERENCES custodians(custodian_id)
            )
        """)

        # 4. Investigations Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS investigations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_number TEXT UNIQUE NOT NULL,
                sample_filename TEXT NOT NULL,
                sample_type TEXT NOT NULL,
                sample_snippet TEXT,
                detected_copy_id TEXT,
                detection_layer TEXT,
                confidence_score REAL,
                attribution_status TEXT NOT NULL,
                responsible_custodian_id TEXT,
                custody_events_count INTEGER DEFAULT 0,
                investigative_conclusion TEXT NOT NULL,
                is_demo INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)

        # 5. Activity Logs Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action_type TEXT NOT NULL,
                details TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)

        conn.commit()


def log_activity(action_type: str, details: str, status: str = "SUCCESS") -> None:
    """Record an operational event in the activity log."""
    now_ts = datetime.now(timezone.utc).isoformat()
    try:
        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO activity_logs (timestamp, action_type, details, status) VALUES (?, ?, ?, ?)",
                (now_ts, action_type, details, status),
            )
            conn.commit()
    except Exception as e:
        print(f"Failed to log activity: {e}")


def get_dashboard_counts() -> Dict[str, int]:
    """Retrieve aggregate counts for dashboard KPI indicators."""
    counts = {
        "examinations": 0,
        "custodians": 0,
        "fingerprinted_copies": 0,
        "investigations": 0,
        "recorded_events": 0,
        "blocks": 0,
    }
    with get_db_connection() as conn:
        cursor = conn.cursor()
        counts["examinations"] = cursor.execute("SELECT COUNT(*) FROM examinations").fetchone()[0]
        counts["custodians"] = cursor.execute("SELECT COUNT(*) FROM custodians").fetchone()[0]
        counts["fingerprinted_copies"] = cursor.execute("SELECT COUNT(*) FROM fingerprinted_copies").fetchone()[0]
        counts["investigations"] = cursor.execute("SELECT COUNT(*) FROM investigations").fetchone()[0]

    return counts


def get_recent_activities(limit: int = 8) -> List[Dict[str, Any]]:
    """Retrieve recent operational activity logs."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        rows = cursor.execute(
            "SELECT * FROM activity_logs ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
