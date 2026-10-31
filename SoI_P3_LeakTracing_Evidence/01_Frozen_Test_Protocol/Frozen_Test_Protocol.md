# Frozen Test Protocol: Phase 3 Proof of Concept

* **Document Version:** 1.0 (Baseline Frozen)
* **Original Protocol Date:** 16 October 2026
* **Execution Date:** 31 October 2026
* **Project Title:** Blockchain-Based Leak Tracing for Examination Question Papers
* **Selected Concept:** I01 — Fingerprinted Copies + Blockchain Access Ledger
* **Vertical:** Blockchain | **Batch:** 2025–29
* **Project Team:** Hari Varna V S, Harshavardini D, Kavin Kumar V, Mohanavel N
* **Faculty Mentor:** Selva Kumar

---

## 1. Protocol Freezing & Traceability Notice

This test protocol preserves the verbatim success criteria established in our Phase 2 Ideation submission dated **16 October 2026**. In compliance with School of Innovation audit guidelines, this protocol was locked prior to executing formal test runs on 31 October 2026. No thresholds, sample sizes, or pass/fail criteria have been retroactively modified to accommodate prototype performance.

---

## 2. Test 1: Fingerprint Tracing under Transformations

### 2.1 Original Objective & Success Target
* **Target:** Correctly identify the originating copy identifier for at least **18 out of 20** simulated leak samples ($\ge 90\%$).
* **Comparator Baseline:** Identical unmarked question paper copies distributed without digital fingerprinting. In the unmarked baseline, attribution is limited to random guessing among candidate custodians ($1 \text{ in } 10$, or $10\%$).

### 2.2 Hypothesis
A multi-layered document fingerprint—combining invisible zero-width unicode steganography, deterministic syntactic/punctuation permutations, and visual corner micro-markers—can survive digital copy-paste, manual retyping, screen capture, and print-and-scan rendering with an attribution accuracy exceeding $90\%$.

### 2.3 Test Environment & Hardware Specification
* **Operating System:** Windows 11 Enterprise (Build 10.0.26300, AMD64)
* **Runtime:** Python 3.12.10 (CPython)
* **Key Libraries:** `Pillow 12.3.0` (Image rendering, spatial transforms, Gaussian filtering), `cryptography 50.0.2`
* **Test Runner Script:** `tests/test_fingerprint.py`

### 2.4 Inputs & Sample-Generation Methodology
1. **Master Document:** A standardized engineering examination question paper generated via `src.paper_generator` (`QP-2026-CS801-AUTUMN`), consisting of Course Code, Title, Instructions to Candidates, Part A (10 short-answer questions, 2 marks each), and Part B (5 essay questions, 16 marks each).
2. **Fingerprinted Cohort:** 20 unique copies (`CPY-01` through `CPY-20`) generated deterministically:
   * **Layer 1 (Invisible Steganography):** Copy ID binary payload encoded into Zero-Width Space (`\u200b` for 0) and Zero-Width Non-Joiner (`\u200c` for 1), framed by Zero-Width Joiner (`\u200d`).
   * **Layer 2 (Syntactic Variation):** Base-4 variation vector governing instruction list delimiters, punctuation marks, and synonym phrase substitutions (e.g., "scientific calculators are permitted" vs "scientific calculators are allowed").
   * **Layer 3 (Visual Micro-Pattern):** 1200x1600 raster page rendering embedding an 8-pixel corner binary grid pattern encoding the copy serial number, plus faint background watermark.
3. **Comparator Samples:** 4 identical, unmarked master question paper copies without zero-width characters or syntactic permutations (`COMP-UNMARKED-01` to `COMP-UNMARKED-04`).

### 2.5 Planned Transformations (5 Samples Each)
* **Transformation 1: Copying (Samples `SMP-01` – `SMP-05`):** Direct clipboard digital text copying. Simulates digital leak via messaging apps or unformatted plain text.
* **Transformation 2: Retyping (Samples `SMP-06` – `SMP-10`):** Simulates manual retyping or aggressive OCR where non-printable unicode characters (`\u200b`, `\u200c`, `\u200d`) are stripped, but readable phrasing is preserved.
* **Transformation 3: Screenshot (Samples `SMP-11` – `SMP-15`):** High-resolution raster page capture cropped and re-encoded into PNG format.
* **Transformation 4: Print and Scan (Samples `SMP-16` – `SMP-20`):** Simulates physical handling: image degraded via Gaussian blur ($\sigma = 0.4$), contrast reduction, and lossy JPEG compression ($Q=90$).

