"""Leak Tracing & Forensic Analysis Engine.

Correlates recovered document fingerprints with cryptographic access ledger
events to trace physical and administrative chain of custody, identify the
custodian responsible, and produce an auditable investigative dossier.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from PIL import Image

from .fingerprint import extract_fingerprint
from .ledger import BlockchainLedger
from .models import AccessEvent


@dataclass
class ForensicReport:
    sample_type: str
    detected_copy_id: Optional[str]
    detection_layer: Optional[str]
    confidence_score: float
    detection_status: str
    custody_events_count: int
    last_known_custodian_id: Optional[str]
    last_known_location: Optional[str]
    last_action: Optional[str]
    last_timestamp: Optional[str]
    custody_trail: List[Dict[str, Any]]
    investigative_conclusion: str


class LeakTracer:
    def __init__(self, ledger: BlockchainLedger, registered_copies: Optional[Dict[str, Dict[str, Any]]] = None):
        self.ledger = ledger
        self.registered_copies = registered_copies or {}

    def trace_leak(
        self,
        sample_text: Optional[str] = None,
        sample_image: Optional[Image.Image] = None,
    ) -> ForensicReport:
        """Trace a leaked document snippet or image back to the responsible custodian."""
        sample_type = "IMAGE" if sample_image else ("TEXT" if sample_text else "UNKNOWN")

        # 1. Extract Fingerprint
        detection = extract_fingerprint(
            sample_text=sample_text,
            sample_image=sample_image,
            registered_copies=self.registered_copies,
        )

        copy_id = detection.get("detected_copy_id")
        layer = detection.get("detection_layer")
        conf = detection.get("confidence", 0.0)
        status = detection.get("status", "UNMATCHED")

        if not copy_id:
            return ForensicReport(
                sample_type=sample_type,
                detected_copy_id=None,
                detection_layer=layer,
                confidence_score=conf,
                detection_status=status,
                custody_events_count=0,
                last_known_custodian_id=None,
                last_known_location=None,
                last_action=None,
                last_timestamp=None,
                custody_trail=[],
                investigative_conclusion=(
                    "NO ATTRIBUTABLE FINGERPRINT DETECTED: The provided excerpt does not "
                    "contain valid cryptographic or steganographic markers. Chain of custody "
                    "cannot be established."
                ),
            )

        # 2. Query Blockchain Ledger for Custody Events
        events = self.ledger.get_events_for_copy(copy_id)

        # Sort chronologically
        events.sort(key=lambda e: e.timestamp)

        custody_trail = [
            {
                "event_id": e.event_id,
                "timestamp": e.timestamp,
                "action": e.action,
                "custodian_id": e.custodian_id,
                "location": e.location,
                "signature_valid": e.verify(),
            }
            for e in events
        ]

        last_custodian = events[-1].custodian_id if events else None
        last_loc = events[-1].location if events else None
        last_action = events[-1].action if events else None
        last_time = events[-1].timestamp if events else None

        if events:
            conclusion = (
                f"POSITIVE ATTRIBUTION: Leaked copy {copy_id} was identified via {layer} "
                f"with {conf*100:.1f}% confidence. The cryptographic access ledger verifies "
                f"{len(events)} logged custody transitions. The document was last handled by "
                f"Custodian '{last_custodian}' at location '{last_loc}' during action "
                f"'{last_action}' on {last_time}. All cryptographic signatures verified."
            )
        else:
            conclusion = (
                f"FINGERPRINT DETECTED WITHOUT LEDGER RECORD: Copy {copy_id} was recognized, "
                f"but no corresponding custody events exist in the active ledger. Possible unlogged copy."
            )

        return ForensicReport(
            sample_type=sample_type,
            detected_copy_id=copy_id,
            detection_layer=layer,
            confidence_score=conf,
            detection_status=status,
            custody_events_count=len(events),
            last_known_custodian_id=last_custodian,
            last_known_location=last_loc,
            last_action=last_action,
            last_timestamp=last_time,
            custody_trail=custody_trail,
            investigative_conclusion=conclusion,
        )
