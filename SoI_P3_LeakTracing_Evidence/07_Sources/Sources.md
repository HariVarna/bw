# Sources and Technical References

* **Project Title:** Blockchain-Based Leak Tracing for Examination Question Papers
* **Concept:** I01 — Fingerprinted Copies + Blockchain Access Ledger
* **Document Status:** Complete & Audited
* **Date of Compilation:** 31 October 2026

---

## 1. Cryptographic and Ledger Foundations

### 1.1 Ed25519 Digital Signatures
* **Title:** RFC 8032: Edwards-Curve Digital Signature Algorithm (EdDSA)
* **Authors:** S. Josefsson, I. Liusvaara
* **URL:** https://datatracker.ietf.org/doc/html/rfc8032
* **Access Date:** October 2026
* **Application in Project:** Basis for asymmetric custodian key generation and digital non-repudiation across all access events in `src/crypto.py`.

### 1.2 Secure Hash Standard (SHA-256)
* **Title:** FIPS PUB 180-4: Secure Hash Standard (SHS)
* **Publisher:** National Institute of Standards and Technology (NIST)
* **URL:** https://csrc.nist.gov/publications/detail/fips/180-4/final
* **Access Date:** October 2026
* **Application in Project:** Utilized for block header hash chaining, event payload digest generation, and Merkle tree leaf computations.

### 1.3 Merkle Tree Structures
* **Title:** A Certified Digital Signature
* **Author:** Ralph C. Merkle
* **Publication:** Advances in Cryptology — CRYPTO '89, Lecture Notes in Computer Science, Vol 435. Springer, New York, NY.
* **URL:** https://link.springer.com/chapter/10.1007/0-387-34805-0_21
* **Access Date:** October 2026
* **Application in Project:** Algorithm used in `src/crypto.py` (`compute_merkle_root`) to summarize batch events into immutable block headers.

### 1.4 Cryptographic Blockchain Architecture
* **Title:** Bitcoin: A Peer-to-Peer Electronic Cash System
* **Author:** Satoshi Nakamoto (2008)
* **URL:** https://bitcoin.org/bitcoin.pdf
* **Access Date:** October 2026
* **Application in Project:** Conceptual reference for linear previous-block hash linkage (`prev_hash`) and timestamped block sequencing.

---

## 2. Document Fingerprinting & Steganography References

### 2.1 Unicode Steganography (Zero-Width Characters)
* **Title:** Unicode Standard Annex #44: Unicode Character Database (Zero-Width Spaces U+200B, U+200C, U+200D)
* **Publisher:** The Unicode Consortium
* **URL:** https://www.unicode.org/reports/tr44/
* **Access Date:** October 2026
* **Application in Project:** Standard specifications for zero-width space characters used to construct Layer 1 binary-encoded document fingerprints.

### 2.2 Syntactic and Lexical Watermarking
* **Title:** Natural Language Watermarking: Challenges, Techniques, and Future Directions
* **Authors:** M. Atallah et al. (Purdue University)
* **URL:** https://www.cerias.purdue.edu/assets/pdf/bibtex_archive/2001-44.pdf
* **Access Date:** October 2026
* **Application in Project:** Formulation of Layer 2 syntactic permutations for preserving watermark signals through human retyping and paraphrasing.

---

## 3. Software Frameworks and Open-Source Libraries

### 3.1 Python Cryptography Library
* **Title:** `cryptography` Package (pyca/cryptography)
* **URL:** https://cryptography.io/en/latest/
* **Version:** 50.0.2
* **Application in Project:** High-assurance Python bindings for Ed25519 digital signatures (`cryptography.hazmat.primitives.asymmetric.ed25519`).

### 3.2 Python Imaging Library (Pillow)
* **Title:** Pillow: The Friendly Python Imaging Library Fork
* **URL:** https://python-pillow.org/
* **Version:** 12.3.0
* **Application in Project:** Rendering examination paper raster artifacts and simulating screenshot and print-scan degradation filters.

### 3.3 Python CPython Standard Library
* **Title:** The Python Standard Library Documentation (Release 3.12.10)
* **Publisher:** Python Software Foundation
* **URL:** https://docs.python.org/3.12/library/
* **Application in Project:** Native modules `hashlib`, `json`, `statistics`, `time`, and `argparse`.
