"""Fingerprint Service: Coordinates multi-layer steganography and visual artifact rendering."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.fingerprint import (
    SYNTACTIC_RULES,
    apply_fingerprint_to_text,
    derive_syntactic_vector,
    render_paper_image,
)
from webapp.database import get_db_connection, log_activity

COPIES_DIR = ROOT_DIR / "webapp" / "static" / "generated_copies"


class FingerprintService:
    @classmethod
    def list_copies(cls) -> List[Dict[str, Any]]:
        """List all generated fingerprinted copies."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(
                """
                SELECT f.*, c.name as custodian_name, c.role as custodian_role, c.center_code
                FROM fingerprinted_copies f
                LEFT JOIN custodians c ON f.custodian_id = c.custodian_id
                ORDER BY f.id ASC
                """
            ).fetchall()
            copies = []
            for r in rows:
                d = dict(r)
                d["syntactic_vector"] = json.loads(d["syntactic_vector"])
                copies.append(d)
            return copies

    @classmethod
    def get_copy(cls, copy_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve copy details by ID."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute(
                """
                SELECT f.*, c.name as custodian_name, c.role as custodian_role, c.center_code, c.public_key
                FROM fingerprinted_copies f
                LEFT JOIN custodians c ON f.custodian_id = c.custodian_id
                WHERE f.copy_id = ?
                """,
                (copy_id,),
            ).fetchone()
            if not row:
                return None
            d = dict(row)
            d["syntactic_vector"] = json.loads(d["syntactic_vector"])
            return d

    @classmethod
    def get_registered_manifest(cls) -> Dict[str, Dict[str, Any]]:
        """Return manifest dictionary formatted for LeakTracer."""
        copies = cls.list_copies()
        manifest: Dict[str, Dict[str, Any]] = {}
        for c in copies:
            manifest[c["copy_id"]] = {
                "copy_id": c["copy_id"],
                "custodian_id": c["custodian_id"],
                "syntactic_vector": c["syntactic_vector"],
                "text_file": c.get("text_file"),
                "image_file": c.get("image_file"),
            }
        return manifest

    @classmethod
    def generate_copy_record(
        cls,
        paper_id: str,
        base_text: str,
        copy_idx: int,
        custodian_id: str,
        is_demo: bool = False,
    ) -> Dict[str, Any]:
        """Generate a single fingerprinted copy with Layer 1, Layer 2, and Layer 3 artifacts."""
        COPIES_DIR.mkdir(parents=True, exist_ok=True)
        copy_id = f"CPY-{copy_idx:02d}"
        vector = derive_syntactic_vector(copy_idx)

        # 1. Apply Layer 1 (Zero-Width) and Layer 2 (Syntactic)
        fp_text = apply_fingerprint_to_text(base_text, copy_id, copy_idx, paper_id)

        # Write text artifact
        text_filename = f"{copy_id}.txt"
        text_path = COPIES_DIR / text_filename
        text_path.write_text(fp_text, encoding="utf-8")

        # 2. Render Layer 3 (Visual raster corner micro-grid and watermark)
        img = render_paper_image(fp_text, copy_id)
        img_filename = f"{copy_id}.png"
        img_path = COPIES_DIR / img_filename
        img.save(img_path)

        # Preview snippet (first 300 characters without zero-width chars for display)
        preview_text = "".join(ch for ch in fp_text[:350] if ch not in "\u200b\u200c\u200d")

        now_ts = datetime.now(timezone.utc).isoformat()

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO fingerprinted_copies
                (copy_id, paper_id, custodian_id, copy_idx, syntactic_vector, text_preview, text_file, image_file, is_demo, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    copy_id,
                    paper_id,
                    custodian_id,
                    copy_idx,
                    json.dumps(vector),
                    preview_text,
                    text_filename,
                    img_filename,
                    1 if is_demo else 0,
                    now_ts,
                ),
            )
            conn.commit()

        log_activity(
            action_type="GENERATE_FINGERPRINT",
            details=f"Generated multi-layer fingerprinted copy {copy_id} (Assigned Custodian: {custodian_id}).",
            status="SUCCESS",
        )

        return cls.get_copy(copy_id)  # type: ignore
