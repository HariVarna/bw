"""Custodian Service: Manages examination custodians and Ed25519 asymmetric key pairs."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.crypto import generate_keypair
from src.models import Custodian
from webapp.database import get_db_connection, log_activity


class CustodianService:
    @staticmethod
    def list_custodians() -> List[Dict[str, Any]]:
        """List all registered examination custodians."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(
                "SELECT id, custodian_id, name, role, center_code, public_key, is_demo, created_at FROM custodians ORDER BY id ASC"
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_custodian(custodian_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve custodian by ID."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute(
                "SELECT * FROM custodians WHERE custodian_id = ?", (custodian_id,)
            ).fetchone()
            return dict(row) if row else None

    @classmethod
    def register_custodian(
        cls,
        custodian_id: str,
        name: str,
        role: str,
        center_code: str,
        is_demo: bool = False,
    ) -> Dict[str, Any]:
        """Generate Ed25519 keypair and register new examination custodian."""
        priv_key, pub_key = generate_keypair()
        now_ts = datetime.now(timezone.utc).isoformat()

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO custodians 
                (custodian_id, name, role, center_code, public_key, private_key, is_demo, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    custodian_id,
                    name,
                    role,
                    center_code,
                    pub_key,
                    priv_key,
                    1 if is_demo else 0,
                    now_ts,
                ),
            )
            conn.commit()

        log_activity(
            action_type="REGISTER_CUSTODIAN",
            details=f"Registered custodian {custodian_id} ({name}, Role: {role}, Center: {center_code}). Ed25519 keypair generated.",
            status="SUCCESS",
        )
        return cls.get_custodian(custodian_id)  # type: ignore
