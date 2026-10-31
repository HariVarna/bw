# Phase 1: Repository Analysis and Architecture Specification
## Project: Blockchain-Based Leak Tracing for Examination Question Papers (SoI Phase 3 PoC)
**Repository:** `https://github.com/HariVarna/bw`  
**Execution Environment:** Python 3.12.10 (Windows x64)  
**Date:** 31 October 2026  

---

## 1. Codebase Overview & Inventory

The repository is organized into three primary top-level directories:
- `src/`: Core domain models, cryptographic utilities, multi-layer document steganography, blockchain ledger implementation, forensic leak tracer, and CLI interface.
- `tests/`: Automated test suite implementing the SoI Phase 3 Frozen Test Protocol (Test 1: Fingerprint Tracing, Test 2: Ledger Tampering, Test 3: Event-Logging Timing and Cost).
- `SoI_P3_LeakTracing_Evidence/`: Frozen evidence package containing master index, protocol specifications, raw CSV/JSON logs, quantitative calculations, replay guides, and architectural annexures.

### Component Manifest (`src/`)

| File | Lines | Bytes | Role & Implemented Capabilities |
| :--- | :--- | :--- | :--- |
| `src/__init__.py` | 5 | 193 | Package initialization, metadata, version `0.3.0-poc`, author credentials. |
| `src/crypto.py` | 92 | 3,398 | Ed25519 asymmetric keypair generation (`generate_keypair`), message signing (`sign_message`), signature verification (`verify_signature`), SHA-256 cryptographic hashing (`sha256_hex`), Merkle root computation (`compute_merkle_root`), deterministic JSON canonicalization (`canonical_json_bytes`). |
| `src/models.py` | 171 | 5,480 | Dataclasses for `Custodian`, `QuestionPaper`, `AccessEvent`, and `Block`. Enumeration `AccessAction` defining 8 distinct custody stages. Methods for canonical event payload serialization, digest calculation, signing, and signature verification. |
| `src/paper_generator.py` | 74 | 3,676 | Synthetic university examination question paper generator (`generate_synthetic_question_paper`) producing structured instructions, Part A (10 questions x 2 marks), Part B (5 questions x 16 marks), and plain text rendering. |
| `src/fingerprint.py` | 344 | 12,678 | Multi-layer fingerprinting: Layer 1 (Zero-Width Unicode steganography via ZWSP, ZWNJ, ZWJ), Layer 2 (Syntactic and punctuation permutations supporting up to 256 unique copies), Layer 3 (Visual raster rendering with corner micro-pattern grids and watermarks using Pillow), and multi-layer extraction pipeline (`extract_fingerprint`). |
| `src/ledger.py` | 187 | 7,311 | `BlockchainLedger` managing in-memory and persistent append-only chain of blocks. Genesis block creation, event validation and queuing, block mining/commitment, disk persistence (`save_to_disk`, `load_from_disk`), and comprehensive cryptographic auditing (`verify_ledger_integrity`). |
| `src/leak_tracer.py` | 132 | 4,955 | `LeakTracer` engine. Correlates extracted fingerprint signals from text snippets or scanned images with ledger custody records. Builds chronological handover trails and generates a forensic attribution dossier (`ForensicReport`). |
| `src/cli.py` | 219 | 9,024 | Command-line interface providing `init-batch` (generate fingerprinted copies, custodians, and initial ledger), `verify-ledger` (audit ledger integrity), and `trace-leak` (trace leaked snippet or image). |

---

## 2. Test Suite & Genuine Execution Results

The test suite was executed locally via `python tests/run_all_tests.py` using Python 3.12.10. All tests completed with **100% pass rates**, fully meeting or exceeding Phase 3 Frozen Test Protocol benchmarks:

```text
======================================================================
EXECUTING SOI PHASE 3 FROZEN TEST PROTOCOL (AY 2026-27)
Project: Blockchain-Based Leak Tracing for Examination Question Papers
Concept: I01 — Fingerprinted Copies + Blockchain Access Ledger
======================================================================
Assigned Execution Run ID: RUN-SOI-P3-20261031-163616

Test 1: Fingerprint Tracing under Transformations
  - Total Samples: 20 test samples + 4 comparator samples
  - Transformations Tested: Digital Copying (5), Human Retyping (5), Screen Capture (5), Print & Scan (5)
  - Correct Matches: 20/20 (100.0%)
  - Target: >= 90.0% -> PASSED

Test 2: Ledger Integrity under Deliberate Tampering
  - Total Attack Vectors: 10 distinct vectors (timestamp alteration, custodian substitution, signature corruption, event deletion, event injection, Merkle root tampering, block hash recalculation bypass, invalid block sequence, broken prev_hash, genesis block alteration)
  - Detected Tampering: 10/10 (100.0%)
  - Target: 10/10 (100.0%) -> PASSED

Test 3: Event-Logging Latency and Cost Benchmark
  - Consecutive Logged Events: 50 operations (construct + Ed25519 sign + verify + ingest)
  - Average Latency: 0.4632 ms (0.000463 s)
  - Maximum Latency: 1.5649 ms (0.001565 s)
  - Target: <= 5.0 s -> PASSED (exceeded by ~10,000x speedup)
  - Incurred Compute Cost: INR 0.0 (Local permissioned ledger) -> PASSED
```

