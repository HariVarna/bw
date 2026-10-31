# Source Code & Software Implementation Baseline

* **Project Title:** Blockchain-Based Leak Tracing for Examination Question Papers
* **Selected Concept:** I01 — Fingerprinted Copies + Blockchain Access Ledger
* **Artifact Version:** `v0.3.0-poc`
* **Commit Hash:** `d40487ae9053fe7cfc280328a076b03646011763`
* **Release Date:** 31 October 2026
* **Primary Language:** Python 3.12+ (CPython)
* **Codebase Locations:**
  * Core Engine: `src/`
  * Test Suite: `tests/`
  * Evidence Package: `SoI_P3_LeakTracing_Evidence/`

---

## 1. Component Architecture & Modular Layout

The implementation is structured into clean, decoupled modules adhering to single-responsibility principles:

```
src/
├── __init__.py           # Package versioning (v0.3.0-poc) & author metadata
├── crypto.py             # Ed25519 signing/verification, SHA-256, Merkle Tree, Canonical JSON
├── models.py             # Dataclasses: Custodian, QuestionPaper, AccessEvent, Block, AccessAction
├── paper_generator.py    # Synthetic university examination paper generator (standardized format)
├── fingerprint.py        # Multi-layer fingerprinting: Layer 1 (ZWSP), Layer 2 (Syntactic), Layer 3 (Visual)
├── ledger.py             # Append-only blockchain ledger, block mining, persistence, cryptographic audit
├── leak_tracer.py        # Forensic attribution engine correlating fingerprints with custody chains
└── cli.py                # Reviewer CLI: batch generation, ledger verification, forensic leak tracing
```

---

## 2. Dependencies and Version Manifest

The prototype minimizes external attack surfaces by leveraging Python's standard library for deterministic hashing, supplemented by industry-standard cryptography and imaging libraries:

| Library | Version | Purpose in Prototype |
| :--- | :--- | :--- |
| **Python** | `3.12.10` | Core language runtime |
| **cryptography** | `50.0.2` | High-assurance Ed25519 asymmetric key generation, signing, and signature verification |
| **Pillow (PIL)** | `12.3.0` | Raster document rendering, visual corner micro-pattern generation, and print-scan simulation |
| **cffi** | `2.1.1` | Foreign function interface for native cryptographic bindings |
| **pycparser** | `3.12` | C parser supporting `cffi` |
| **Standard Library** | `3.12.10` | `hashlib` (SHA-256), `json` (canonical serialization), `statistics`, `time`, `pathlib`, `argparse` |

---

## 3. Implemented vs. Incomplete Components

To ensure complete academic and technical transparency, the current implementation status is categorized below:

### 3.1 Fully Implemented & Tested Components
1. **Synthetic Question Paper Generator (`paper_generator.py`):** Produces realistic multi-part university question papers with instructions, course headers, and mark allocations.
2. **Layer 1 Invisible Steganography (`fingerprint.py`):** Encodes 16-bit copy identifiers into invisible zero-width unicode sequences (`\u200b`, `\u200c`, `\u200d`). Survives exact digital copy-paste.
3. **Layer 2 Syntactic Permutation (`fingerprint.py`):** Applies deterministic base-4 permutations to instruction prefixes and specific vocabulary choices, surviving plain retyping.
4. **Layer 3 Visual Micro-Watermarking (`fingerprint.py`):** Renders high-resolution raster images embedding corner binary security grids and background micro-watermarks. Survives screenshotting and print-and-scan degradation.
5. **Ed25519 Cryptographic Signatures (`crypto.py`):** Generates asymmetric key pairs for examination custodians and cryptographically signs every access event.
6. **Merkle Tree & Block Hash Chaining (`ledger.py`):** Implements SHA-256 Merkle tree calculation across all events in a block and chains blocks via `prev_hash`.
7. **Comprehensive Audit Engine (`ledger.py`):** Traverses the blockchain to detect 10 distinct tampering attacks (payload modification, signature corruption, record deletion/injection, Merkle mismatch).
8. **Forensic Leak Tracer (`leak_tracer.py`):** Extracts recovered fingerprints and queries the blockchain ledger to produce an auditable custody handover trail.
9. **Full Reviewer CLI (`cli.py`):** Command-line tool for reproducing all operations.

### 3.2 Known Incomplete & Out-of-Scope Components (Future Roadmap)
* **Byzantine Fault Tolerant (PBFT) Network Consensus:** The Phase 3 PoC runs as a single-node permissioned ledger with deterministic append-only verification. Full multi-node PBFT socket consensus across decentralized university servers is scheduled for Phase 4.
* **Optical Character Recognition (OCR) Preprocessor:** When physical print-and-scan copies are degraded, our Layer 3 decoder directly samples the corner micro-grid. An end-to-end OCR pipeline (e.g., Tesseract OCR) to extract text from skewed smartphone camera photographs remains planned for future vertical integration.
* **Hardware Security Module (HSM) Key Storage:** Custodian Ed25519 private keys in this PoC are managed in memory during testing. Hardware token (FIDO2/PKCS#11) integration is an institutional deployment objective.

---

## 4. Technical Distinction: Visible Text Markers vs. Robust Steganography

Reviewers must note a critical technical distinction:

> **A visible text marker or metadata header is NOT equivalent to an invisible document fingerprint.**
> 
> * **Visible Text Markers / Metadata (e.g., "Copy CPY-01"):** Easily recognized and stripped by an intentional leaker using simple text deletion, cropping, or blurring. It provides zero survivability against deliberate redaction.
> * **Invisible Steganography (Layer 1):** Zero-width unicode characters are completely imperceptible to human readers and word processors. However, they are fragile under manual human retyping or basic ASCII-only OCR.
> * **Syntactic / Permutation Fingerprinting (Layer 2):** Alters subtle linguistic patterns (e.g., delimiter styles, synonymous phrases). A retyper who transcribes the text verbatim inadvertently preserves the unique fingerprint.
> * **Visual Micro-Grid Watermarking (Layer 3):** Encodes copy serial numbers into spatial pixel grids located outside standard text margins and embedded within background watermarks.
>
> Our Phase 3 implementation combines all three layers into a defense-in-depth model, acknowledging the specific failure modes of each technique.

---

## 5. Build and Verification Instructions

To execute the test suite and verify the prototype from a clean environment:

```powershell
# 1. Clone/Navigate to workspace
cd e:\bw

# 2. Verify Python environment
python --version  # Requires Python 3.10+

# 3. Install required dependencies
pip install cryptography pillow

# 4. Run frozen test protocol suite
python tests/run_all_tests.py

# 5. Verify CLI functionality
python -m src.cli --help
```
