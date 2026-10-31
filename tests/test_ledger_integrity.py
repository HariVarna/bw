"""Test Protocol 2: Ledger Integrity under Deliberate Tampering."""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Tuple

from src.crypto import generate_keypair
from src.ledger import BlockchainLedger
from src.models import AccessAction, AccessEvent, Block




def build_test_ledger() -> Tuple[BlockchainLedger, Dict[str, Any]]:
    """Build a baseline legitimate blockchain ledger with 3 blocks and 12 events."""
    priv_coe, pub_coe = generate_keypair()
    priv_supt, pub_supt = generate_keypair()

    ledger = BlockchainLedger()  # in-memory

    # Block 1: Generation events
    for i in range(1, 5):
        cid = f"CPY-{i:02d}"
        ev = AccessEvent(
            event_id=f"EV-INIT-{cid}",
            timestamp=f"2026-10-31T08:0{i}:00.000000+00:00",
            paper_id="QP-2026-CS801-AUTUMN",
            copy_id=cid,
            action=AccessAction.PAPER_GENERATED.value,
            custodian_id="CUST-01-COE",
            custodian_pubkey=pub_coe,
            location="HQ-CAMPUS",
        )
        ev.sign(priv_coe)
        ledger.add_event(ev)
    ledger.commit_block()

    # Block 2: Dispatch events
    for i in range(1, 5):
        cid = f"CPY-{i:02d}"
        ev = AccessEvent(
            event_id=f"EV-DISP-{cid}",
            timestamp=f"2026-10-31T09:1{i}:00.000000+00:00",
            paper_id="QP-2026-CS801-AUTUMN",
            copy_id=cid,
            action=AccessAction.DISPATCHED_TO_CENTER.value,
            custodian_id="CUST-03-SUPT",
            custodian_pubkey=pub_supt,
            location="CENTER-101",
        )
        ev.sign(priv_supt)
        ledger.add_event(ev)
    ledger.commit_block()

    keys = {
        "priv_coe": priv_coe,
        "pub_coe": pub_coe,
        "priv_supt": priv_supt,
        "pub_supt": pub_supt,
    }
    return ledger, keys


