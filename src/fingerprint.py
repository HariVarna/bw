"""Multi-Layer Fingerprint Generation and Extraction Module.

Implements three distinct fingerprinting layers:
1. Layer 1 (Zero-Width Unicode Steganography):
   Encodes Copy ID into invisible zero-width unicode characters (ZWSP, ZWNJ, ZWJ).
   Extremely robust to digital copy-paste; stripped by OCR and human retyping.

2. Layer 2 (Syntactic & Punctuation Permutation):
   Applies deterministic stylistic variations to instructions and section headers.
   Survives verbatim retyping and plain text extraction.

3. Layer 3 (Visual Micro-Watermarking & Steganographic Corner Patterns):
   Renders document pages as visual artifacts with low-contrast micro-markers
   and corner checksum patterns. Evaluated against screenshot and print/scan transformations.
"""

from __future__ import annotations

import base64
import json
import math
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Zero-width unicode constants
ZWSP = "\u200b"  # Zero-Width Space -> bit '0'
ZWNJ = "\u200c"  # Zero-Width Non-Joiner -> bit '1'
ZWJ = "\u200d"   # Zero-Width Joiner -> Frame Delimiter

# Syntactic permutation dictionaries (Layer 2)
SYNTACTIC_RULES = {
    "inst_prefix": [
        lambda i: f"  {i}. ",
        lambda i: f"  ({i}) ",
        lambda i: f"  [{i}] ",
        lambda i: f"  {i}) ",
    ],
    "calc_phrase": [
        "Standard scientific calculators are permitted;",
        "Standard scientific calculators are allowed;",
        "Use of standard scientific calculators is permitted;",
        "Scientific calculators (non-programmable) are permitted;",
    ],
    "mobile_phrase": [
        "mobile devices are strictly prohibited.",
        "cellular phones and digital devices are strictly prohibited.",
        "smart devices and phones are strictly barred.",
        "mobile phones are strictly forbidden.",
    ],
    "part_a_delim": [
        "PART A — (10 x 2 = 20 Marks)",
        "PART - A (10 x 2 = 20 MARKS)",
        "SECTION A: (10 x 2 = 20 Marks)",
        "PART A: (10 Questions x 2 = 20 Marks)",
    ],
}


@dataclass
class FingerprintManifest:
    paper_id: str
    copy_id: str
    custodian_id: str
    zw_payload: str
    syntactic_vector: List[int]
    visual_tag: str


def encode_string_to_zw(text: str) -> str:
    """Encode an ASCII string into zero-width binary characters enclosed by ZWJ delimiters."""
    binary_str = "".join(f"{ord(c):08b}" for c in text)
    zw_encoded = "".join(ZWSP if b == "0" else ZWNJ for b in binary_str)
    return f"{ZWJ}{zw_encoded}{ZWJ}"


def decode_zw_to_string(text: str) -> Optional[str]:
    """Extract and decode zero-width encoded payload from text. Returns None if not found."""
    # Find sequence between ZWJ delimiters
    pattern = f"{ZWJ}([\\{ZWSP}\\{ZWNJ}]+){ZWJ}"
    matches = re.findall(pattern, text)
    if not matches:
        return None

    for m in matches:
        if len(m) % 8 != 0:
            continue
        chars = []
        try:
            for i in range(0, len(m), 8):
                byte_bits = m[i : i + 8]
                byte_val = int("".join("0" if b == ZWSP else "1" for b in byte_bits), 2)
                chars.append(chr(byte_val))
            decoded = "".join(chars)
            if decoded.isalnum() or "-" in decoded or "_" in decoded:
                return decoded
        except Exception:
            continue
    return None


def derive_syntactic_vector(copy_idx: int) -> List[int]:
    """Derive deterministic index choices for syntactic variations based on copy index."""
    return [
        (copy_idx + 0) % len(SYNTACTIC_RULES["inst_prefix"]),
        (copy_idx + 1) % len(SYNTACTIC_RULES["calc_phrase"]),
        (copy_idx + 2) % len(SYNTACTIC_RULES["mobile_phrase"]),
        (copy_idx + 3) % len(SYNTACTIC_RULES["part_a_delim"]),
    ]


