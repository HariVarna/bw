"""Synthetic Examination Question Paper Generator."""

from __future__ import annotations

import random
from typing import Optional

from .models import QuestionPaper


def generate_synthetic_question_paper(
    paper_id: str = "QP-2026-CS801-AUTUMN",
    seed: Optional[int] = 42,
) -> QuestionPaper:
    """Generate a realistic, standardized university engineering question paper."""
    rng = random.Random(seed)

    instructions = [
        "Answer ALL questions in Part A and any FIVE questions from Part B.",
        "Standard scientific calculators are permitted; programmable calculators and mobile devices are strictly prohibited.",
        "Assume suitable missing data if any, and state the assumptions clearly.",
        "Write answers legibly; marks are allocated based on technical rigor and clarity.",
    ]

    part_a_questions = [
        {"text": "State the Byzantine Generals Problem and define Byzantine Fault Tolerance (BFT).", "marks": 2},
        {"text": "Differentiate between Proof of Work (PoW) and Proof of Stake (PoS) consensus mechanisms.", "marks": 2},
        {"text": "Define cryptographic hash collision resistance and preimage resistance.", "marks": 2},
        {"text": "Explain the role of the Merkle Tree root in SPV (Simplified Payment Verification) nodes.", "marks": 2},
        {"text": "What is an UTXO? How does it prevent the double-spending problem?", "marks": 2},
        {"text": "Describe the operational difference between public permissionless and consortium blockchains.", "marks": 2},
        {"text": "What are zero-knowledge proofs (ZKP)? Name two practical applications.", "marks": 2},
        {"text": "Explain the significance of nonce in block header construction.", "marks": 2},
        {"text": "How does asymmetric cryptography ensure non-repudiation in digital transactions?", "marks": 2},
        {"text": "Define smart contract reentrancy vulnerability and how it is mitigated.", "marks": 2},
    ]

    part_b_questions = [
        {
            "text": "Design a permissioned ledger protocol for high-security academic document custody. Include block structure, participant roles, and Merkle tree validation.",
            "marks": 16,
        },
        {
            "text": "Analyze the security vulnerabilities of zero-width steganography versus robust visual micro-watermarking under aggressive image compression and optical character recognition (OCR).",
            "marks": 16,
        },
        {
            "text": "Construct a complete consensus verification algorithm for a 4-node PBFT network under one malicious validator node.",
            "marks": 16,
        },
        {
            "text": "Explain the mechanics of elliptic curve digital signatures (Ed25519 vs ECDSA secp256k1). Evaluate key generation, signature generation, and verification complexity.",
            "marks": 16,
        },
        {
            "text": "Discuss the privacy-preservation versus auditability trade-off in distributed ledgers for national examination logistics.",
            "marks": 16,
        },
    ]

    return QuestionPaper(
        paper_id=paper_id,
        course_code="CS801",
        course_title="Distributed Ledger Technologies & Cryptographic Systems",
        exam_date="2026-11-15",
        duration_minutes=180,
        max_marks=100,
        instructions=instructions,
        sections=[
            {"title": "PART A — (10 x 2 = 20 Marks)", "marks": 20, "questions": part_a_questions},
            {"title": "PART B — (5 x 16 = 80 Marks)", "marks": 80, "questions": part_b_questions},
        ],
    )