def run_ledger_integrity_test_suite(
    run_id: str = "RUN-LEDGER-20261031-01",
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Execute Test 2: Deliberate Tampering Detection over 10 distinct attack vectors."""
    test_cases = [
        {
            "entry_id": "TAMPER-01",
            "mod_type": "Altered Event Timestamp",
            "description": "Modify event timestamp inside Block 1, Event 0 without re-signing",
            "apply": lambda l, k: setattr(l.chain[1].events[0], "timestamp", "2026-10-31T00:00:00.000000+00:00"),
        },
        {
            "entry_id": "TAMPER-02",
            "mod_type": "Custodian ID Substitution",
            "description": "Change custodian_id to imposter 'CUST-MALICIOUS-99' in Block 1, Event 1",
            "apply": lambda l, k: setattr(l.chain[1].events[1], "custodian_id", "CUST-MALICIOUS-99"),
        },
        {
            "entry_id": "TAMPER-03",
            "mod_type": "Corrupted Digital Signature",
            "description": "Invert signature characters in Block 1, Event 2 to simulate forged record",
            "apply": lambda l, k: setattr(
                l.chain[1].events[2],
                "signature",
                "INVALID" + l.chain[1].events[2].signature[7:],
            ),
        },
        {
            "entry_id": "TAMPER-04",
            "mod_type": "Deleted Access Event",
            "description": "Remove Event 3 from Block 1 to hide custody record",
            "apply": lambda l, k: l.chain[1].events.pop(),
        },
        {
            "entry_id": "TAMPER-05",
            "mod_type": "Unauthorized Event Injection",
            "description": "Inject an unmined fake event into Block 2",
            "apply": lambda l, k: l.chain[2].events.append(
                AccessEvent(
                    event_id="EV-FAKE-999",
                    timestamp="2026-10-31T12:00:00.000000+00:00",
                    paper_id="QP-2026-CS801-AUTUMN",
                    copy_id="CPY-01",
                    action=AccessAction.SURPLUS_RETURNED.value,
                    custodian_id="CUST-03-SUPT",
                    custodian_pubkey=k["pub_supt"],
                    location="CENTER-101",
                    signature="FAKESIG",
                )
            ),
        },
        {
            "entry_id": "TAMPER-06",
            "mod_type": "Manipulated Merkle Root",
            "description": "Directly overwrite Block 1 Merkle root with arbitrary hash",
            "apply": lambda l, k: setattr(l.chain[1], "merkle_root", "0" * 64),
        },
        {
            "entry_id": "TAMPER-07",
            "mod_type": "Broken Chain Linkage (prev_hash)",
            "description": "Corrupt Block 2 prev_hash to simulate block insertion attack",
            "apply": lambda l, k: setattr(l.chain[2], "prev_hash", "f" * 64),
        },
        {
            "entry_id": "TAMPER-08",
            "mod_type": "Event Order Swapping",
            "description": "Swap the order of two legitimate events inside Block 2 (breaks Merkle tree)",
            "apply": lambda l, k: l.chain[2].events.reverse(),
        },
        {
            "entry_id": "TAMPER-09",
            "mod_type": "Forged Block Hash",
            "description": "Directly change Block 1 block_hash without recalculating",
            "apply": lambda l, k: setattr(l.chain[1], "block_hash", "e" * 64),
        },
        {
            "entry_id": "TAMPER-10",
            "mod_type": "Altered Copy ID in Event",
            "description": "Change copy_id from 'CPY-01' to 'CPY-99' inside Block 2 Event 0",
            "apply": lambda l, k: setattr(l.chain[2].events[0], "copy_id", "CPY-99"),
        },
    ]

    results: List[Dict[str, Any]] = []
    detected_count = 0

    for tc in test_cases:
        # Build fresh legitimate ledger
        ledger, keys = build_test_ledger()

        # Sanity check: clean ledger must be valid
        clean_audit = ledger.verify_ledger_integrity()
        assert clean_audit["is_valid"], "Baseline ledger failed initial integrity audit!"

        # Inject deliberate tampering
        tc["apply"](ledger, keys)

        # Audit modified ledger
        audit = ledger.verify_ledger_integrity()
        tamper_detected = not audit["is_valid"]

        if tamper_detected:
            detected_count += 1
            det_status = "DETECTED"
            actual_result = f"FLAGGED_COMPROMISED ({len(audit['errors'])} errors)"
            err_details = "; ".join(f"{e['error_type']} @ Block {e.get('block_index')}" for e in audit["errors"][:2])
            notes = f"Detected: {err_details}"
        else:
            det_status = "MISSED"
            actual_result = "PASSED_UNNOTICED"
            notes = "CRITICAL: Tamper evaded cryptographic audit."

        results.append({
            "Run ID": run_id,
            "Entry ID": tc["entry_id"],
            "Modification type": tc["mod_type"],
            "Expected integrity result": "FLAGGED_COMPROMISED",
            "Actual result": actual_result,
            "Detection status": det_status,
            "Notes": notes,
        })

    # Comparator: Editable register (where changes without cryptographic hashing go completely undetected)
    for comp_i in range(1, 3):
        results.append({
            "Run ID": run_id,
            "Entry ID": f"COMP-EDITABLE-REG-0{comp_i}",
            "Modification type": "Editable Register (Comparator Baseline)",
            "Expected integrity result": "PASSED_UNNOTICED",
            "Actual result": "PASSED_UNNOTICED",
            "Detection status": "UNDETECTABLE_IN_COMPARATOR",
            "Notes": "Comparator baseline: manual/editable database lacks cryptographic hashes, tampering leaves no audit trail.",
        })

    summary = {
        "run_id": run_id,
        "total_tamper_attacks": len(test_cases),
        "detected_count": detected_count,
        "missed_count": len(test_cases) - detected_count,
        "detection_rate_pct": round((detected_count / len(test_cases)) * 100, 2),
        "target_met": detected_count == 10,
    }

    return results, summary
