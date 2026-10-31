"""Domain models for Examination Question Paper Leak Tracing."""

from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from .crypto import canonical_json_bytes, compute_merkle_root, sha256_hex, sign_message, verify_signature


class AccessAction(str, Enum):
    PAPER_GENERATED = "PAPER_GENERATED"
    DISPATCHED_TO_CENTER = "DISPATCHED_TO_CENTER"
    RECEIVED_AT_CENTER = "RECEIVED_AT_CENTER"
    VAULT_DEPOSITED = "VAULT_DEPOSITED"
    SEAL_VERIFIED = "SEAL_VERIFIED"
    EXAM_HALL_TRANSFERRED = "EXAM_HALL_TRANSFERRED"
    DISTRIBUTED_TO_STUDENT = "DISTRIBUTED_TO_STUDENT"
    SURPLUS_RETURNED = "SURPLUS_RETURNED"


@dataclass
class Custodian:
    custodian_id: str
    name: str
    role: str
    center_code: str
    public_key: str
    private_key: Optional[str] = None  # None when stored in public directory

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d.pop("private_key", None)
        return d


@dataclass
class QuestionPaper:
    paper_id: str
    course_code: str
    course_title: str
    exam_date: str
    duration_minutes: int
    max_marks: int
    instructions: List[str]
    sections: List[Dict[str, Any]]

    def render_plain_text(self) -> str:
        """Render readable plain text examination paper."""
        lines = [
            "=" * 70,
            f"EXAMINATION PAPER: {self.course_code} - {self.course_title.upper()}",
            f"Paper ID: {self.paper_id} | Date: {self.exam_date} | Duration: {self.duration_minutes} Mins | Max Marks: {self.max_marks}",
            "=" * 70,
            "\nINSTRUCTIONS TO CANDIDATES:",
        ]
        for idx, inst in enumerate(self.instructions, 1):
            lines.append(f"  {idx}. {inst}")

        for sec in self.sections:
            lines.append(f"\n--- {sec['title']} (Marks: {sec.get('marks', 'N/A')}) ---")
            for q_idx, q in enumerate(sec["questions"], 1):
                lines.append(f"  Q{q_idx}. {q['text']} [{q['marks']} Marks]")
        lines.append("=" * 70)
        return "\n".join(lines)


@dataclass
class AccessEvent:
    event_id: str
    timestamp: str
    paper_id: str
    copy_id: str
    action: str
    custodian_id: str
    custodian_pubkey: str
    location: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    signature: str = ""

    def payload_bytes(self) -> bytes:
        """Deterministic byte representation of fields that are signed."""
        payload = {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "paper_id": self.paper_id,
            "copy_id": self.copy_id,
            "action": self.action,
            "custodian_id": self.custodian_id,
            "custodian_pubkey": self.custodian_pubkey,
            "location": self.location,
            "metadata": self.metadata,
        }
        return canonical_json_bytes(payload)

    def compute_digest(self) -> str:
        """SHA-256 digest of payload."""
        return sha256_hex(self.payload_bytes())

    def sign(self, private_key_b64: str) -> None:
        """Sign this event using the custodian's private key."""
        self.signature = sign_message(private_key_b64, self.payload_bytes())

    def verify(self) -> bool:
        """Verify the signature against the custodian's public key."""
        if not self.signature:
            return False
        return verify_signature(self.custodian_pubkey, self.payload_bytes(), self.signature)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AccessEvent:
        return cls(**data)


@dataclass
class Block:
    index: int
    timestamp: str
    prev_hash: str
    events: List[AccessEvent]
    merkle_root: str = ""
    block_hash: str = ""

    def compute_merkle_root(self) -> str:
        digests = [e.compute_digest() for e in self.events]
        self.merkle_root = compute_merkle_root(digests)
        return self.merkle_root

    def header_bytes(self) -> bytes:
        header = {
            "index": self.index,
            "timestamp": self.timestamp,
            "prev_hash": self.prev_hash,
            "merkle_root": self.merkle_root,
        }
        return canonical_json_bytes(header)

    def compute_block_hash(self) -> str:
        if not self.merkle_root:
            self.compute_merkle_root()
        self.block_hash = sha256_hex(self.header_bytes())
        return self.block_hash

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "prev_hash": self.prev_hash,
            "merkle_root": self.merkle_root,
            "block_hash": self.block_hash,
            "events": [e.to_dict() for e in self.events],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Block:
        events = [AccessEvent.from_dict(e) for e in data["events"]]
        return cls(
            index=data["index"],
            timestamp=data["timestamp"],
            prev_hash=data["prev_hash"],
            events=events,
            merkle_root=data["merkle_root"],
            block_hash=data["block_hash"],
        )
