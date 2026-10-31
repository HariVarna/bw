"""Tracing Service: Executes forensic leak attribution across document artifacts."""

from __future__ import annotations

import io
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from PIL import Image

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.leak_tracer import ForensicReport, LeakTracer
from webapp.database import get_db_connection, log_activity
from webapp.services.access_ledger_service import AccessLedgerService
from webapp.services.fingerprint_service import FingerprintService


class TracingService:
    @classmethod
    def list_investigations(cls) -> List[Dict[str, Any]]:
        """List all past forensic leak investigation cases."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(
                "SELECT * FROM investigations ORDER BY id DESC"
            ).fetchall()
            return [dict(r) for r in rows]

    @classmethod
    def get_investigation(cls, case_number: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific forensic investigation by case number."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute(
                "SELECT * FROM investigations WHERE case_number = ?", (case_number,)
            ).fetchone()
            if not row:
                return None
            inv = dict(row)
            
            # Fetch custody trail if copy was detected
            if inv.get("detected_copy_id"):
                inv["custody_trail"] = AccessLedgerService.get_events_for_copy(inv["detected_copy_id"])
            else:
                inv["custody_trail"] = []
                
            return inv

    @classmethod
    def investigate(
        cls,
        sample_text: Optional[str] = None,
        sample_image_bytes: Optional[bytes] = None,
        filename: str = "submitted_sample.txt",
        is_demo: bool = False,
    ) -> Dict[str, Any]:
        """Perform multi-layer forensic leak attribution on submitted text or image."""
        ledger = AccessLedgerService.get_ledger()
        manifest = FingerprintService.get_registered_manifest()
        tracer = LeakTracer(ledger=ledger, registered_copies=manifest)

        pil_image: Optional[Image.Image] = None
        if sample_image_bytes:
            try:
                pil_image = Image.open(io.BytesIO(sample_image_bytes))
            except Exception as e:
                print(f"Error reading image: {e}")

        # Execute leak tracing
        report: ForensicReport = tracer.trace_leak(
            sample_text=sample_text,
            sample_image=pil_image,
        )

        # Generate unique case number
        import uuid
        case_id = f"CASE-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:4].upper()}"
        now_ts = datetime.now(timezone.utc).isoformat()

        snippet_preview = None
        if sample_text:
            snippet_preview = "".join(ch for ch in sample_text[:250] if ch not in "\u200b\u200c\u200d")

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO investigations (
                    case_number, sample_filename, sample_type, sample_snippet,
                    detected_copy_id, detection_layer, confidence_score,
                    attribution_status, responsible_custodian_id, custody_events_count,
                    investigative_conclusion, is_demo, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    case_id,
                    filename,
                    report.sample_type,
                    snippet_preview,
                    report.detected_copy_id,
                    report.detection_layer,
                    report.confidence_score,
                    report.detection_status,
                    report.last_known_custodian_id,
                    report.custody_events_count,
                    report.investigative_conclusion,
                    1 if is_demo else 0,
                    now_ts,
                ),
            )
            conn.commit()

        log_activity(
            action_type="LEAK_INVESTIGATION",
            details=f"Processed case {case_id}: Attribution {report.detection_status} (Detected: {report.detected_copy_id or 'None'}, Confidence: {report.confidence_score*100:.1f}%).",
            status="SUCCESS" if report.detected_copy_id else "WARNING",
        )

        return cls.get_investigation(case_id)  # type: ignore
