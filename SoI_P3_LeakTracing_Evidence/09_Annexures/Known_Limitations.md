# Technical Annexure 3: Known Limitations & Threat Model Boundaries

* **Project Title:** Blockchain-Based Leak Tracing for Examination Question Papers
* **Concept:** I01 — Fingerprinted Copies + Blockchain Access Ledger
* **Artifact Version:** `v0.3.0-poc`
* **Status:** Critical Audit & Failure Analysis

---

## 1. Executive Statement on Honest Constraints

Academic integrity requires explicit disclosure of engineering limitations. The prototype developed in Phase 3 proves core feasibility under controlled experimental conditions, but reviewers and institutional stakeholders must consider the following real-world limitations prior to campus-wide deployment.

---

## 2. Fingerprint Degradation & Attack Vulnerabilities

### 2.1 Zero-Width Unicode Steganography (Layer 1)
* **Vulnerability:** Zero-width characters (`\u200b`, `\u200c`, `\u200d`) exist solely as digital byte representations.
* **Failure Modes:**
  * Converting text to pure ASCII (`text.encode('ascii', 'ignore')`) strips all zero-width characters completely.
  * Human retyping on a physical keyboard automatically strips all zero-width characters.
  * Text sanitization pipelines in certain web forms and SMS gateways discard zero-width spaces.

### 2.2 Syntactic & Lexical Permutations (Layer 2)
* **Vulnerability:** Depends upon verbatim transcription of specific clauses and delimiters.
* **Failure Modes:**
  * **Paraphrasing / LLM Rewriting:** If an adversary passes leaked questions through an AI rephraser (e.g., "rewrite these exam questions in your own words"), all instruction prefixes and syntactic markers are erased.
  * **Selective Excerpting:** If a leaker only leaks a single question (e.g., "What is BFT?") without instructions or headers, the syntactic variation vector cannot be calculated, resulting in an ambiguous or unmatched verdict.
  * **Keyspace Saturation:** A 4-feature, 4-variation system yields $4^4 = 256$ unique copies. Scaling to 10,000 university students requires at least 14 independent lexical variation points across the paper.

### 2.3 Visual Corner Micro-Patterns (Layer 3)
* **Vulnerability:** Requires spatial preservation of page margins.
* **Failure Modes:**
  * **Cropping:** If a leaker crops out the top-right corner or captures only the center questions with a phone camera, the micro-grid pattern is lost.
  * **Extreme Perspective Skew & Lens Distortion:** Angled smartphone photographs without homographic un-warping prevent accurate binary cell grid alignment.

---

## 3. False Matches & Ambiguity Handling

* **Risk of False Attribution:** In high-stakes examination malpractice investigations, a false match could falsely accuse an innocent examination superintendent of leaking a paper.
* **Mitigation Built into Prototype:**
  * The algorithm enforces a strict separation threshold (minimum score gap $\ge 3$) for syntactic matches.
  * If scores tie, the system explicitly outputs `AMBIGUOUS` rather than guessing.
  * Single-layer clues must be treated as circumstantial leads, requiring corroboration with physical custody records and access timestamps.

---

## 4. Key Management & Identity Verification

* **Private Key Security:** In this PoC, Ed25519 keys are generated in memory and stored in test files.
* **Operational Risk:** If an examination center superintendent's laptop is compromised, an attacker could forge custody signatures or steal credentials.
* **Required Production Upgrade:** Production deployment mandates Hardware Security Modules (HSM) or FIDO2 cryptographic USB tokens (e.g., YubiKeys) ensuring private keys cannot be extracted.

---

## 5. Privacy vs. Auditability Trade-Off

* **GDPR / DPDP Compliance:** Logging custodian names, center codes, and exact timestamps to an immutable ledger creates an unalterable permanent record.
* **Mitigation:** In our architecture, the ledger stores pseudonymous `custodian_id` hashes (`CUST-03-SUPT`) and public keys. The mapping of custodian IDs to real legal identities is held in a confidential institutional directory accessible only to authorized inquiry committees.

---

## 6. Physical Document Access Outside Software Scope

* **The "Analog Hole":** Software and blockchain cannot prevent an authorized custodian from physically reading the paper or whispering question topics to a third party.
* **Scope Boundary:** Blockchain access ledgers record *custodial possession transitions*, not physical human gaze. The system establishes accountability for who possessed physical copies when a leak occurred, narrowing suspect pools from hundreds to specific individuals.

---

## 7. Blockchain Scalability & Consensus Boundaries

* **Single-Node vs. Multi-Node:** The Phase 3 PoC runs as a local append-only permissioned ledger to achieve high throughput ($0.25\text{ ms}$ latency) and zero transaction fees.
* **Decentralization Target:** A production system requires multi-institution validator nodes running Practical Byzantine Fault Tolerance (PBFT) or Raft consensus. Network latency across university campuses will increase block commit times to approximately 500 ms – 2 seconds, which remains well within the 5.0-second success criterion.
