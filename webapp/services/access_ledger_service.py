"""Access Ledger Service: Integrates the cryptographic blockchain ledger with web workflows."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.crypto import generate_keypair
from src.ledger import BlockchainLedger
from src.models import AccessAction, AccessEvent, Block
from webapp.database import log_activity

LEDGER_PATH = ROOT_DIR / "webapp" / "instance" / "ledger.json"


class AccessLedgerService:
    @staticmethod
    def get_ledger() -> BlockchainLedger:
        """Load or create the single instance of the blockchain ledger."""
        LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        return BlockchainLedger(str(LEDGER_PATH))

    @classmethod
    def verify_ledger(cls) -> Dict[str, Any]:
        """Perform comprehensive cryptographic audit of the blockchain ledger."""
        ledger = cls.get_ledger()
        result = ledger.verify_ledger_integrity()
        status_str = "VALID" if result["is_valid"] else "COMPROMISED"
        log_activity(
            action_type="LEDGER_CRYPTOGRAPHIC_AUDIT",
            details=f"Audited {result['total_blocks']} blocks ({result['total_events']} events). Status: {status_str}.",
            status="SUCCESS" if result["is_valid"] else "ALERT",
        )
        return result

    @classmethod
    def get_blocks(cls) -> List[Dict[str, Any]]:
        """Retrieve all blocks in reverse chronological order."""
        ledger = cls.get_ledger()
        blocks = [b.to_dict() for b in reversed(ledger.chain)]
        return blocks

    @classmethod
    def get_all_events(cls) -> List[Dict[str, Any]]:
        """Retrieve all events across all blocks in reverse chronological order."""
        ledger = cls.get_ledger()
        all_events: List[Dict[str, Any]] = []
        for b in reversed(ledger.chain):
            for e in reversed(b.events):
                event_dict = e.to_dict()
                event_dict["block_index"] = b.index
                event_dict["signature_valid"] = e.verify()
                all_events.append(event_dict)
        return all_events

    @classmethod
    def get_events_for_copy(cls, copy_id: str) -> List[Dict[str, Any]]:
        """Retrieve full verified chain of custody for a specific copy ID."""
        ledger = cls.get_ledger()
        events = ledger.get_events_for_copy(copy_id)
        events.sort(key=lambda e: e.timestamp)
        return [
            {
                **e.to_dict(),
                "signature_valid": e.verify(),
            }
            for e in events
        ]

    @classmethod
    def get_ledger_stats(cls) -> Dict[str, Any]:
        """Return ledger aggregate metrics and health status."""
        ledger = cls.get_ledger()
        total_blocks = len(ledger.chain)
        total_events = sum(len(b.events) for b in ledger.chain)
        pending_count = len(ledger.pending_events)
        
        # Verify integrity
        audit = ledger.verify_ledger_integrity()

        return {
            "total_blocks": total_blocks,
            "total_events": total_events,
            "pending_events": pending_count,
            "latest_block_hash": ledger.latest_block.block_hash if ledger.chain else "N/A",
            "is_valid": audit["is_valid"],
            "error_count": len(audit["errors"]),
        }
