# Raw Test Logs & Execution Data

* **Run Identifier:** `RUN-SOI-P3-20261031-161854`
* **Execution Timestamp:** 2026-10-31T16:18:54.150281+00:00 (UTC)
* **Command Executed:** `python tests/run_all_tests.py`
* **Artifact Version:** `v0.3.0-poc` (Git Commit: `d40487ae9053fe7cfc280328a076b03646011763`)
* **Host Platform:** Windows 11 Enterprise (10.0.26300, AMD64), Python 3.12.10

---

## 1. Directory Structure

```
04_Raw_Test_Logs/
├── README.md                     # This documentation file
├── fingerprint_tests.csv         # Genuine raw log for Test 1 (Fingerprint Tracing)
├── ledger_integrity_tests.csv    # Genuine raw log for Test 2 (Ledger Tampering Detection)
├── event_timing_tests.csv        # Genuine raw log for Test 3 (Event Latency & Cost)
└── run_metadata.json             # Environment and KPI summary snapshot
```

---

## 2. Log File Schemas & Column Descriptions

### 2.1 `fingerprint_tests.csv` (Test 1: Fingerprint Tracing)
Records attribution performance across 20 transformed question paper copies and 4 unmarked comparator samples.

| Column Header | Data Type | Description |
| :--- | :--- | :--- |
| **Run ID** | String | Global unique test run identifier (`RUN-SOI-P3-20261031-161854`) |
| **Sample ID** | String | Individual sample code (`SMP-01` through `SMP-20`, or `COMP-UNMARKED-01`..`04`) |
| **Transformation** | String | Transformation applied: `Copying`, `Retyping`, `Screenshot`, `Print and scan`, or `Unmarked Baseline (Comparator)` |
| **Expected copy ID** | String | Ground-truth copy identifier (`CPY-01`..`CPY-20`, or `NONE` for comparator) |
| **Detected copy ID** | String | Identifier recovered by the multi-layer extraction pipeline (`CPY-xx` or `NONE`) |
| **Match status** | String | Classification: `CORRECT_MATCH`, `CORRECT_REJECTION`, `FALSE_MATCH`, or `NO_MATCH` |
| **Ambiguous/failed status** | String | Flag: `NONE`, `AMBIGUOUS`, or `FAILED` |
| **Notes** | String | Detection layer triggered (`LAYER_1_ZERO_WIDTH`, `LAYER_2_SYNTACTIC`, `LAYER_3_VISUAL_PATTERN`) and confidence score |

### 2.2 `ledger_integrity_tests.csv` (Test 2: Ledger Integrity)
Records detection capability across 10 distinct deliberate tampering attacks against the cryptographic blockchain ledger, plus 2 editable register comparators.

| Column Header | Data Type | Description |
| :--- | :--- | :--- |
| **Run ID** | String | Global unique test run identifier (`RUN-SOI-P3-20261031-161854`) |
| **Entry ID** | String | Attack identifier (`TAMPER-01` through `TAMPER-10`, or `COMP-EDITABLE-REG-01`..`02`) |
| **Modification type** | String | Specific tampering applied (e.g., `Altered Event Timestamp`, `Custodian ID Substitution`, `Broken Chain Linkage`) |
| **Expected integrity result** | String | Anticipated system verdict: `FLAGGED_COMPROMISED` (or `PASSED_UNNOTICED` for comparator) |
| **Actual result** | String | Observed cryptographic verification verdict and count of errors detected |
| **Detection status** | String | Audit outcome: `DETECTED` (for cryptographic ledger) or `UNDETECTABLE_IN_COMPARATOR` (for editable register) |
| **Notes** | String | Cryptographic failure details (e.g., `MERKLE_ROOT_MISMATCH`, `INVALID_EVENT_SIGNATURE`, `BROKEN_HASH_LINK`) |

### 2.3 `event_timing_tests.csv` (Test 3: Event-Logging Latency and Cost)
Records high-resolution elapsed time measurements across 50 consecutive access-event lifecycle operations.

| Column Header | Data Type | Description |
| :--- | :--- | :--- |
| **Run ID** | String | Global unique test run identifier (`RUN-SOI-P3-20261031-161854`) |
| **Event number** | String | Sequential event identifier (`EV-LOG-001` through `EV-LOG-050`) |
| **Operation** | String | Custody transition action: Construct + Ed25519 Sign + Verify + Ledger Ingest |
| **Start/end or elapsed time** | Float (String) | Measured duration for the entire four-step operation (measured via `time.perf_counter_ns()`) |
| **Unit** | String | Measurement unit (`milliseconds`) |
| **Outcome** | String | Operational status: `SUCCESS` or `FAILED` |
| **Notes** | String | Target comparison ($\le 5000\text{ ms}$) and incurred fee status (`INR 0`) |

### 2.4 `run_metadata.json`
Machine-readable snapshot recording host operating system, CPU architecture, Python version, Git commit hash, timestamp, and high-level KPI target compliance.

---

## 3. Authenticity & Non-Simulation Guarantee

All CSV and JSON files in this folder contain genuine measurement data emitted directly by Python execution during run `RUN-SOI-P3-20261031-161854`. No mock generators, manual CSV edits, or synthetic success numbers were substituted. Reviewers can independently re-generate these exact logs by executing `python tests/run_all_tests.py`.
