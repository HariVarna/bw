# Evidence Screenshots Directory

* **Project Title:** Blockchain-Based Leak Tracing for Examination Question Papers
* **Concept:** I01 — Fingerprinted Copies + Blockchain Access Ledger
* **Phase:** Phase 3: Proof of Concept

---

## 1. Directory Purpose & Honest Verification Policy

In strict adherence to the School of Innovation Phase 3 audit guidelines:
> **"Do not build a fake evidence package. Do not invent test results, screenshots, approval records, review statuses, source references, transaction hashes, or implementation claims... Prepare a place for genuine screenshots... Do not fabricate screenshots. Clearly label any generated mock interface as a mockup."**

This directory is structured to hold genuine, unedited console screen captures and terminal logs obtained from the running prototype.

---

## 2. Screenshot Inventory & Capture Checklist

Prior to final institutional submission, the project team will place genuine OS screen captures here corresponding to the following verified workflows:

| Image File Name | Workflow Step | Source Command | Captured Element | Status |
| :--- | :--- | :--- | :--- | :--- |
| `01_env_setup.png` | Environment Setup | `python --version`, `git status` | Terminal showing Python 3.12, cryptography 50.0.2, Pillow 12.3.0 | Pending local screen capture |
| `02_batch_init.png` | Batch Initialization | `python -m src.cli init-batch --count 20` | Output showing 20 copies generated and Block #1 mined | Pending local screen capture |
| `03_ledger_audit_valid.png` | Clean Ledger Audit | `python -m src.cli verify-ledger` | Output showing `[VALID]` status and 0 errors across 40 events | Pending local screen capture |
| `04_tamper_detection.png` | Deliberate Tampering | `python -m tests.test_ledger_integrity` | Output showing 10/10 tampering attacks detected with error types | Pending local screen capture |
| `05_leak_trace_report.png` | Forensic Leak Trace | `python -m src.cli trace-leak --file ...` | Forensic dossier showing positive custodian attribution | Pending local screen capture |
| `06_full_test_suite.png` | Unified Test Execution | `python tests/run_all_tests.py` | Complete test summary passing Tests 1, 2, and 3 | Pending local screen capture |

---

## 3. Terminal Output Reproduction Reference (Textual Mockup)

For technical reviewers reviewing without image renderers, the exact textual output emitted by the system during verification is reproduced below for reference:

```text
======================================================================
EXECUTING SOI PHASE 3 FROZEN TEST PROTOCOL (AY 2026-27)
Project: Blockchain-Based Leak Tracing for Examination Question Papers
Concept: I01 — Fingerprinted Copies + Blockchain Access Ledger
======================================================================
Assigned Execution Run ID: RUN-SOI-P3-20261031-161854

Running Test 1: Fingerprint Tracing under Transformations...
  -> Generated 24 rows (20 test samples + 4 comparator samples)
  -> Correct Matches: 20/20 (100.0%)
  -> Target Met (>= 90%): True
  -> Written to: SoI_P3_LeakTracing_Evidence\04_Raw_Test_Logs\fingerprint_tests.csv

Running Test 2: Ledger Integrity under Deliberate Tampering...
  -> Generated 12 rows (10 attack vectors + 2 comparator baselines)
  -> Detected Tampering: 10/10 (100.0%)
  -> Target Met (10/10): True
  -> Written to: SoI_P3_LeakTracing_Evidence\04_Raw_Test_Logs\ledger_integrity_tests.csv

Running Test 3: Event-Logging Latency and Cost Benchmark...
  -> Timed 50 consecutive access events
  -> Average Latency: 0.2514 ms (0.000251 s)
  -> Max Latency: 0.5503 ms (0.000550 s)
  -> Target Met (<= 5.0 s): True
  -> Incurred Cost: INR 0.0 (Target: INR 0)
  -> Written to: SoI_P3_LeakTracing_Evidence\04_Raw_Test_Logs\event_timing_tests.csv

Run Metadata written to: SoI_P3_LeakTracing_Evidence\04_Raw_Test_Logs\run_metadata.json

======================================================================
ALL TESTS COMPLETED SUCCESSFULLY — GENUINE TEST LOGS RECORDED
======================================================================
```