---

## 3. Analysis: Implemented, Tested, and Documented Features

| Capability | Code Status | Test Status | Documentation Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Layer 1: Zero-Width Steganography** | Implemented (`src/fingerprint.py`) | Tested (100% in digital copying) | Fully documented | Decodes exact ASCII/copy_id string from binary ZWSP/ZWNJ bits enclosed by ZWJ frames. |
| **Layer 2: Syntactic Permutations** | Implemented (`src/fingerprint.py`) | Tested (100% in plain retyping) | Fully documented | Base-4 permutation vector over instruction prefixes and question phrases. Survives retyping. |
| **Layer 3: Visual Corner Micro-Grids** | Implemented (`src/fingerprint.py`) | Tested (100% in screenshot/print-scan) | Fully documented | 16-bit binary micro-cell grid rendered in top-right margin of PIL raster image. |
| **Ed25519 Digital Signatures** | Implemented (`src/crypto.py`) | Tested (Sign + Verify across 50 events) | Fully documented | Uses Python `cryptography` primitives. Guarantees non-repudiation. |
| **SHA-256 Merkle Tree Chaining** | Implemented (`src/crypto.py`, `src/ledger.py`) | Tested (Verified across 10 tamper attacks) | Fully documented | Merkle root calculated for every block; header hash links to `prev_hash`. |
| **Append-Only Ledger Persistence** | Implemented (`src/ledger.py`) | Tested | Fully documented | Serializes and loads canonical block structures to/from JSON. |
| **Forensic Leak Tracer** | Implemented (`src/leak_tracer.py`) | Tested via CLI and unit workflows | Fully documented | Produces `ForensicReport` correlating detection layer, confidence, and chain of custody. |
| **PBFT Distributed Consensus** | Not in PoC (Single-node permissioned) | N/A | Documented as future Phase 4 roadmap | Phase 3 focuses on single-node cryptographic integrity. |
| **OCR Image Preprocessing** | Not in PoC (direct raster grid sampling) | N/A | Documented as future work | Currently uses micro-pattern coordinate sampling. |

---

## 4. Backend-to-Web Feature Mapping

The Flask web application will directly reuse and expose the existing verified backend modules without rewriting or mocking:

| Web Interface Section | Web Feature / View | Reused Backend Functions | Data Source |
| :--- | :--- | :--- | :--- |
| **Dashboard** | System KPI cards (Exams, Custodians, Copies, Events, Investigations) | `BlockchainLedger`, `database.py` count queries | SQLite database + active `ledger.json` |
| **Dashboard** | Live Ledger Integrity Health Monitor | `BlockchainLedger.verify_ledger_integrity()` | Live cryptographic chain audit |
| **Dashboard** | Examination Security Workflow Diagram | High-level interactive visualization of SoI 7-stage custody protocol | Dynamic SVG / CSS component |
| **Dashboard** | Recent Audit & Custody Activity Feed | SQLite `audit_logs` + `ledger.chain` recent events | SQLite + Ledger |
| **Dashboard** | Seed / Reset Demo Dataset | `paper_generator.py`, `fingerprint.py`, `crypto.py`, `ledger.py` | Clean automated seeding routine |
| **Examinations** | View master question paper & metadata | `generate_synthetic_question_paper()`, `QuestionPaper.render_plain_text()` | SQLite `examinations` |
| **Custodians** | Custodian directory with role & public keys | `crypto.generate_keypair()`, `Custodian.to_dict()` | SQLite `custodians` |
| **Fingerprinted Copies** | Inspect Layer 1, Layer 2, Layer 3 for generated copies | `apply_fingerprint_to_text()`, `render_paper_image()`, `derive_syntactic_vector()` | SQLite `fingerprinted_copies` + generated files |
| **Access Ledger** | Blockchain Explorer (Blocks, Events, Merkle Roots) | `BlockchainLedger.chain`, `Block.header_bytes()`, `compute_merkle_root()` | Active `ledger.json` / SQLite |
| **Access Ledger** | On-Demand Cryptographic Tamper Audit | `BlockchainLedger.verify_ledger_integrity()` | Live recalculation of all hashes |
| **Leak Investigation** | Upload snippet or image & perform multi-layer forensic tracing | `extract_fingerprint()`, `LeakTracer.trace_leak()` | User input + active ledger + manifest |
| **Reports** | Frozen Protocol test results & forensic audit dossier | Reads `SoI_P3_LeakTracing_Evidence/04_Raw_Test_Logs` + generated dossiers | CSV logs + database |
| **System Info** | Cryptographic parameters, hash algorithms, environment diagnostics | System inspection + `src.__version__` + `platform` | Runtime diagnostics |
