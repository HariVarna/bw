"""Command Line Interface for Blockchain-Based Question Paper Leak Tracing."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

from .crypto import generate_keypair
from .fingerprint import apply_fingerprint_to_text, derive_syntactic_vector, render_paper_image
from .leak_tracer import LeakTracer
from .ledger import BlockchainLedger
from .models import AccessAction, AccessEvent, Custodian
from .paper_generator import generate_synthetic_question_paper


def cmd_init_batch(args: argparse.Namespace) -> None:
    """Initialize synthetic exam question paper, generate copies, and log custody events."""
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    copies_dir = out_dir / "copies"
    copies_dir.mkdir(parents=True, exist_ok=True)
    ledger_file = out_dir / "ledger.json"

    paper = generate_synthetic_question_paper(args.paper_id)
    base_text = paper.render_plain_text()

    # Save base paper
    (out_dir / "master_question_paper.txt").write_text(base_text, encoding="utf-8")

    # Generate synthetic custodians
    custodians = [
        {"id": "CUST-01-COE", "name": "Controller of Examinations", "role": "COE", "center": "HQ-CAMPUS"},
        {"id": "CUST-02-PRINT", "name": "Confidential Printing Officer", "role": "PRINTER", "center": "PRESS-VAULT"},
        {"id": "CUST-03-SUPT", "name": "Chief Superintendent Hall A", "role": "SUPERINTENDENT", "center": "CENTER-101"},
        {"id": "CUST-04-SUPT", "name": "Chief Superintendent Hall B", "role": "SUPERINTENDENT", "center": "CENTER-102"},
    ]

    custodian_objs: dict[str, Custodian] = {}
    for c in custodians:
        priv, pub = generate_keypair()
        custodian_objs[c["id"]] = Custodian(
            custodian_id=c["id"],
            name=c["name"],
            role=c["role"],
            center_code=c["center"],
            public_key=pub,
            private_key=priv,
        )

    # Initialize blockchain ledger
    ledger = BlockchainLedger(str(ledger_file))
    manifest: dict[str, dict] = {}

    num_copies = args.count
    print(f"Generating {num_copies} fingerprinted question paper copies...")

    for i in range(1, num_copies + 1):
        copy_id = f"CPY-{i:02d}"
        assigned_custodian_id = custodians[(i - 1) % len(custodians)]["id"]
        custodian = custodian_objs[assigned_custodian_id]

        fp_text = apply_fingerprint_to_text(base_text, copy_id, i, args.paper_id)
        text_path = copies_dir / f"{copy_id}.txt"
        text_path.write_text(fp_text, encoding="utf-8")

        # Render visual image for visual tracking
        img = render_paper_image(fp_text, copy_id)
        img_path = copies_dir / f"{copy_id}.png"
        img.save(img_path)

        manifest[copy_id] = {
            "copy_id": copy_id,
            "custodian_id": assigned_custodian_id,
            "text_file": str(text_path.name),
            "image_file": str(img_path.name),
            "syntactic_vector": derive_syntactic_vector(i),
        }

        # Log custody creation event
        ev = AccessEvent(
            event_id=f"EV-GEN-{copy_id}",
            timestamp="2026-10-31T08:00:00.000000+00:00",
            paper_id=args.paper_id,
            copy_id=copy_id,
            action=AccessAction.PAPER_GENERATED.value,
            custodian_id="CUST-01-COE",
            custodian_pubkey=custodian_objs["CUST-01-COE"].public_key,
            location="HQ-CAMPUS",
            metadata={"batch": "2026-AUTUMN", "serial": i},
        )
        ev.sign(custodian_objs["CUST-01-COE"].private_key)
        ledger.add_event(ev)

        # Log custody dispatch event
        ev_disp = AccessEvent(
            event_id=f"EV-DISP-{copy_id}",
            timestamp="2026-10-31T09:30:00.000000+00:00",
            paper_id=args.paper_id,
            copy_id=copy_id,
            action=AccessAction.DISPATCHED_TO_CENTER.value,
            custodian_id=assigned_custodian_id,
            custodian_pubkey=custodian.public_key,
            location=custodian.center_code,
            metadata={"courier_seal": f"SEAL-882-{i}"},
        )
        ev_disp.sign(custodian.private_key)
        ledger.add_event(ev_disp)

    # Commit events into a new block
    block = ledger.commit_block()
    print(f"Block #{block.index} committed with {len(block.events)} events. Merkle Root: {block.merkle_root[:16]}...")

    # Save manifest and public keys
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    pubkeys = {cid: c.to_dict() for cid, c in custodian_objs.items()}
    (out_dir / "custodians.json").write_text(json.dumps(pubkeys, indent=2), encoding="utf-8")

    print(f"Batch setup complete. Artifacts saved to: {out_dir}")


def cmd_verify_ledger(args: argparse.Namespace) -> None:
    """Audit blockchain ledger cryptographic integrity."""
    ledger = BlockchainLedger(args.ledger_file)
    audit = ledger.verify_ledger_integrity()

    print("\n" + "=" * 60)
    print("BLOCKCHAIN ACCESS LEDGER CRYPTOGRAPHIC AUDIT REPORT")
    print("=" * 60)
    print(f"Status:        {'[VALID]' if audit['is_valid'] else '[COMPROMISED]'}")
    print(f"Total Blocks:  {audit['total_blocks']}")
    print(f"Total Events:  {audit['total_events']}")
    print(f"Errors Found:  {len(audit['errors'])}")

    if audit["errors"]:
        print("\nTAMPERING DETECTED:")
        for err in audit["errors"]:
            print(f"  - Block {err.get('block_index')}: {err.get('error_type')} -> {err.get('details')}")
    else:
        print("\nAll hash-chain linkages, Merkle roots, and Ed25519 signatures verified.")
    print("=" * 60)


def cmd_trace_leak(args: argparse.Namespace) -> None:
    """Trace a recovered leaked file back to the responsible custodian."""
    ledger = BlockchainLedger(args.ledger_file)

    manifest = {}
    if args.manifest and Path(args.manifest).exists():
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))

    tracer = LeakTracer(ledger, manifest)

    sample_path = Path(args.file)
    sample_text = None
    sample_img = None

    if sample_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
        sample_img = Image.open(sample_path)
    else:
        sample_text = sample_path.read_text(encoding="utf-8", errors="ignore")

    report = tracer.trace_leak(sample_text=sample_text, sample_image=sample_img)

    print("\n" + "=" * 65)
    print("FORENSIC LEAK INVESTIGATION REPORT")
    print("=" * 65)
    print(f"Sample File:         {sample_path.name}")
    print(f"Sample Type:         {report.sample_type}")
    print(f"Detected Copy ID:    {report.detected_copy_id or 'NONE'}")
    print(f"Detection Layer:     {report.detection_layer or 'NONE'}")
    print(f"Attribution Status:  {report.detection_status}")
    print(f"Confidence Score:    {report.confidence_score * 100:.1f}%")
    print("-" * 65)
    print(f"Custody Events:      {report.custody_events_count}")
    print(f"Last Custodian ID:   {report.last_known_custodian_id or 'UNKNOWN'}")
    print(f"Last Location:       {report.last_known_location or 'UNKNOWN'}")
    print(f"Last Action:         {report.last_action or 'UNKNOWN'}")
    print(f"Timestamp:           {report.last_timestamp or 'UNKNOWN'}")
    print("-" * 65)
    print(f"Conclusion: {report.investigative_conclusion}")
    print("=" * 65)


def main() -> None:
    parser = argparse.ArgumentParser(description="Blockchain-Based Leak Tracing CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init-batch
    p_init = subparsers.add_parser("init-batch", help="Generate synthetic paper copies and ledger")
    p_init.add_argument("--paper-id", default="QP-2026-CS801-AUTUMN", help="Paper ID")
    p_init.add_argument("--count", type=int, default=20, help="Number of copies to generate")
    p_init.add_argument("--output-dir", default="data_poc", help="Output directory")

    # verify-ledger
    p_verify = subparsers.add_parser("verify-ledger", help="Verify ledger integrity")
    p_verify.add_argument("--ledger-file", default="data_poc/ledger.json", help="Ledger JSON file")

    # trace-leak
    p_trace = subparsers.add_parser("trace-leak", help="Trace a leaked snippet")
    p_trace.add_argument("--file", required=True, help="Path to leaked snippet or image")
    p_trace.add_argument("--ledger-file", default="data_poc/ledger.json", help="Ledger JSON file")
    p_trace.add_argument("--manifest", default="data_poc/manifest.json", help="Manifest JSON file")

    args = parser.parse_args()
    if args.command == "init-batch":
        cmd_init_batch(args)
    elif args.command == "verify-ledger":
        cmd_verify_ledger(args)
    elif args.command == "trace-leak":
        cmd_trace_leak(args)


if __name__ == "__main__":
    main()
