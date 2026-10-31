"""Examination Service: Handles question paper creation, registration, and plain text rendering."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.models import QuestionPaper
from src.paper_generator import generate_synthetic_question_paper
from webapp.database import get_db_connection, log_activity


class ExaminationService:
    @staticmethod
    def list_examinations() -> List[Dict[str, Any]]:
        """List all registered examinations."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(
                "SELECT * FROM examinations ORDER BY id DESC"
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def get_examination(paper_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve single examination record by paper_id."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute(
                "SELECT * FROM examinations WHERE paper_id = ?", (paper_id,)
            ).fetchone()
            return dict(row) if row else None

    @classmethod
    def create_synthetic_examination(
        cls,
        paper_id: str = "QP-2026-CS801-AUTUMN",
        is_demo: bool = False,
    ) -> Dict[str, Any]:
        """Generate and save standard university examination question paper."""
        paper = generate_synthetic_question_paper(paper_id=paper_id)
        raw_text = paper.render_plain_text()
        now_ts = datetime.now(timezone.utc).isoformat()

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO examinations 
                (paper_id, course_code, course_title, exam_date, duration_minutes, max_marks, raw_text, is_demo, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    paper.paper_id,
                    paper.course_code,
                    paper.course_title,
                    paper.exam_date,
                    paper.duration_minutes,
                    paper.max_marks,
                    raw_text,
                    1 if is_demo else 0,
                    now_ts,
                ),
            )
            conn.commit()

        log_activity(
            action_type="REGISTER_EXAMINATION",
            details=f"Registered examination paper {paper.paper_id} ({paper.course_code}: {paper.course_title}).",
            status="SUCCESS",
        )
        return cls.get_examination(paper_id)  # type: ignore
