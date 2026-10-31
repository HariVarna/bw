# Technical Annexure 1: System Architecture

* **Project Title:** Blockchain-Based Leak Tracing for Examination Question Papers
* **Concept:** I01 — Fingerprinted Copies + Blockchain Access Ledger
* **Artifact Version:** `v0.3.0-poc`
* **Status:** Complete Technical Specification

---

## 1. System Decomposition & Logical Components

The system architecture partitions into five primary functional layers:

```
+-------------------------------------------------------------------------+
|                        APPLICATION & REVIEWER LAYER                     |
|            CLI (src/cli.py) | Forensic Tracer (src/leak_tracer.py)      |
+-------------------------------------------------------------------------+
                                    |
+-----------------------------------+-------------------------------------+
|        DOCUMENT GENERATION        |       FINGERPRINTING ENGINE         |
|   Paper Generator (paper_gen.py)  |   - Layer 1: Zero-Width Steganography|
|   Standardized Exam Templates     |   - Layer 2: Syntactic Permutations  |
|                                   |   - Layer 3: Visual Corner Grids    |
+-----------------------------------+-------------------------------------+
                                    |
+-----------------------------------+-------------------------------------+
|        CRYPTOGRAPHIC ENGINE       |       BLOCKCHAIN ACCESS LEDGER      |
|   - Ed25519 Signing & Verify      |   - Append-Only Block Chain         |
|   - SHA-256 Digest Calculations   |   - Merkle Tree Batch Summaries     |
|   - Canonical JSON Serialization  |   - Tamper Detection Audit Engine   |
+-----------------------------------+-------------------------------------+
                                    |
+-------------------------------------------------------------------------+
|                           PERSISTENCE LAYER                             |
|       Append-Only Ledger Store (JSON) | Asset Storage (PNG / TXT)       |
+-------------------------------------------------------------------------+
```

---

## 2. Component Responsibilities & Interface Specifications

### 2.1 Cryptographic Utilities (`src/crypto.py`)
* **Responsibilities:** Provides mathematically verified implementations of Ed25519 asymmetric cryptography and SHA-256 Merkle trees.
* **Key Interfaces:**
  * `generate_keypair() -> (priv_b64, pub_b64)`
  * `sign_message(priv_b64, message_bytes) -> signature_b64`
  * `verify_signature(pub_b64, message_bytes, signature_b64) -> bool`
  * `compute_merkle_root(leaf_hashes: list[str]) -> str`
  * `canonical_json_bytes(obj) -> bytes` (enforces deterministic key ordering and compact separators)

### 2.2 Domain Models (`src/models.py`)
* **Responsibilities:** Strongly typed data representations enforcing data integrity.
* **Entities:**
  * `Custodian`: Identifies university officials, public keys, and roles.
  * `QuestionPaper`: Standard university paper model (Part A, Part B, Instructions).
  * `AccessEvent`: Atomic custody transition containing `event_id`, `copy_id`, `action`, `custodian_id`, `location`, `timestamp`, and `signature`.
  * `Block`: Cryptographic grouping containing `index`, `timestamp`, `prev_hash`, `merkle_root`, `events`, and `block_hash`.

### 2.3 Multi-Layer Fingerprinting (`src/fingerprint.py`)
* **Responsibilities:** Embeds copy identifiers into plain text and rendered raster images, and performs forensic pattern recovery.
* **Mechanisms:**
  * **Layer 1 (Zero-Width):** Maps ASCII characters to binary sequences of `\u200b` (0) and `\u200c` (1) enclosed by `\u200d`.
  * **Layer 2 (Syntactic):** Selects from 4 stylistic variations across 4 document feature points (instruction prefixes, calculator clauses, mobile phone warnings, section headers), supporting up to $4^4 = 256$ unique vectors.
  * **Layer 3 (Visual Corner Grid):** Renders a 16-bit binary pixel pattern in top-right corner margins along with faint diagonal page watermarks.

### 2.4 Blockchain Access Ledger (`src/ledger.py`)
* **Responsibilities:** Maintains the tamper-evident chain of custody blocks.
* **Key Interfaces:**
  * `add_event(event: AccessEvent, verify_sig=True) -> (bool, str)`
  * `commit_block() -> Block`
  * `verify_ledger_integrity() -> dict` (audits Genesis block, block hash linkage, Merkle roots, and Ed25519 signatures)
  * `get_events_for_copy(copy_id) -> list[AccessEvent]`

### 2.5 Forensic Leak Tracer (`src/leak_tracer.py`)
* **Responsibilities:** Connects recovered artifacts with the blockchain record.
* **Process:** Extracts candidate fingerprint from leaked text/image $\rightarrow$ Queries ledger for copy custody history $\rightarrow$ Identifies the last registered custodian, location, and action.

---

## 3. Data Storage & Schema

* **Ledger Store (`ledger.json`):** Formatted as an append-only JSON structure containing an array of chained blocks.
* **Manifest (`manifest.json`):** Public registration mapping copy IDs to syntactic choice vectors and assigned custodians.
* **Document Assets:** Master text file (`master_question_paper.txt`), fingerprinted text copies (`copies/CPY-xx.txt`), and high-resolution raster images (`copies/CPY-xx.png`).

---

## 4. Trust Boundaries & Threat Model

```
[ UNTRUSTED PHYSICAL / EXTERNAL ENVIRONMENT ]
         | (Leaks, Screen Captures, Photocopies, Redaction)
         v
+--------------------------------------------------------------+
| TRUST BOUNDARY: Forensic Ingestion Engine                     |
| - Strips noise, normalizes text, decodes steganography       |
+--------------------------------------------------------------+
         |
+--------------------------------------------------------------+
| TRUST BOUNDARY: Permissioned Ledger Core                     |
| - Custodians possess private keys                            |
| - Public keys registered in verified directory               |
| - Unsigned or forged events are rejected at ingestion        |
| - Any block mutation triggers Merkle / Hash failure          |
+--------------------------------------------------------------+
```

### Assumptions:
1. Custodians safeguard their private keys during their active custody window.
2. The university administration operates the ledger nodes in a secure server room or managed cloud.
3. The original question paper master is generated in an air-gapped confidential press facility.

---

## 5. Security & Cryptographic Guarantees

1. **Non-Repudiation:** Custodians cannot deny handling a copy because every custody event is signed with their unique Ed25519 private key.
2. **Immutability:** Once committed into a block, changing even 1 bit in an event changes its digest, which breaks the block Merkle root, which alters the block hash, breaking the entire downstream hash chain.
3. **Collision Resistance:** Copy IDs are mapped via 16-bit to 256-bit unique hashes, preventing ambiguous identity collisions in institutional batches up to 65,536 copies.
