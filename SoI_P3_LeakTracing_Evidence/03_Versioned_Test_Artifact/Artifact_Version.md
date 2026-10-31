# Versioned Test Artifact Specification

* **Artifact Identifier:** `SoI-P3-LeakTracing-v0.3.0`
* **Semantic Version:** `v0.3.0-poc`
* **Git Commit Hash:** `d40487ae9053fe7cfc280328a076b03646011763`
* **Repository Path:** `e:\bw`
* **Build / Frozen Date:** 31 October 2026
* **Verification Status:** Verified & Frozen for Reviewer Audit

---

## 1. Provenance and Environment Baseline

The software artifact evaluated under the Phase 3 Frozen Test Protocol was built and executed under the following certified environment:

| Attribute | Specification | Verification Command |
| :--- | :--- | :--- |
| **Operating System** | Windows 11 Enterprise (Build 10.0.26300, AMD64) | `[System.Environment]::OSVersion` |
| **Python Runtime** | Python 3.12.10 (CPython, 64-bit) | `python --version` |
| **Asymmetric Crypto Engine** | `cryptography` v50.0.2 (OpenSSL/hazmat backend) | `python -c "import cryptography; print(cryptography.__version__)"` |
| **Imaging & Raster Engine** | `Pillow (PIL)` v12.3.0 | `python -c "import PIL; print(PIL.__version__)"` |
| **VCS Commit Baseline** | Git 2.52.0 (`commit d40487a`) | `git rev-parse HEAD` |
| **Execution Host Timestamp** | 2026-10-31T16:18:54Z | Monotonic Perf Counter UTC |

---

## 2. Cryptographic Source Code Manifest (SHA-256 Checksums)

To guarantee that no files were altered post-testing, the SHA-256 hashes of all source code files comprising artifact `v0.3.0-poc` are recorded below:

| File Path | SHA-256 Digest | Status |
| :--- | :--- | :--- |
| `src/__init__.py` | `e5c712ac739eb6edcb105a162ce45984c793cccbb72fc1dc00c25d6abed9bd1b` | Frozen |
| `src/crypto.py` | `93b9f6bb62bfb4722ecf70446bfb18e6e2bd3ad6b5c62443eb7a0c065f2b2a11` | Frozen |
| `src/models.py` | `aedb2e20be6fe35916783c0b659b05da97a77ce40583c6cfcc2df0e82617ff28` | Frozen |
| `src/paper_generator.py` | `a58b83da93f105ce1a3cabb1299548b3f059e5e5100fa3b4eaff3d38027a3011` | Frozen |
| `src/fingerprint.py` | `9ec04b92c1cb5762c2c0d4840d67236a575ca774fdca6d661db634b8e05bc510` | Frozen |
| `src/ledger.py` | `d55c8b6e984735e697d23ee1045348f44560fbe55ee1340f423f7a046e77605e` | Frozen |
| `src/leak_tracer.py` | `93eab5cbd2684d1e603763fcf6e6f27d54e3b74b284f49dd160ffa301dbff76f` | Frozen |
| `src/cli.py` | `f4528213ea4c72e03370902f801b362cbfcc961c14d98f152852ac0b0af0cedc` | Frozen |
| `tests/run_all_tests.py` | Executed directly to produce `04_Raw_Test_Logs/` | Frozen |

---

## 3. Artifact Packaging and Reproducibility

This artifact is self-contained within the repository. To re-instantiate this exact build:
1. Ensure Python 3.12 is active.
2. Install exact dependencies:
   ```bash
   pip install cryptography==50.0.2 pillow==12.3.0
   ```
3. Run the automated audit script:
   ```bash
   python tests/run_all_tests.py
   ```
4. Verify that generated CSV digests match the expected test execution run ID: `RUN-SOI-P3-20261031-161854`.