def apply_fingerprint_to_text(
    base_text: str,
    copy_id: str,
    copy_idx: int,
    paper_id: str,
) -> str:
    """Embed Layer 1 (Zero-width) and Layer 2 (Syntactic) into question paper text."""
    zw_payload = encode_string_to_zw(copy_id)
    vector = derive_syntactic_vector(copy_idx)

    # 1. Apply syntactic variations
    text = base_text
    # Replace default phrases with copy-specific variations
    default_calc = "Standard scientific calculators are permitted;"
    if default_calc in text:
        text = text.replace(default_calc, SYNTACTIC_RULES["calc_phrase"][vector[1]])

    default_mobile = "mobile devices are strictly prohibited."
    if default_mobile in text:
        text = text.replace(default_mobile, SYNTACTIC_RULES["mobile_phrase"][vector[2]])

    default_part_a = "PART A — (10 x 2 = 20 Marks)"
    if default_part_a in text:
        text = text.replace(default_part_a, SYNTACTIC_RULES["part_a_delim"][vector[3]])

    # 2. Embed zero-width payload after the paper header line
    lines = text.split("\n")
    if len(lines) > 2:
        lines[1] = lines[1] + zw_payload
    else:
        lines[0] = lines[0] + zw_payload

    return "\n".join(lines)


