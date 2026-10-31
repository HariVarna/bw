# Replay & Reproducibility Runbook

* **Project Title:** Blockchain-Based Leak Tracing for Examination Question Papers
* **Concept:** I01 — Fingerprinted Copies + Blockchain Access Ledger
* **Artifact Version:** `v0.3.0-poc` (Git Commit: `d40487ae9053fe7cfc280328a076b03646011763`)
* **Target Audience:** Phase 3 Technical Reviewers and Academic Auditors

---

## 1. Project Overview

This prototype demonstrates a cryptographically auditable custody system for university examination question papers. When a confidential paper is generated, distinct copies receive multi-layer fingerprints (invisible zero-width steganography, syntactic variations, and visual micro-patterns). Physical and digital custody transitions are signed with Ed25519 asymmetric keys and committed to an append-only, Merkle-backed blockchain ledger. If a leaked paper excerpt surfaces, the forensic engine extracts the fingerprint, queries the blockchain, and pinpoints the last verified custodian.

---

## 2. System Requirements

* **Operating System:** Windows 10/11, macOS 12+, or Ubuntu Linux 20.04+ (tested on Windows 11 Enterprise AMD64)
* **Processor:** 1.8 GHz dual-core x86_64 or ARM64
* **Memory (RAM):** Minimum 2 GB (4 GB recommended)
* **Disk Space:** Less than 100 MB for repository, virtual environment, and test logs
* **Network:** Offline capable after dependency installation (no internet connection required for testing or replay)

---

## 3. Prerequisites & Installation

Verify Python and Git are installed:

```powershell
python --version  # Requires Python 3.10, 3.11, or 3.12
git --version
```

Clone or open the workspace repository:

```powershell
cd e:\bw
```

Install the two required runtime dependencies:

```powershell
pip install cryptography==50.0.2 pillow==12.3.0
```

---

## 4. Configuration

No complex `.env` or external database configuration is required. The prototype defaults to:
* **Ledger File:** Local JSON append-only store (`data_poc/ledger.json` or custom path)
* **Signatures:** Ed25519 (RFC 8032)
* **Hashing:** SHA-256 (FIPS 180-4)

---

## 5. How to Run the Application (CLI Demonstration)

The CLI supports end-to-end operational workflows:

### Step 5.1: Initialize an Examination Batch
Generates a master question paper, creates 20 unique fingerprinted copies (both plain text and rendered PNGs), registers custodians, signs custody events, and mines them into block #1:

```powershell
python -m src.cli init-batch --paper-id QP-2026-CS801-AUTUMN --count 20 --output-dir demo_data
```

**Expected Console Output:**
```
Generating 20 fingerprinted question paper copies...
Block #1 committed with 40 events. Merkle Root: ...
Batch setup complete. Artifacts saved to: demo_data
```

### Step 5.2: Verify Blockchain Ledger Cryptographic Integrity
Runs the complete cryptographic audit across all blocks, Merkle roots, and Ed25519 signatures:

```powershell
python -m src.cli verify-ledger --ledger-file demo_data/ledger.json
```

**Expected Console Output:**
```
============================================================
BLOCKCHAIN ACCESS LEDGER CRYPTOGRAPHIC AUDIT REPORT
============================================================
Status:        [VALID]
Total Blocks:  2
Total Events:  40
Errors Found:  0

All hash-chain linkages, Merkle roots, and Ed25519 signatures verified.
============================================================
```

### Step 5.3: Trace a Simulated Leak
Provide a leaked text or image file. The engine identifies the copy, traces the custody ledger, and outputs the responsible custodian:

```powershell
python -m src.cli trace-leak --file demo_data/copies/CPY-05.txt --ledger-file demo_data/ledger.json --manifest demo_data/manifest.json
```

**Expected Console Output:**
```
=================================================================
FORENSIC LEAK INVESTIGATION REPORT
=================================================================
Sample File:         CPY-05.txt
Sample Type:         TEXT
Detected Copy ID:    CPY-05
Detection Layer:     LAYER_1_ZERO_WIDTH
Attribution Status:  MATCH_VERIFIED
Confidence Score:    100.0%
-----------------------------------------------------------------
Custody Events:      2
Last Custodian ID:   CUST-01-COE
Last Location:       HQ-CAMPUS
Last Action:         DISPATCHED_TO_CENTER
Timestamp:           2026-10-31T09:30:00.000000+00:00
-----------------------------------------------------------------
Conclusion: POSITIVE ATTRIBUTION: Leaked copy CPY-05 was identified via LAYER_1_ZERO_WIDTH with 100.0% confidence...
=================================================================
```

---

## 6. How to Run Each Test in the Frozen Protocol

### Step 6.1: Run the Unified Test Suite
Executes Tests 1, 2, and 3 sequentially and regenerates the raw logs:

```powershell
python tests/run_all_tests.py
```

### Step 6.2: Run Tests Individually via pytest
You can also run individual test suites using `pytest`:

```powershell
pytest -v tests/test_fingerprint.py
pytest -v tests/test_ledger_integrity.py
pytest -v tests/test_event_timing.py
```

---

## 7. How to Reproduce the Calculations

After running `python tests/run_all_tests.py`, run this one-line calculation script to independently verify the summary metrics in `05_Calculations/Calculations.md`:

```powershell
python -c "import csv, statistics; rows = [float(r['Start/end or elapsed time']) for r in csv.DictReader(open('SoI_P3_LeakTracing_Evidence/04_Raw_Test_Logs/event_timing_tests.csv'))]; print(f'Mean: {statistics.mean(rows):.4f} ms'); print(f'Max: {max(rows):.4f} ms'); print(f'Median: {statistics.median(rows):.4f} ms')"
```

---

## 8. Identifying Failed Tests & Error Diagnosis

* **Fingerprint Failure:** If detected copy ID is `NONE` or doesn't match expected ID, `Match status` will indicate `FALSE_MATCH` or `NO_MATCH`.
* **Ledger Tampering Failure:** If any deliberate tampering injection is not detected, `Detection status` in `ledger_integrity_tests.csv` will read `MISSED` and the runner will fail.
* **Latency Failure:** If any event exceeds $5000\text{ ms}$, `Target Met` will report `False`.

---

## 9. Distinguishing Genuine Test Results from Demonstrations

* Files located in `SoI_P3_LeakTracing_Evidence/04_Raw_Test_Logs/` are **genuine execution logs** generated during formal test runs.
* Files in `demo_data/` are temporary sandbox outputs created when testing the interactive CLI.

---

## 10. Cleanup Instructions

To remove temporary demonstration files without touching frozen evidence:

```powershell
Remove-Item -Recurse -Force demo_data -ErrorAction SilentlyContinue
```

---

## 11. Troubleshooting

| Symptom | Cause | Solution |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'cryptography'` | Cryptography package not installed | Run `pip install cryptography` |
| `ModuleNotFoundError: No module named 'PIL'` | Pillow package not installed | Run `pip install pillow` |
| `fatal: not a git repository` | Git uninitialized in test directory | Run `git status` inside `e:\bw` |
| Windows `cp1252` console encoding error | Printing non-ASCII characters directly | The CLI and test runner use ASCII-compatible `INR` formatting |
