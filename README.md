# Blockchain-Based Leak Tracing for Examination Question Papers

**School of Innovation (SoI) — AY 2026–27 | Phase 3: Proof of Concept**

* **Selected Concept:** I01 — Fingerprinted Copies + Blockchain Access Ledger
* **Project Team:**
  * Hari Varna V S
  * Harshavardini D
  * Kavin Kumar V
  * Mohanavel N
* **Batch:** 2025–29 | **Vertical:** Blockchain
* **Faculty Mentor:** Selva Kumar

---

## Quick Navigation

* **Official Evidence Package:** [`SoI_P3_LeakTracing_Evidence/`](SoI_P3_LeakTracing_Evidence/README.md)
* **Master Evidence Index:** [`Evidence_Index.md`](SoI_P3_LeakTracing_Evidence/00_Evidence_Index/Evidence_Index.md)
* **Frozen Test Protocol:** [`Frozen_Test_Protocol.md`](SoI_P3_LeakTracing_Evidence/01_Frozen_Test_Protocol/Frozen_Test_Protocol.md)
* **Raw Execution Logs (CSV/JSON):** [`04_Raw_Test_Logs/`](SoI_P3_LeakTracing_Evidence/04_Raw_Test_Logs/README.md)
* **Quantitative Calculations:** [`Calculations.md`](SoI_P3_LeakTracing_Evidence/05_Calculations/Calculations.md)
* **Replay & Reproducibility Guide:** [`Replay_README.md`](SoI_P3_LeakTracing_Evidence/06_Replay_Documentation/Replay_README.md)

---

## Quick Start

### 1. Web Application Dashboard (Recommended)

```powershell
# Install dependencies
pip install -r requirements.txt

# Launch Institutional Security Dashboard
python -m webapp.app
```
Open your browser at `http://127.0.0.1:5000` to access the cybersecurity investigation dashboard.

### 2. Automated Test Protocol & CLI Verification

```powershell
# Execute complete test protocol (generates raw logs & runs calculations)
python tests/run_all_tests.py

# Run automated webapp test suite
python -m pytest tests/test_webapp.py

# Run interactive CLI
python -m src.cli --help
```

---

## Web Application Navigation & Capabilities

* **Dashboard (`/dashboard`):** High-level metrics, live cryptographic ledger health check, interactive 7-stage workflow lifecycle diagram, recent activities, and 1-click demonstration dataset controls.
* **Examinations (`/examinations`):** Question paper generator and plain-text review.
* **Custodians (`/custodians`):** Institutional directory of examination officers and Ed25519 public keys.
* **Fingerprinted Copies (`/copies`):** Multi-layer serialized copies inspector (Layer 1 Zero-Width, Layer 2 Syntactic Permutation, Layer 3 Visual Corner Micro-Grid).
* **Access Ledger (`/ledger`):** Blockchain block explorer, Merkle root verifier, and live cryptographic audit.
* **Leak Investigation (`/investigation`):** Forensic leak attribution tool for text excerpts and images with pre-packaged demo samples.
* **Reports (`/reports`):** Official SoI Phase 3 Frozen Test Protocol results, raw CSV logs, and quantitative derivations.
* **System Information (`/system-info`):** Architectural specifications, cryptographic standards, and runtime diagnostics.
