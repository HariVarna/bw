"""Test Protocol 3: Event-Logging Time and Cost Benchmark."""

from __future__ import annotations

import statistics
import time
from typing import Any, Dict, List, Tuple

from src.crypto import generate_keypair
from src.ledger import BlockchainLedger
from src.models import AccessAction, AccessEvent


def run_event_timing_test_suite(
    num_events: int = 50,
    run_id: str = "RUN-TIMING-20261031-01",
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Execute Test 3: Benchmark latency and compute cost across 50 logged custody events."""
    priv_key, pub_key = generate_keypair()
    ledger = BlockchainLedger()  # in-memory ledger

    results: List[Dict[str, Any]] = []
    elapsed_times_ms: List[float] = []
    failed_ops = 0

    actions = [
        AccessAction.PAPER_GENERATED.value,
        AccessAction.DISPATCHED_TO_CENTER.value,
        AccessAction.RECEIVED_AT_CENTER.value,
        AccessAction.VAULT_DEPOSITED.value,
        AccessAction.SEAL_VERIFIED.value,
        AccessAction.EXAM_HALL_TRANSFERRED.value,
        AccessAction.DISTRIBUTED_TO_STUDENT.value,
        AccessAction.SURPLUS_RETURNED.value,
    ]

    for i in range(1, num_events + 1):
        event_num = f"EV-LOG-{i:03d}"
        action = actions[(i - 1) % len(actions)]
        cid = f"CPY-{(i % 20) + 1:02d}"

        # High-precision timer start
        t0 = time.perf_counter_ns()

        # Step 1: Create event
        ev = AccessEvent(
            event_id=f"EV-BENCH-{i:04d}",
            timestamp="2026-10-31T10:00:00.000000+00:00",
            paper_id="QP-2026-CS801-AUTUMN",
            copy_id=cid,
            action=action,
            custodian_id=f"CUST-OFFICER-{(i % 5) + 1:02d}",
            custodian_pubkey=pub_key,
            location=f"CENTER-{(i % 4) + 101}",
            metadata={"batch_seq": i, "seal_code": f"SEAL-SLOT-{i}"},
        )

        # Step 2: Ed25519 digital signature
        ev.sign(priv_key)

        # Step 3: Signature verification and ledger addition
        ok, msg = ledger.add_event(ev, verify_sig=True)

        t1 = time.perf_counter_ns()
        elapsed_ms = (t1 - t0) / 1_000_000.0
        elapsed_times_ms.append(elapsed_ms)

        outcome = "SUCCESS" if ok else "FAILED"
        if not ok:
            failed_ops += 1

        results.append({
            "Run ID": run_id,
            "Event number": event_num,
            "Operation": f"Construct + Ed25519 Sign + Verify + Ledger Ingest ({action})",
            "Start/end or elapsed time": f"{elapsed_ms:.4f}",
            "Unit": "milliseconds",
            "Outcome": outcome,
            "Notes": f"Target <= 5000 ms (5s). Incurred cost: ₹0 (Local permissioned ledger).",
        })

    # Commit block containing the 50 events
    t_commit_0 = time.perf_counter_ns()
    block = ledger.commit_block()
    t_commit_1 = time.perf_counter_ns()
    commit_elapsed_ms = (t_commit_1 - t_commit_0) / 1_000_000.0

    avg_ms = statistics.mean(elapsed_times_ms)
    median_ms = statistics.median(elapsed_times_ms)
    max_ms = max(elapsed_times_ms)
    min_ms = min(elapsed_times_ms)

    avg_s = avg_ms / 1000.0
    max_s = max_ms / 1000.0

    summary = {
        "run_id": run_id,
        "events_tested": num_events,
        "failed_operations": failed_ops,
        "avg_event_time_ms": round(avg_ms, 4),
        "median_event_time_ms": round(median_ms, 4),
        "min_event_time_ms": round(min_ms, 4),
        "max_event_time_ms": round(max_ms, 4),
        "avg_event_time_sec": round(avg_s, 6),
        "max_event_time_sec": round(max_s, 6),
        "block_commit_time_ms": round(commit_elapsed_ms, 4),
        "target_time_sec": 5.0,
        "target_cost_inr": 0.0,
        "actual_cost_inr": 0.0,
        "target_met": (max_s <= 5.0) and (failed_ops == 0),
        "comparator_baseline_desc": "Manual paper register entry: 30 to 60 seconds per custody transition.",
    }

    return results, summary
