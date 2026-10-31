# AI Assistance Disclosure

* **Institution:** School of Innovation
* **Academic Year:** 2026–27 | **Phase:** Phase 3: Proof of Concept
* **Project Title:** Blockchain-Based Leak Tracing for Examination Question Papers
* **Project Team:** Hari Varna V S, Harshavardini D, Kavin Kumar V, Mohanavel N
* **Date:** 31 October 2026

---

## 1. Principles of Academic Transparency

In accordance with the School of Innovation Policy on Artificial Intelligence in Research and Prototyping, this disclosure details the scope, nature, and boundaries of AI tool assistance utilized during Phase 3 development.

---

## 2. Scope of AI Assistance

The project team utilized AI assistance (DeepMind Antigravity / Gemini 3.8 Flash) for the following specific technical activities:

1. **Test Runner & Harness Scaffolding:**
   * Automated creation of parameterized test scripts (`tests/test_fingerprint.py`, `tests/test_ledger_integrity.py`, `tests/test_event_timing.py`) implementing the frozen test criteria from the Phase 2 Ideation document.
   * Structuring high-precision timing routines using `time.perf_counter_ns()`.

2. **Modular Code Architecture & Boilerplate:**
   * Implementing standard cryptographic wrapper functions (`src/crypto.py`) interfacing with the Python `cryptography` library for Ed25519 signing.
   * Generating synthetic university question paper text and structures (`src/paper_generator.py`).

3. **Documentation Structuring & Standardization:**
   * Formatting evidence indexes, Markdown annexures, and tables adhering to institutional Phase 3 submission templates.
   * Debugging console character encoding compatibility (`cp1252` on Windows hosts).

---

## 3. Human Engineering Responsibilities & Validation

The student project team maintains primary intellectual ownership of the system architecture. Specifically:
* **Ideation & Concept Formulation:** The selected concept (*I01 — Fingerprinted Copies + Blockchain Access Ledger*) and frozen success criteria were formulated by the team on 16 October 2026 prior to AI code generation.
* **Cryptographic & Forensic Design:** The multi-layer defense-in-depth model (separating digital steganography, syntactic variation, and visual micro-patterns) was designed and validated by the team.
* **Code Review & Audit:** Every script and module was reviewed, compiled, and executed locally on team hardware under Windows 11.
* **Integrity Guarantee:** AI was not used to synthesize fake test results, fabricate transaction hashes, or alter test logs. All quantitative measurements in `04_Raw_Test_Logs/` represent genuine local runtime execution outputs.

---

## 4. Attestation

We affirm that all statements regarding system capabilities, test execution, and limitations in this evidence package are truthful and accurately reflect the actual prototype.

*Signed by Project Team Members:*
* Hari Varna V S
* Harshavardini D
* Kavin Kumar V
* Mohanavel N
