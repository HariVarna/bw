# School of Innovation (SoI) — Phase 3 Evidence Package

## Project Title: Blockchain-Based Leak Tracing for Examination Question Papers
### Concept: I01 — Fingerprinted Copies + Blockchain Access Ledger

* **Academic Year:** 2026–27
* **Program:** Phase 3: Proof of Concept
* **Vertical:** Blockchain | **Batch:** 2025–29
* **Project Team:**
  * Hari Varna V S
  * Harshavardini D
  * Kavin Kumar V
  * Mohanavel N
* **Faculty Mentor:** Selva Kumar (as listed in Ideation Document)
* **Date of Submission:** 31 October 2026
* **Artifact Version:** `v0.3.0-poc` | **Git Commit Hash:** `d40487ae9053fe7cfc280328a076b03646011763`
* **Test Run ID:** `RUN-SOI-P3-20261031-161854`

---

## 1. Executive Summary & Reviewer Guidance

This repository contains the complete, reviewer-ready **Phase 3: Proof of Concept Evidence Package** for our investigation into cryptographic document security and tamper-evident custody tracking for high-stakes academic examinations.

The core problem addressed is the attribution gap during examination paper leaks: when an examination paper is leaked prior to or during an examination, traditional paper registers and unmarked photocopies cannot prove which custodian or center was responsible.

Our selected concept (**I01: Fingerprinted Copies + Blockchain Access Ledger**) solves this by:
1. **Multi-Layer Steganographic Fingerprinting:** Embedding imperceptible, deterministic signals (invisible zero-width unicode steganography, syntactic phrase permutations, and visual corner micro-grids) into each serialized copy.
2. **Permissioned Blockchain Access Ledger:** Recording every physical and digital custody transition in an append-only, SHA-256 Merkle-tree backed blockchain ledger where every transaction is signed by the custodian using **Ed25519 digital signatures**.
3. **Forensic Attribution Engine:** Ingesting leaked snippets or photos, extracting the underlying copy identifier, querying the blockchain ledger, and pinpointing the exact custodian responsible.

---

## 2. Evidence Package Directory Structure

```
SoI_P3_LeakTracing_Evidence/
│
├── 00_Evidence_Index/
│   └── Evidence_Index.md          # Master catalog mapping evidence IDs E01-E10 to criteria and files
│
├── 01_Frozen_Test_Protocol/
│   └── Frozen_Test_Protocol.md    # Original frozen success criteria from 16 Oct 2026 Phase 2 Ideation
│
├── 02_Source_Code/
│   └── README.md                  # Codebase architecture, dependencies, components, build instructions
│
├── 03_Versioned_Test_Artifact/
│   └── Artifact_Version.md        # Exact artifact manifest, environment baseline, SHA-256 checksums
│
├── 04_Raw_Test_Logs/
│   ├── README.md                  # Schema definitions and data dictionaries
│   ├── fingerprint_tests.csv      # Genuine raw log: Test 1 (20 transformed samples + 4 comparators)
│   ├── ledger_integrity_tests.csv # Genuine raw log: Test 2 (10 deliberate tampering attack vectors)
│   ├── event_timing_tests.csv     # Genuine raw log: Test 3 (50 high-precision timed custody events)
│   └── run_metadata.json          # Complete execution snapshot with platform & commit hash
│
├── 05_Calculations/
│   └── Calculations.md            # Mathematical derivations, worked formulas, and target comparisons
│
├── 06_Replay_Documentation/
│   └── Replay_README.md           # Step-by-step reproduction instructions and CLI command runbook
│
├── 07_Sources/
│   └── Sources.md                 # Academic and technical references for crypto, hashing, and steganography
│
├── 08_AI_Disclosure/
│   └── AI_Disclosure.md           # Ethical statement on AI tools used, team validation, and scope
│
├── 09_Annexures/
│   ├── Architecture.md            # Detailed component breakdown, trust boundaries, threat model
│   ├── Data_Flow.md               # 7-stage end-to-end data flow from paper generation to leak dossier
│   ├── Known_Limitations.md       # Honest analysis of degradation, OCR, key storage, analog hole
│   └── Screenshots/
│       └── README.md              # Screenshot inventory, checklist, and terminal output references
│
└── README.md                      # This package overview document
```

---

## 3. Master Test Results Summary

All tests were executed against commit `d40487a` on 31 October 2026 under the Frozen Test Protocol:

| Protocol Test | Original Phase 2 Target | Comparator Baseline | Phase 3 Actual Measurement | Evaluation |
| :--- | :--- | :--- | :--- | :--- |
| **Test 1: Fingerprint Tracing** | $\ge 18 / 20$ correct ($\ge 90\%$) | $1 \text{ in } 10$ ($10\%$, random guessing) | **$20 / 20$ correct ($100.0\%$)** | **PASSED (Target Met)** |
| **Test 2: Ledger Tampering Detection** | $10 / 10$ detected ($100\%$) | $0\%$ (editable register without crypto hashing) | **$10 / 10$ detected ($100.0\%$)** | **PASSED (Target Met)** |
| **Test 3: Event Latency & Cost** | $\le 5.0\text{ s}$ per event; Cost $=\text{₹0}$ | $30\text{ to } 60\text{ s}$ (manual paper register) | **Mean: $0.2514\text{ ms}$; Max: $0.5503\text{ ms}$; Cost: $\text{₹0}$** | **PASSED (Target Met)** |

---

## 4. Quick Start for Reviewers

To reproduce the complete test protocol and verify calculations:

```powershell
# Navigate to repository root
cd e:\bw

# Install dependencies
pip install cryptography pillow

# Execute the frozen test protocol
python tests/run_all_tests.py

# Run end-to-end CLI workflow demonstration
python -m src.cli init-batch --count 20 --output-dir demo_data
python -m src.cli verify-ledger --ledger-file demo_data/ledger.json
python -m src.cli trace-leak --file demo_data/copies/CPY-05.txt --ledger-file demo_data/ledger.json --manifest demo_data/manifest.json
```

---

## 5. Submission & Reviewer Cloud Access Note

This evidence package was generated and validated on the team's local development environment. In accordance with Phase 3 instructions, local folder creation does not grant cloud access. The project team will upload this directory to the designated School of Innovation portal and configure institutional reviewer permissions.