### 2.6 Extraction & Matching Rules
Extraction traverses detection layers in decreasing order of bit-level precision:
1. **Primary Check (Layer 1):** Search for `\u200d[\u200b\u200c]+\u200d`. If found and decodes to a valid alphanumeric copy tag, match is declared with confidence $1.0$.
2. **Secondary Check (Layer 3):** If visual image is supplied, sample top-right corner micro-grid cells. If luminance thresholding recovers a valid integer copy tag, match is declared with confidence $0.95$.
3. **Tertiary Check (Layer 2):** If zero-width bits are absent, evaluate syntactic variation score across registered copies.
   * If best candidate score $\ge 6/12$ and leads runner-up by $\ge 3$ points: match declared with confidence $\text{Score} / 12.0$.
   * If top candidates tie: return `AMBIGUOUS`.

### 2.7 Classification Definitions
* **Correct Match:** Detected copy ID exactly equals Expected copy ID.
* **False Match:** Detected copy ID points to a different valid copy ID ($C_{\text{detected}} \ne C_{\text{expected}}$).
* **Ambiguous Result:** Extraction algorithm detects competing candidates with tied scores.
* **Unmatched / Failed:** No fingerprint pattern recognized across all three layers.
* **Correct Rejection (Comparator):** Unmarked sample yields `NONE` without false alarm.

### 2.8 Exclusion Rules
* Excerpts containing fewer than 15 consecutive words and lacking header metadata are excluded from Layer 2 syntactic evaluation due to insufficient entropy.
* Severely distorted images where corner alignment markers are completely clipped are excluded from Layer 3 grid decoding.

### 2.9 Pass/Fail Criteria
* **Pass:** Correct matches $\ge 18 / 20$ ($\ge 90\%$) with zero false matches against unmarked comparators.
* **Fail:** Correct matches $< 18 / 20$ ($< 90\%$) or false match rate $> 5\%$.

---

## 3. Test 2: Ledger Integrity under Deliberate Tampering

### 3.1 Original Objective & Success Target
* **Target:** Detect **10 out of 10** deliberately modified ledger entries ($100\%$ detection rate).
* **Comparator Baseline:** Standard editable relational/flat-file register where unauthorized record edits leave no cryptographic trail ($0\%$ intrinsic detection without external logs).

### 3.2 Hypothesis
A cryptographically chained ledger utilizing Ed25519 digital signatures, canonical JSON byte serialization, SHA-256 block hashing, and Merkle tree roots will deterministically detect any unauthorized bit modification in historical custody records.

### 3.3 Test Procedure & Attack Vectors
A baseline blockchain ledger is seeded with a Genesis block and two successive blocks containing 8 signed access events. Ten distinct tampering mutations are independently applied:

| Attack ID | Mutation Type | Description of Deliberate Modification | Expected Detection Mechanism |
| :--- | :--- | :--- | :--- |
| **TAMPER-01** | Timestamp Alteration | In-place change of event timestamp in Block 1 Event 0 | Merkle Root Mismatch & Ed25519 Signature Invalidity |
| **TAMPER-02** | Custodian Substitution | In-place change of custodian ID to malicious imposter | Merkle Root Mismatch & Ed25519 Signature Invalidity |
| **TAMPER-03** | Corrupted Signature | Bit inversion inside base64 Ed25519 signature payload | Cryptographic Signature Verification Failure |
| **TAMPER-04** | Record Deletion | Removal of Event 3 from Block 1 to hide custody step | Merkle Root Mismatch |
| **TAMPER-05** | Unauthorized Injection | Insertion of unmined fake event into Block 2 | Merkle Root Mismatch & Invalid Signature |
| **TAMPER-06** | Merkle Root Overwrite | Overwriting Block 1 Merkle root with arbitrary hash | Merkle Root Mismatch & Block Hash Mismatch |
| **TAMPER-07** | Broken Hash Link | Overwriting Block 2 `prev_hash` to break chain | Broken Previous Block Hash Linkage |
| **TAMPER-08** | Event Reordering | Swapping order of two legitimate events in Block 2 | Merkle Root Mismatch |
| **TAMPER-09** | Forged Block Hash | Overwriting Block 1 `block_hash` directly | Stored Block Hash Mismatch & Broken Link in Block 2 |
| **TAMPER-10** | Copy ID Alteration | In-place change of `copy_id` inside Block 2 Event 0 | Merkle Root Mismatch & Ed25519 Signature Invalidity |

