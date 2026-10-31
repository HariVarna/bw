"""Demo Service: Orchestrates automated seeding and reset of institutional demonstration dataset."""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.models import AccessAction, AccessEvent
from webapp.database import get_db_connection, log_activity
from webapp.services.access_ledger_service import AccessLedgerService
from webapp.services.custodian_service import CustodianService
from webapp.services.examination_service import ExaminationService
from webapp.services.fingerprint_service import COPIES_DIR, FingerprintService
from webapp.services.tracing_service import TracingService

SAMPLES_DIR = ROOT_DIR / "webapp" / "static" / "samples"


class DemoService:
    @classmethod
    def is_demo_seeded(cls) -> bool:
        """Check if demonstration data currently exists in the database."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            count = cursor.execute("SELECT COUNT(*) FROM examinations WHERE is_demo = 1").fetchone()[0]
            return count > 0

    @classmethod
    def seed_demo_data(cls) -> Dict[str, Any]:
        """Seed complete institutional examination lifecycle demonstration data."""
        # 1. Reset any existing demo data first to guarantee determinism
        cls.reset_demo_data()

        # 2. Register Master Examination
        paper_id = "QP-2026-CS801-AUTUMN"
        exam = ExaminationService.create_synthetic_examination(paper_id=paper_id, is_demo=True)

        # 3. Register Custodians with Ed25519 Keypairs
        demo_custodians = [
            {"id": "CUST-01-COE", "name": "Prof. R. Narayanan", "role": "Controller of Examinations", "center": "HQ-CAMPUS"},
            {"id": "CUST-02-PRINT", "name": "V. Senthil Kumar", "role": "Confidential Printing Officer", "center": "PRESS-VAULT"},
            {"id": "CUST-03-SUPT", "name": "Dr. Ananya Sharma", "role": "Chief Superintendent Hall A", "center": "CENTER-101"},
            {"id": "CUST-04-SUPT", "name": "Prof. K. Rajendran", "role": "Chief Superintendent Hall B", "center": "CENTER-102"},
        ]

        custodian_objs: Dict[str, Dict[str, Any]] = {}
        for c in demo_custodians:
            custodian_objs[c["id"]] = CustodianService.register_custodian(
                custodian_id=c["id"],
                name=c["name"],
                role=c["role"],
                center_code=c["center"],
                is_demo=True,
            )

        # 4. Generate 8 Multi-Layer Fingerprinted Copies
        base_text = exam["raw_text"]
        generated_copies = []
        for i in range(1, 9):
            assigned_custodian_id = demo_custodians[(i - 1) % len(demo_custodians)]["id"]
            copy_rec = FingerprintService.generate_copy_record(
                paper_id=paper_id,
                base_text=base_text,
                copy_idx=i,
                custodian_id=assigned_custodian_id,
                is_demo=True,
            )
            generated_copies.append(copy_rec)

        # 5. Build Cryptographic Blockchain Ledger with Signed Events
        ledger = AccessLedgerService.get_ledger()
        ledger.chain = []
        ledger.pending_events = []
        ledger.create_genesis_block()

        # Block 1: Generation events signed by COE
        coe_priv = custodian_objs["CUST-01-COE"]["private_key"]
        coe_pub = custodian_objs["CUST-01-COE"]["public_key"]

        for i in range(1, 9):
            cid = f"CPY-{i:02d}"
            ev = AccessEvent(
                event_id=f"EV-GEN-{cid}",
                timestamp=f"2026-10-31T08:{i:02d}:00.000000+00:00",
                paper_id=paper_id,
                copy_id=cid,
                action=AccessAction.PAPER_GENERATED.value,
                custodian_id="CUST-01-COE",
                custodian_pubkey=coe_pub,
                location="HQ-CAMPUS",
                metadata={"batch": "2026-AUTUMN-DEMO", "serial": i},
            )
            ev.sign(coe_priv)
            ledger.add_event(ev)

        block_1 = ledger.commit_block()

        # Block 2: Dispatch and Receipt events signed by assigned custodians
        for i in range(1, 9):
            cid = f"CPY-{i:02d}"
            assigned_c = demo_custodians[(i - 1) % len(demo_custodians)]
            c_priv = custodian_objs[assigned_c["id"]]["private_key"]
            c_pub = custodian_objs[assigned_c["id"]]["public_key"]

            # Dispatch
            ev_disp = AccessEvent(
                event_id=f"EV-DISP-{cid}",
                timestamp=f"2026-10-31T09:{i+10:02d}:00.000000+00:00",
                paper_id=paper_id,
                copy_id=cid,
                action=AccessAction.DISPATCHED_TO_CENTER.value,
                custodian_id=assigned_c["id"],
                custodian_pubkey=c_pub,
                location=assigned_c["center"],
                metadata={"courier_seal": f"SEAL-DEMO-{i:03d}"},
            )
            ev_disp.sign(c_priv)
            ledger.add_event(ev_disp)

            # Center receipt / vault deposit
            ev_vault = AccessEvent(
                event_id=f"EV-VAULT-{cid}",
                timestamp=f"2026-10-31T10:{i+15:02d}:00.000000+00:00",
                paper_id=paper_id,
                copy_id=cid,
                action=AccessAction.VAULT_DEPOSITED.value,
                custodian_id=assigned_c["id"],
                custodian_pubkey=c_pub,
                location=assigned_c["center"],
                metadata={"vault_box": f"VB-SEC-{assigned_c['center']}"},
            )
            ev_vault.sign(c_priv)
            ledger.add_event(ev_vault)

        block_2 = ledger.commit_block()

        # 6. Create Pre-Packaged Sample Files for user experimentation
        SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

        # Sample 1: Direct digital leak of CPY-03 (Contains invisible zero-width unicode)
        cpy3_path = COPIES_DIR / "CPY-03.txt"
        if cpy3_path.exists():
            (SAMPLES_DIR / "leak_sample_digital_copy3.txt").write_text(
                cpy3_path.read_text(encoding="utf-8"), encoding="utf-8"
            )

        # Sample 2: Retyped snippet of CPY-02 (Zero-width stripped, preserves syntactic variations)
        cpy2_path = COPIES_DIR / "CPY-02.txt"
        if cpy2_path.exists():
            raw_c2 = cpy2_path.read_text(encoding="utf-8")
            retyped_c2 = "".join(ch for ch in raw_c2 if ch not in "\u200b\u200c\u200d")
            (SAMPLES_DIR / "leak_sample_retyped_copy2.txt").write_text(
                retyped_c2, encoding="utf-8"
            )

        # Sample 3: Image copy of CPY-01 (PNG with corner grid)
        cpy1_img = COPIES_DIR / "CPY-01.png"
        if cpy1_img.exists():
            shutil.copy(str(cpy1_img), str(SAMPLES_DIR / "leak_sample_image_copy1.png"))

        # 7. Seed Initial Demonstration Leak Investigation Dossiers
        sample1_text = (SAMPLES_DIR / "leak_sample_digital_copy3.txt").read_text(encoding="utf-8")
        TracingService.investigate(
            sample_text=sample1_text,
            filename="leak_sample_digital_copy3.txt",
            is_demo=True,
        )

        sample2_text = (SAMPLES_DIR / "leak_sample_retyped_copy2.txt").read_text(encoding="utf-8")
        TracingService.investigate(
            sample_text=sample2_text,
            filename="leak_sample_retyped_copy2.txt",
            is_demo=True,
        )

        log_activity(
            action_type="SEED_DEMO_DATASET",
            details="Successfully initialized institutional demonstration dataset (1 Exam, 4 Custodians, 8 Fingerprinted Copies, 2 Blocks / 24 Events, 2 Sample Investigations).",
            status="SUCCESS",
        )

        return {
            "status": "success",
            "message": "Institutional demonstration dataset loaded successfully.",
            "examinations": 1,
            "custodians": len(demo_custodians),
            "copies": len(generated_copies),
            "blocks": len(ledger.chain),
            "events": sum(len(b.events) for b in ledger.chain),
        }

    @classmethod
    def reset_demo_data(cls) -> Dict[str, Any]:
        """Reset and wipe demonstration records cleanly."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM investigations WHERE is_demo = 1")
            cursor.execute("DELETE FROM fingerprinted_copies WHERE is_demo = 1")
            cursor.execute("DELETE FROM custodians WHERE is_demo = 1")
            cursor.execute("DELETE FROM examinations WHERE is_demo = 1")
            conn.commit()

        # Reset ledger
        ledger = AccessLedgerService.get_ledger()
        ledger.chain = []
        ledger.pending_events = []
        ledger.create_genesis_block()

        log_activity(
            action_type="RESET_DEMO_DATASET",
            details="Reset institutional demonstration dataset to clean baseline.",
            status="SUCCESS",
        )

        return {"status": "success", "message": "Demonstration data reset successfully."}
