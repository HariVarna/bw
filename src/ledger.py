"""Cryptographic Blockchain Access Ledger for Custody Events.

Implements an append-only, Merkle-backed cryptographic ledger.
Supports event signing, block creation, persistent storage, and rigorous
cryptographic auditing (hash chain verification, Merkle root verification,
and Ed25519 signature validation).
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .crypto import compute_merkle_root, sha256_hex
from .models import AccessEvent, Block


class BlockchainLedger:
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = Path(storage_path) if storage_path else None
        self.chain: List[Block] = []
        self.pending_events: List[AccessEvent] = []

        if self.storage_path and self.storage_path.exists():
            self.load_from_disk()
        else:
            self.create_genesis_block()

    def create_genesis_block(self) -> Block:
        """Create and append the immutable genesis block."""
        genesis_block = Block(
            index=0,
            timestamp="2026-10-31T00:00:00.000000+00:00",
            prev_hash="0" * 64,
            events=[],
            merkle_root=sha256_hex(b"GENESIS_SEED_LEAK_TRACING_2026"),
        )
        genesis_block.block_hash = sha256_hex(genesis_block.header_bytes())
        self.chain = [genesis_block]
        self._auto_save()
        return genesis_block

    @property
    def latest_block(self) -> Block:
        return self.chain[-1]

    def add_event(self, event: AccessEvent, verify_sig: bool = True) -> Tuple[bool, str]:
        """Validate and queue an access event for inclusion in the next block."""
        if verify_sig:
            if not event.verify():
                return False, f"Event {event.event_id} signature verification failed."

        self.pending_events.append(event)
        return True, f"Event {event.event_id} queued successfully."

    def commit_block(self) -> Block:
        """Mine/commit pending events into a new cryptographic block."""
        prev = self.latest_block
        now_ts = datetime.now(timezone.utc).isoformat()

        new_block = Block(
            index=len(self.chain),
            timestamp=now_ts,
            prev_hash=prev.block_hash,
            events=list(self.pending_events),
        )
        new_block.compute_merkle_root()
        new_block.compute_block_hash()

        self.chain.append(new_block)
        self.pending_events = []
        self._auto_save()
        return new_block

    def verify_ledger_integrity(self) -> Dict[str, Any]:
        """Perform comprehensive cryptographic audit of the entire blockchain."""
        errors: List[Dict[str, Any]] = []
        total_events = sum(len(b.events) for b in self.chain)

        # 1. Audit Genesis Block
        if not self.chain:
            return {"is_valid": False, "total_blocks": 0, "total_events": 0, "errors": [{"type": "EMPTY_CHAIN"}]}

        genesis = self.chain[0]
        if genesis.index != 0 or genesis.prev_hash != "0" * 64:
            errors.append({
                "block_index": 0,
                "error_type": "CORRUPT_GENESIS_LINK",
                "details": f"Index {genesis.index}, prev_hash {genesis.prev_hash}",
            })

        # 2. Audit Chain Sequence, Hashes, Merkle Roots, and Event Signatures
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]

            # Sequence check
            if curr.index != i:
                errors.append({
                    "block_index": i,
                    "error_type": "INVALID_BLOCK_SEQUENCE",
                    "details": f"Expected index {i}, found {curr.index}",
                })

            # Previous hash link check
            if curr.prev_hash != prev.block_hash:
                errors.append({
                    "block_index": i,
                    "error_type": "BROKEN_HASH_LINK",
                    "details": f"Expected prev_hash {prev.block_hash}, found {curr.prev_hash}",
                })

            # Merkle root verification
            event_digests = [e.compute_digest() for e in curr.events]
            recalculated_merkle = compute_merkle_root(event_digests)
            if curr.merkle_root != recalculated_merkle:
                errors.append({
                    "block_index": i,
                    "error_type": "MERKLE_ROOT_MISMATCH",
                    "details": f"Stored Merkle root {curr.merkle_root} != computed {recalculated_merkle}",
                })

            # Block hash verification
            recalculated_block_hash = sha256_hex(curr.header_bytes())
            if curr.block_hash != recalculated_block_hash:
                errors.append({
                    "block_index": i,
                    "error_type": "BLOCK_HASH_MISMATCH",
                    "details": f"Stored block hash {curr.block_hash} != computed {recalculated_block_hash}",
                })

            # Event-level signature verification
            for e_idx, event in enumerate(curr.events):
                if not event.verify():
                    errors.append({
                        "block_index": i,
                        "event_index": e_idx,
                        "event_id": event.event_id,
                        "error_type": "INVALID_EVENT_SIGNATURE",
                        "details": f"Signature invalid for event {event.event_id} signed by {event.custodian_id}",
                    })

        return {
            "is_valid": len(errors) == 0,
            "total_blocks": len(self.chain),
            "total_events": total_events,
            "errors": errors,
        }

    def get_events_for_copy(self, copy_id: str) -> List[AccessEvent]:
        """Retrieve complete historical custody trail for a specific copy ID."""
        matching: List[AccessEvent] = []
        for b in self.chain:
            for e in b.events:
                if e.copy_id == copy_id:
                    matching.append(e)
        return matching

    def to_dict(self) -> Dict[str, Any]:
        return {
            "blocks": [b.to_dict() for b in self.chain],
            "pending": [e.to_dict() for e in self.pending_events],
        }

    def save_to_disk(self, path: Optional[str] = None) -> None:
        target = Path(path) if path else self.storage_path
        if not target:
            return
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    def load_from_disk(self) -> None:
        if not self.storage_path or not self.storage_path.exists():
            return
        with open(self.storage_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.chain = [Block.from_dict(b) for b in data.get("blocks", [])]
        self.pending_events = [AccessEvent.from_dict(e) for e in data.get("pending", [])]

    def _auto_save(self) -> None:
        if self.storage_path:
            self.save_to_disk()
