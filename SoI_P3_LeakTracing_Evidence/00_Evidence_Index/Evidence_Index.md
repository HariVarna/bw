# Phase 3 Evidence Index: Blockchain-Based Leak Tracing for Examination Question Papers

* **Institution:** School of Innovation
* **Academic Year:** 2026–27
* **Phase:** Phase 3: Proof of Concept
* **Concept:** I01 — Fingerprinted Copies + Blockchain Access Ledger
* **Project Team:**
  * Hari Varna V S
  * Harshavardini D
  * Kavin Kumar V
  * Mohanavel N
* **Batch:** 2025–29 | **Vertical:** Blockchain
* **Faculty Mentor:** Selva Kumar
* **Execution Timestamp (UTC):** 2026-10-31T16:18:54Z
* **Execution Run ID:** `RUN-SOI-P3-20261031-161854`
* **Artifact Version:** `v0.3.0-poc`
* **Git Commit Hash:** `d40487ae9053fe7cfc280328a076b03646011763`

---

## 1. Master Evidence Register

This index catalogs all evidence items collected for the Phase 3 Proof of Concept submission. Evidence identifiers (`E01`–`E10`) are internal reference labels for traceability and auditability, distinct from official institutional receipt identifiers.

### Evidence Status Definitions
* **Available:** Documented and present in the package, representing foundational protocols, disclosures, and architectural designs.
* **Verified:** Fully implemented, executed under test protocol, mathematically validated, and cross-referenced with genuine raw test logs and cryptographic artifacts.
* **Implemented but not tested:** Software component exists in the codebase but has not yet completed formal protocol verification.
* **Planned:** Architectural or operational feature designed for production roadmap but excluded from the current Proof of Concept scope.
* **Missing:** Required evidence item that was neither observed nor generated during Phase 3 execution.

| Evidence ID | Evidence Title | File Path | Evidence Type | Related Success Criterion | Evidence Status | Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **E01** | Project & Concept Reference | [README.md](../README.md) | Project Overview | Baseline alignment with Phase 2 Ideation | **Available** | Project metadata, team charter, problem statement, selected concept (I01), and review package boundaries. |
| **E02** | Frozen Test Protocol | [01_Frozen_Test_Protocol/Frozen_Test_Protocol.md](../01_Frozen_Test_Protocol/Frozen_Test_Protocol.md) | Test Specification | Protocol specification for Tests 1, 2, and 3 | **Available** | Frozen test methodology dated 16 October 2026, defining hypotheses, sample generation, comparators, pass/fail rules, and stop rules. |
| **E03** | Source Code & Artifact Version | [02_Source_Code/README.md](../02_Source_Code/README.md)<br>[03_Versioned_Test_Artifact/Artifact_Version.md](../03_Versioned_Test_Artifact/Artifact_Version.md) | Software Artifact & Manifest | Reproducible build baseline | **Verified** | Core Python 3.12 prototype, cryptographic engine (Ed25519, SHA-256, Merkle Trees), environment manifest, and exact Git commit hash `d40487a`. |
| **E04** | Fingerprint Verification Test Output | [04_Raw_Test_Logs/fingerprint_tests.csv](../04_Raw_Test_Logs/fingerprint_tests.csv) | Raw Test Log (CSV) | Test 1: Fingerprint tracing (Target: >= 18/20, 90%) | **Verified** | Genuine CSV output of 20 transformed samples (copying, retyping, screenshot, print-and-scan) plus 4 unmarked comparators. Accuracy: 20/20 (100%). |
| **E05** | Ledger Integrity Test Output | [04_Raw_Test_Logs/ledger_integrity_tests.csv](../04_Raw_Test_Logs/ledger_integrity_tests.csv) | Raw Test Log (CSV) | Test 2: Tampering detection (Target: 10/10, 100%) | **Verified** | Genuine CSV output of 10 distinct deliberate tampering attacks against the cryptographic ledger plus editable register baseline. Detection: 10/10 (100%). |
| **E06** | Event Timing & Cost Measurements | [04_Raw_Test_Logs/event_timing_tests.csv](../04_Raw_Test_Logs/event_timing_tests.csv)<br>[04_Raw_Test_Logs/run_metadata.json](../04_Raw_Test_Logs/run_metadata.json) | Performance Benchmark (CSV/JSON) | Test 3: Latency <= 5.0 s; Cost = INR 0 | **Verified** | High-resolution benchmark of 50 consecutive access events. Mean latency: 0.2514 ms; Max: 0.5503 ms; Incurred transaction cost: INR 0. |
| **E07** | Mathematical Calculations | [05_Calculations/Calculations.md](../05_Calculations/Calculations.md) | Audit Documentation | Formal verification of success metrics | **Verified** | Worked mathematical derivations for match rate, tamper detection rate, latency statistics (mean, median, max), and zero-cost model. |
| **E08** | Replay Instructions | [06_Replay_Documentation/Replay_README.md](../06_Replay_Documentation/Replay_README.md) | Operational Runbook | Independent reviewer reproducibility | **Verified** | Step-by-step instructions tested and verified on Windows 11 / AMD64 Python 3.12 runtime with exact CLI reproduction commands. |
| **E09** | Architecture & Data-Flow Annexures | [09_Annexures/Architecture.md](../09_Annexures/Architecture.md)<br>[09_Annexures/Data_Flow.md](../09_Annexures/Data_Flow.md)<br>[09_Annexures/Known_Limitations.md](../09_Annexures/Known_Limitations.md) | System Documentation | System design and trust boundaries | **Available** | Technical specifications detailing component boundaries, Ed25519 signatures, Merkle verification, forensic data flows, and honest real-world limitations. |
| **E10** | AI Disclosure | [08_AI_Disclosure/AI_Disclosure.md](../08_AI_Disclosure/AI_Disclosure.md) | Governance & Ethics | Compliance with School of Innovation policy | **Available** | Complete, transparent record of AI assistance utilized for test harness scaffolding, documentation drafting, and mathematical verification. |

---

## 2. Integrity Certification

We, the student engineering team, certify that:
1. No simulated or fabricated data has been represented as genuine test execution evidence.
2. All raw logs in `04_Raw_Test_Logs/` were generated by running the automated test suite against the versioned software artifact `v0.3.0-poc` at commit `d40487a`.
3. The original success criteria formulated in the Phase 2 Ideation document (16 October 2026) have been preserved without post-hoc modifications.
4. Institutional review and official deployment approvals remain pending formal institutional submission; local prototype verification does not constitute campus-wide deployment authorization.