def render_paper_image(
    paper_text: str,
    copy_id: str,
    watermark_opacity: int = 18,
) -> Image.Image:
    """Render plain text paper into a high-resolution PIL Image with Layer 3 visual markers."""
    width, height = 1200, 1600
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Draw faint diagonal tiled watermark for visual layer
    wm_text = f"CONFIDENTIAL :: {copy_id} :: OFFICIAL"
    for y in range(100, height, 250):
        for x in range(50, width, 400):
            draw.text((x, y), wm_text, fill=(235, 235, 235))

    # Corner security micro-pattern encoding copy ID (4 corners)
    # Encodes integer copy ID into 8-pixel binary square in top-right corner
    try:
        copy_num = int("".join(filter(str.isdigit, copy_id)))
    except ValueError:
        copy_num = 1

    pattern_x, pattern_y = width - 80, 40
    # Frame bounding box
    draw.rectangle([pattern_x - 4, pattern_y - 4, pattern_x + 36, pattern_y + 36], outline=(180, 180, 180))
    for bit in range(16):
        bx = pattern_x + (bit % 4) * 8
        by = pattern_y + (bit // 4) * 8
        is_on = (copy_num >> bit) & 1
        color = (20, 20, 20) if is_on else (240, 240, 240)
        draw.rectangle([bx, by, bx + 6, by + 6], fill=color)

    # Draw text lines
    lines = paper_text.split("\n")
    y_cursor = 80
    for line in lines[:55]:  # fit on first page
        if line.startswith("="):
            draw.line([(60, y_cursor), (width - 60, y_cursor)], fill=(100, 100, 100), width=2)
            y_cursor += 15
        elif line.startswith("---") or line.startswith("PART"):
            draw.text((60, y_cursor), line, fill=(10, 10, 10))
            y_cursor += 28
        else:
            # Wrap long lines simply
            if len(line) > 95:
                line = line[:92] + "..."
            draw.text((60, y_cursor), line, fill=(30, 30, 30))
            y_cursor += 22

    # Draw footer
    draw.line([(60, height - 60), (width - 60, height - 60)], fill=(180, 180, 180), width=1)
    draw.text((60, height - 45), f"Page 1 of 1 | Security Tag: SEC-{copy_id}", fill=(120, 120, 120))

    return img


def extract_corner_tag(img: Image.Image) -> Optional[str]:
    """Extract integer copy number from top-right corner micro-pattern."""
    width, height = img.size
    pattern_x, pattern_y = width - 80, 40

    recovered_num = 0
    for bit in range(16):
        bx = pattern_x + (bit % 4) * 8 + 3
        by = pattern_y + (bit // 4) * 8 + 3
        if 0 <= bx < width and 0 <= by < height:
            pixel = img.getpixel((bx, by))
            # Grayscale intensity
            lum = (pixel[0] + pixel[1] + pixel[2]) // 3 if isinstance(pixel, tuple) else pixel
            if lum < 128:
                recovered_num |= (1 << bit)

    if recovered_num > 0:
        return f"CPY-{recovered_num:02d}"
    return None


def match_syntactic_fingerprint(
    text: str,
    registered_copies: Dict[str, Dict[str, Any]],
) -> Tuple[Optional[str], float]:
    """Score text against registered syntactic variations. Returns (best_copy_id, confidence_score)."""
    scores: Dict[str, int] = {cid: 0 for cid in registered_copies}

    for cid, meta in registered_copies.items():
        vector = meta.get("syntactic_vector", [])
        if len(vector) < 4:
            continue

        # Check calc phrase
        calc_target = SYNTACTIC_RULES["calc_phrase"][vector[1]]
        if calc_target in text:
            scores[cid] += 3

        # Check mobile phrase
        mobile_target = SYNTACTIC_RULES["mobile_phrase"][vector[2]]
        if mobile_target in text:
            scores[cid] += 3

        # Check part a delim
        part_a_target = SYNTACTIC_RULES["part_a_delim"][vector[3]]
        if part_a_target in text:
            scores[cid] += 3

    if not scores:
        return None, 0.0

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_cid, best_score = sorted_scores[0]
    second_score = sorted_scores[1][1] if len(sorted_scores) > 1 else 0

    max_possible = 9.0
    confidence = best_score / max_possible

    # Must have strict separation and at least 2 distinct matches to avoid ambiguity
    if best_score >= 6 and (best_score - second_score >= 3):
        return best_cid, round(confidence, 3)
    elif best_score > 0 and best_score == second_score:
        return "AMBIGUOUS", round(confidence, 3)

    return None, 0.0


def extract_fingerprint(
    sample_text: Optional[str] = None,
    sample_image: Optional[Image.Image] = None,
    registered_copies: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Comprehensive multi-layer fingerprint extraction pipeline."""
    result: Dict[str, Any] = {
        "detected_copy_id": None,
        "detection_layer": None,
        "confidence": 0.0,
        "status": "UNMATCHED",
        "notes": "",
    }

    # 1. Try Layer 1: Zero-Width Unicode Extraction
    if sample_text:
        zw_id = decode_zw_to_string(sample_text)
        if zw_id:
            result["detected_copy_id"] = zw_id
            result["detection_layer"] = "LAYER_1_ZERO_WIDTH"
            result["confidence"] = 1.0
            result["status"] = "MATCH_VERIFIED"
            result["notes"] = "Extracted exact bit payload from zero-width unicode steganography."
            return result

    # 2. Try Layer 3: Visual Image Pattern Extraction
    if sample_image:
        img_id = extract_corner_tag(sample_image)
        if img_id:
            result["detected_copy_id"] = img_id
            result["detection_layer"] = "LAYER_3_VISUAL_PATTERN"
            result["confidence"] = 0.95
            result["status"] = "MATCH_VERIFIED"
            result["notes"] = "Decoded visual micro-pattern from high-contrast corner cell grid."
            return result

    # 3. Try Layer 2: Syntactic & Punctuation Permutation
    if sample_text and registered_copies:
        syn_id, conf = match_syntactic_fingerprint(sample_text, registered_copies)
        if syn_id == "AMBIGUOUS":
            result["detected_copy_id"] = None
            result["detection_layer"] = "LAYER_2_SYNTACTIC"
            result["confidence"] = conf
            result["status"] = "AMBIGUOUS"
            result["notes"] = "Syntactic score tied between multiple copies; insufficient resolution."
            return result
        elif syn_id:
            result["detected_copy_id"] = syn_id
            result["detection_layer"] = "LAYER_2_SYNTACTIC"
            result["confidence"] = conf
            result["status"] = "MATCH_VERIFIED"
            result["notes"] = f"Identified via phrase permutation matching with confidence {conf}."
            return result

    result["notes"] = "No identifiable fingerprint found across available detection layers."
    return result
