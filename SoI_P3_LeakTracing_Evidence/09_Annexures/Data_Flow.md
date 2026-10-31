# Technical Annexure 2: End-to-End Data Flow

* **Project Title:** Blockchain-Based Leak Tracing for Examination Question Papers
* **Concept:** I01 — Fingerprinted Copies + Blockchain Access Ledger
* **Artifact Version:** `v0.3.0-poc`

---

## 1. Overview of Lifecycle Stages

The complete lifecycle consists of seven sequential data-flow stages:

```
[1. Paper Generation] 
        │
        ▼
[2. Copy ID Assignment & Manifest Registration]
        │
        ▼
[3. Multi-Layer Fingerprint Embedding] ───► (Text / PNG Artifacts)
        │
        ▼
[4. Custody Access-Event Creation (Ed25519 Signing)]
        │
        ▼
[5. Blockchain Ledger Ingestion & Block Mining]
        │
        ▼  <=== [LEAK EVENT OCCURS] ===>
        │
[6. Leaked Artifact Ingestion & Forensic Decoding]
        │
        ▼
[7. Ledger Audit Query & Custodial Dossier Output]
```

---

## 2. Detailed Data-Flow Walkthrough

### Stage 1: Synthetic Paper Creation
* **Initiator:** Controller of Examinations (COE) / Confidential Press Officer.
* **Input Data:** Course details (`CS801`), date (`2026-11-15`), duration (`180 mins`), question bank.
* **Processing:** `generate_synthetic_question_paper()` compiles structured sections and instructions.
* **Output:** Master question paper text string ($M_{\text{base}}$).

### Stage 2: Copy ID Assignment & Manifest Registration
* **Input:** Number of required examination copies ($N = 20$).
* **Processing:** 
  * Each copy is assigned a sequential identifier $C_i = \text{"CPY-" + formatted}(i)$.
  * Deterministic base-4 vector $V_i = [v_{i,0}, v_{i,1}, v_{i,2}, v_{i,3}]$ is derived from $i-1$.
  * Mapping $\{C_i \rightarrow (\text{Custodian}_j, V_i)\}$ is committed to `manifest.json`.

### Stage 3: Multi-Layer Fingerprint Embedding
* **Layer 1 (Zero-Width Steganography):**
  * Copy string $C_i$ converted to 8-bit binary ASCII.
  * Encoded into zero-width unicode: $0 \rightarrow \text{ZWSP } (\verb|\u200b|)$, $1 \rightarrow \text{ZWNJ } (\verb|\u200c|)$.
  * Framed by $\verb|\u200d|$ and inserted into the document header.
* **Layer 2 (Syntactic Variation):**
  * Instruction prefix formatted via rule $V_i[0]$.
  * Calculator phrase substituted via rule $V_i[1]$.
  * Mobile phone clause substituted via rule $V_i[2]$.
  * Part A delimiter formatted via rule $V_i[3]$.
* **Layer 3 (Visual Corner Grid):**
  * Text rendered to 1200x1600 canvas using Pillow.
  * Top-right corner $4\times 4$ binary pixel grid drawn based on integer index $i$.
  * Faint tiled background watermark overlaid.
* **Output:** Stored as `copies/CPY-xx.txt` and `copies/CPY-xx.png`.

### Stage 4: Access-Event Creation & Digital Signing
* **Event Structure:**
  ```json
  {
    "event_id": "EV-DISP-CPY-05",
    "timestamp": "2026-10-31T09:30:00.000000+00:00",
    "paper_id": "QP-2026-CS801-AUTUMN",
    "copy_id": "CPY-05",
    "action": "DISPATCHED_TO_CENTER",
    "custodian_id": "CUST-03-SUPT",
    "custodian_pubkey": "base64_encoded_pubkey",
    "location": "CENTER-101",
    "metadata": { "courier_seal": "SEAL-882-5" }
  }
  ```
* **Signing:**
  * Event payload deterministically sorted and serialized to bytes via `canonical_json_bytes()`.
  * Custodian computes Ed25519 signature: $\text{Sig} = \text{Sign}(K_{\text{priv}}, \text{Payload})$.

### Stage 5: Blockchain Ledger Recording & Block Mining
1. Ingestion node verifies $\text{Verify}(K_{\text{pub}}, \text{Payload}, \text{Sig}) == \text{True}$.
2. Event appended to `pending_events` pool.
3. Once batch threshold is reached (or on dispatch trigger), `ledger.commit_block()` is invoked:
   * Event SHA-256 digests computed: $h_k = \text{SHA256}(\text{Event}_k)$.
   * Merkle Root computed via hierarchical pairwise SHA-256 hashing.
   * New block constructed with `prev_hash` pointing to previous block's hash.
   * Block hash computed: $\text{Hash} = \text{SHA256}(\text{Header})$.
   * Chain written to disk store (`ledger.json`).

### Stage 6: Recovered-Copy Forensic Ingestion
When a leaked excerpt surfaces:
1. **Input:** Plain text excerpt or photographic image file.
2. **Layer 1 Check:** Regex scan for $\verb|\u200d[\u200b\u200c]+\u200d|$. If present, decodes binary bits $\rightarrow$ extracts Copy ID.
3. **Layer 3 Check (if Image):** Reads bounding box coordinates $(W-80, 40)$, samples luminance values of 16 grid cells $\rightarrow$ decodes binary integer $\rightarrow$ recovers Copy ID.
4. **Layer 2 Check (if plain text without ZW characters):** Evaluates syntactic phrasing against `manifest.json`. Highest separated candidate score $\rightarrow$ recovers Copy ID.

### Stage 7: Forensic Investigation Output & Dossier
1. Extracted Copy ID is passed to `ledger.get_events_for_copy(copy_id)`.
2. All historical custody blocks containing matching events are filtered.
3. Events sorted chronologically.
4. Final custodian, timestamp, location, and action extracted.
5. Cryptographic integrity of each signature in the custody chain re-verified.
6. Structured investigative report printed to console or exported to JSON.