### 3.4 Audit Engine Verification Workflow
The audit algorithm (`ledger.verify_ledger_integrity()`) evaluates:
1. Genesis block invariants (`index == 0`, `prev_hash == "0"*64`).
2. Hash linkage continuity ($\text{Block}_i.\text{prev\_hash} == \text{Block}_{i-1}.\text{block\_hash}$).
3. Merkle root recalculation from SHA-256 leaf digests of constituent events.
4. Block header SHA-256 hash recalculation.
5. Ed25519 cryptographic signature verification using the custodian's registered public key.

### 3.5 Pass/Fail Criteria
* **Pass:** Exactly 10 out of 10 attack vectors flagged as `COMPROMISED` ($100\%$) with zero undetected mutations.
* **Fail:** Any attack vector evades audit detection ($< 100\%$).

---

## 4. Test 3: Event-Logging Latency and Cost

### 4.1 Original Objective & Success Target
* **Target:** No more than **5.0 seconds** elapsed time per event and **₹0 (INR 0)** estimated cost.
* **Comparator Baseline:** Manual paper register entry (documented operational baseline: 30 to 60 seconds per physical handover).

### 4.2 Measurement Methodology
* **Measurement Instrumentation:** High-precision monotonic timer `time.perf_counter_ns()` with sub-microsecond resolution.
* **Sample Size:** 50 consecutive access events across 8 operational custody stages (`PAPER_GENERATED`, `DISPATCHED_TO_CENTER`, `RECEIVED_AT_CENTER`, `VAULT_DEPOSITED`, `SEAL_VERIFIED`, `EXAM_HALL_TRANSFERRED`, `DISTRIBUTED_TO_STUDENT`, `SURPLUS_RETURNED`).
* **Operations Included in Elapsed Time:**
  1. Memory allocation and canonical payload serialization.
  2. Ed25519 asymmetric private-key digital signing (256-bit curve).
  3. Ed25519 public-key signature verification.
  4. Ingestion into pending ledger transaction pool.
* **Cost Accounting Model:**
  * Public permissionless networks (e.g., Ethereum, Polygon) require gas fees ($>\text{₹5}$ to $\text{₹150}$ per transaction).
  * Our architecture employs a local permissioned ledger deployed on existing institutional infrastructure. Transaction fees are strictly **₹0**.

### 4.3 Pass/Fail Criteria
* **Pass:** Mean event processing latency $\le 5.0\text{ s}$, maximum latency $\le 5.0\text{ s}$, failed operations $= 0$, and incurred transaction fee $= \text{₹0}$.
* **Fail:** Any operation exceeds $5.0\text{ s}$ or incurs non-zero transaction fees.

---

## 5. Stop Rule & Risk Protocol

If any of the following failure triggers occur during testing:
1. Fingerprint accuracy falls below $70\%$ under digital transformations;
2. Ledger audit engine fails to detect deliberate tampering mutations;
3. Event latency exceeds the 5.0-second real-time operational threshold;

**Mandatory Action:** Testing must be halted immediately. The engineering team must not silently alter test samples. Instead, the team must:
* Document the root cause in `Known_Limitations.md`;
* Re-evaluate the multi-layer steganography scheme;
* Prepare to pivot to the alternative concept documented in Phase 2: **I02 — Signed Custody History** (relying purely on physical custodian-signed transfer events rather than document watermarking).
