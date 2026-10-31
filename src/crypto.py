"""Cryptographic utilities for Blockchain-Based Leak Tracing.

Provides:
- Ed25519 key generation, message signing, and signature verification
- SHA-256 cryptographic hashing
- Merkle root computation for access-event batches
- Canonical JSON serialization for deterministic digest calculation
"""

from __future__ import annotations

import base64
import hashlib
import json
from typing import Any, List

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519


def sha256_hex(data: bytes | str) -> str:
    """Compute SHA-256 digest of bytes or UTF-8 string."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(obj: Any) -> bytes:
    """Serialize object to deterministic canonical JSON bytes."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def generate_keypair() -> tuple[str, str]:
    """Generate Ed25519 key pair, returning (private_key_b64, public_key_b64)."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    priv_raw = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pub_raw = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    return base64.b64encode(priv_raw).decode("utf-8"), base64.b64encode(pub_raw).decode("utf-8")


def sign_message(private_key_b64: str, message_bytes: bytes) -> str:
    """Sign message bytes using Ed25519 private key, returning base64 signature."""
    priv_raw = base64.b64decode(private_key_b64)
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(priv_raw)
    sig_raw = private_key.sign(message_bytes)
    return base64.b64encode(sig_raw).decode("utf-8")


def verify_signature(public_key_b64: str, message_bytes: bytes, signature_b64: str) -> bool:
    """Verify Ed25519 signature over message bytes with public key."""
    try:
        pub_raw = base64.b64decode(public_key_b64)
        sig_raw = base64.b64decode(signature_b64)
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_raw)
        public_key.verify(sig_raw, message_bytes)
        return True
    except (InvalidSignature, ValueError, Exception):
        return False


def compute_merkle_root(leaf_hashes: List[str]) -> str:
    """Compute Merkle Root for a list of leaf SHA-256 hashes.
    
    If list is empty, returns SHA-256 of empty string.
    If list length is odd (and > 1), the last element is duplicated to form pairs.
    """
    if not leaf_hashes:
        return sha256_hex(b"")

    current_level = list(leaf_hashes)
    while len(current_level) > 1:
        next_level: List[str] = []
        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])
        for i in range(0, len(current_level), 2):
            combined = current_level[i] + current_level[i + 1]
            next_level.append(sha256_hex(combined.encode("utf-8")))
        current_level = next_level

    return current_level[0]
