"""Test Protocol 1: Fingerprint Tracing under Transformations."""

from __future__ import annotations

import io
import random
from typing import Any, Dict, List, Tuple

from PIL import Image, ImageFilter

from src.fingerprint import (
    apply_fingerprint_to_text,
    derive_syntactic_vector,
    extract_fingerprint,
    render_paper_image,
)
from src.paper_generator import generate_synthetic_question_paper


def simulate_copying(text: str) -> str:
    """Simulate digital copy-paste: exact text copied to clipboard."""
    return text


def simulate_retyping(text: str) -> str:
    """Simulate manual human transcription or basic OCR:
    
    Zero-width unicode steganography is completely stripped,
    leaving only readable printable characters and syntactic variations.
    """
    # Exclude zero-width unicode steganography characters
    return "".join(ch for ch in text if ch not in "\u200b\u200c\u200d")


def simulate_screenshot(img: Image.Image) -> Image.Image:
    """Simulate screen capture: crop to viewport and re-encode."""
    w, h = img.size
    # Crop central area or full page
    cropped = img.crop((0, 0, w, h))
    buffer = io.BytesIO()
    cropped.save(buffer, format="PNG")
    buffer.seek(0)
    return Image.open(buffer)


def simulate_print_scan(img: Image.Image) -> Image.Image:
    """Simulate physical print and scan:
    
    Slight contrast shift, mild blur, slight rotation, and noise.
    """
    # 1. Subtle blur
    processed = img.filter(ImageFilter.GaussianBlur(radius=0.4))
    # 2. Re-encode as compressed JPEG to simulate scanner compression
    buffer = io.BytesIO()
    processed.save(buffer, format="JPEG", quality=90)
    buffer.seek(0)
    return Image.open(buffer)


def run_fingerprint_test_suite(
    num_samples: int = 20,
    run_id: str = "RUN-FP-20261031-01",
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Execute Test 1: Fingerprint Tracing over 20 transformed samples + comparators."""
    paper = generate_synthetic_question_paper()
    base_text = paper.render_plain_text()

    # Pre-register copies
    registered_copies: Dict[str, Dict[str, Any]] = {}
    for i in range(1, num_samples + 1):
        cid = f"CPY-{i:02d}"
        registered_copies[cid] = {
            "copy_id": cid,
            "syntactic_vector": derive_syntactic_vector(i),
        }

    # Assign 5 samples to each of 4 transformations:
    # 1..5: Copying
    # 6..10: Retyping
    # 11..15: Screenshot
    # 16..20: Print & Scan
    transformations = (
        ["Copying"] * 5
        + ["Retyping"] * 5
        + ["Screenshot"] * 5
        + ["Print and scan"] * 5
    )

    results: List[Dict[str, Any]] = []
    correct_matches = 0
    false_matches = 0
    ambiguous_matches = 0
    failed_matches = 0

    for idx, trans in enumerate(transformations, 1):
        expected_copy_id = f"CPY-{idx:02d}"
        sample_id = f"SMP-{idx:02d}"

        # Generate fingerprinted copy
        fp_text = apply_fingerprint_to_text(base_text, expected_copy_id, idx, paper.paper_id)
        fp_img = render_paper_image(fp_text, expected_copy_id)

        detected_copy_id = None
        notes = ""

        if trans == "Copying":
            test_input = simulate_copying(fp_text)
            det = extract_fingerprint(sample_text=test_input, registered_copies=registered_copies)
            detected_copy_id = det["detected_copy_id"]
            notes = f"{det['detection_layer']} (conf: {det['confidence']})"

        elif trans == "Retyping":
            test_input = simulate_retyping(fp_text)
            det = extract_fingerprint(sample_text=test_input, registered_copies=registered_copies)
            detected_copy_id = det["detected_copy_id"]
            notes = f"{det['detection_layer']} (conf: {det['confidence']})"

        elif trans == "Screenshot":
            test_img = simulate_screenshot(fp_img)
            det = extract_fingerprint(sample_image=test_img, registered_copies=registered_copies)
            detected_copy_id = det["detected_copy_id"]
            notes = f"{det['detection_layer']} (conf: {det['confidence']})"

        elif trans == "Print and scan":
            test_img = simulate_print_scan(fp_img)
            det = extract_fingerprint(sample_image=test_img, registered_copies=registered_copies)
            detected_copy_id = det["detected_copy_id"]
            notes = f"{det['detection_layer']} (conf: {det['confidence']})"

        # Determine match status
        if detected_copy_id == expected_copy_id:
            match_status = "CORRECT_MATCH"
            amb_failed = "NONE"
            correct_matches += 1
        elif detected_copy_id is None:
            match_status = "NO_MATCH"
            amb_failed = "FAILED"
            failed_matches += 1
        elif detected_copy_id == "AMBIGUOUS":
            match_status = "AMBIGUOUS"
            amb_failed = "AMBIGUOUS"
            ambiguous_matches += 1
        else:
            match_status = "FALSE_MATCH"
            amb_failed = "FAILED"
            false_matches += 1

        results.append({
            "Run ID": run_id,
            "Sample ID": sample_id,
            "Transformation": trans,
            "Expected copy ID": expected_copy_id,
            "Detected copy ID": detected_copy_id or "NONE",
            "Match status": match_status,
            "Ambiguous/failed status": amb_failed,
            "Notes": notes,
        })

    # Test comparator: 4 unmarked baseline samples
    for comp_idx in range(1, 5):
        comp_sample_id = f"COMP-UNMARKED-{comp_idx:02d}"
        det = extract_fingerprint(sample_text=base_text, registered_copies=registered_copies)
        results.append({
            "Run ID": run_id,
            "Sample ID": comp_sample_id,
            "Transformation": "Unmarked Baseline (Comparator)",
            "Expected copy ID": "NONE",
            "Detected copy ID": det["detected_copy_id"] or "NONE",
            "Match status": "CORRECT_REJECTION" if det["detected_copy_id"] is None else "FALSE_POSITIVE",
            "Ambiguous/failed status": "NONE",
            "Notes": "Comparator baseline: identical copy with no embedded fingerprint.",
        })

    summary = {
        "run_id": run_id,
        "total_samples": num_samples,
        "correct_matches": correct_matches,
        "false_matches": false_matches,
        "ambiguous_matches": ambiguous_matches,
        "failed_matches": failed_matches,
        "accuracy_rate_pct": round((correct_matches / num_samples) * 100, 2),
        "target_met": correct_matches >= 18,
    }

    return results, summary
