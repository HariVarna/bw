"""Flask Application Factory and Route Definitions for Examination Leak Tracing Dashboard."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from webapp.database import get_dashboard_counts, get_recent_activities, init_db
from webapp.services.access_ledger_service import AccessLedgerService
from webapp.services.custodian_service import CustodianService
from webapp.services.demo_service import DemoService
from webapp.services.examination_service import ExaminationService
from webapp.services.fingerprint_service import COPIES_DIR, FingerprintService
from webapp.services.report_service import ReportService
from webapp.services.tracing_service import TracingService

# Create and configure Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-bw-soi-2026")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max upload

# Initialize database tables on app startup
with app.app_context():
    init_db()
    # Check if empty, auto-seed demo data if empty to guarantee instant reviewability
    if not DemoService.is_demo_seeded():
        try:
            DemoService.seed_demo_data()
        except Exception as e:
            print(f"Auto-seeding demo data failed: {e}")


# =============================================================================
# DASHBOARD
# =============================================================================

@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    counts = get_dashboard_counts()
    ledger_stats = AccessLedgerService.get_ledger_stats()
    recent_activities = get_recent_activities(limit=6)
    examinations = ExaminationService.list_examinations()[:3]
    is_demo = DemoService.is_demo_seeded()

    # Merge ledger counts into metrics
    counts["recorded_events"] = ledger_stats["total_events"]
    counts["blocks"] = ledger_stats["total_blocks"]

    return render_template(
        "dashboard.html",
        counts=counts,
        ledger_stats=ledger_stats,
        recent_activities=recent_activities,
        examinations=examinations,
        is_demo=is_demo,
        active_page="dashboard",
    )


# =============================================================================
# EXAMINATIONS
# =============================================================================

@app.route("/examinations")
def examinations():
    all_exams = ExaminationService.list_examinations()
    return render_template(
        "examinations.html",
        examinations=all_exams,
        active_page="examinations",
    )


@app.route("/examinations/new", methods=["POST"])
def create_examination():
    paper_id = request.form.get("paper_id", "").strip() or "QP-2026-CS801-AUTUMN"
    try:
        ExaminationService.create_synthetic_examination(paper_id=paper_id, is_demo=False)
        flash(f"Examination question paper '{paper_id}' generated successfully.", "success")
    except Exception as e:
        flash(f"Failed to generate examination: {e}", "danger")
    return redirect(url_for("examinations"))


# =============================================================================
# CUSTODIANS
# =============================================================================

@app.route("/custodians")
def custodians():
    all_custodians = CustodianService.list_custodians()
    return render_template(
        "custodians.html",
        custodians=all_custodians,
        active_page="custodians",
    )


@app.route("/custodians/register", methods=["POST"])
def register_custodian():
    cid = request.form.get("custodian_id", "").strip()
    name = request.form.get("name", "").strip()
    role = request.form.get("role", "").strip()
    center = request.form.get("center_code", "").strip()

    if not all([cid, name, role, center]):
        flash("All custodian fields are required.", "warning")
        return redirect(url_for("custodians"))

    try:
        CustodianService.register_custodian(
            custodian_id=cid,
            name=name,
            role=role,
            center_code=center,
            is_demo=False,
        )
        flash(f"Custodian '{cid}' registered with Ed25519 keypair.", "success")
    except Exception as e:
        flash(f"Failed to register custodian: {e}", "danger")

    return redirect(url_for("custodians"))


# =============================================================================
# FINGERPRINTED COPIES
# =============================================================================

@app.route("/copies")
def copies():
    all_copies = FingerprintService.list_copies()
    all_exams = ExaminationService.list_examinations()
    return render_template(
        "copies.html",
        copies=all_copies,
        examinations=all_exams,
        active_page="copies",
    )


@app.route("/copies/generate", methods=["POST"])
def generate_copies():
    paper_id = request.form.get("paper_id")
    count_str = request.form.get("count", "4")
    try:
        count = int(count_str)
    except ValueError:
        count = 4

    exam = ExaminationService.get_examination(paper_id)
    if not exam:
        flash("Selected examination does not exist.", "danger")
        return redirect(url_for("copies"))

    custodians_list = CustodianService.list_custodians()
    if not custodians_list:
        flash("No registered custodians available to assign copies to.", "warning")
        return redirect(url_for("copies"))

    existing_copies = FingerprintService.list_copies()
    start_idx = len(existing_copies) + 1

    for i in range(start_idx, start_idx + count):
        assigned_c = custodians_list[(i - 1) % len(custodians_list)]
        FingerprintService.generate_copy_record(
            paper_id=paper_id,
            base_text=exam["raw_text"],
            copy_idx=i,
            custodian_id=assigned_c["custodian_id"],
            is_demo=False,
        )

    flash(f"Generated {count} fingerprinted copies for paper '{paper_id}'.", "success")
    return redirect(url_for("copies"))


# =============================================================================
# ACCESS LEDGER (BLOCKCHAIN EXPLORER)
# =============================================================================

@app.route("/ledger")
def ledger():
    blocks = AccessLedgerService.get_blocks()
    events = AccessLedgerService.get_all_events()
    stats = AccessLedgerService.get_ledger_stats()
    return render_template(
        "ledger.html",
        blocks=blocks,
        events=events,
        stats=stats,
        active_page="ledger",
    )


@app.route("/api/ledger/verify", methods=["POST"])
def api_verify_ledger():
    audit_result = AccessLedgerService.verify_ledger()
    return jsonify(audit_result)


# =============================================================================
# LEAK INVESTIGATION
# =============================================================================

@app.route("/investigation")
def investigation():
    investigations = TracingService.list_investigations()
    sample_files = []
    samples_dir = ROOT_DIR / "webapp" / "static" / "samples"
    if samples_dir.exists():
        for p in samples_dir.glob("*.*"):
            sample_files.append(p.name)

    return render_template(
        "investigation.html",
        investigations=investigations,
        sample_files=sample_files,
        active_page="investigation",
    )


@app.route("/investigation/trace", methods=["POST"])
def trace_leak():
    sample_text = request.form.get("sample_text", "").strip()
    uploaded_file = request.files.get("sample_file")
    preloaded_sample = request.form.get("preloaded_sample", "").strip()

    filename = "submitted_sample.txt"
    file_bytes = None

    if preloaded_sample:
        sample_path = ROOT_DIR / "webapp" / "static" / "samples" / preloaded_sample
        if sample_path.exists():
            filename = preloaded_sample
            if preloaded_sample.lower().endswith((".png", ".jpg", ".jpeg")):
                file_bytes = sample_path.read_bytes()
                sample_text = None
            else:
                sample_text = sample_path.read_text(encoding="utf-8", errors="ignore")
    elif uploaded_file and uploaded_file.filename:
        filename = uploaded_file.filename
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            file_bytes = uploaded_file.read()
            sample_text = None
        else:
            sample_text = uploaded_file.read().decode("utf-8", errors="ignore")

    if not sample_text and not file_bytes:
        flash("Please provide a text snippet, upload an excerpt file, or select a preloaded sample.", "warning")
        return redirect(url_for("investigation"))

    inv_result = TracingService.investigate(
        sample_text=sample_text,
        sample_image_bytes=file_bytes,
        filename=filename,
        is_demo=False,
    )

    if inv_result.get("detected_copy_id"):
        flash(
            f"Forensic attribution successful: Leaked excerpt matched to copy {inv_result['detected_copy_id']} "
            f"via {inv_result['detection_layer']} (Confidence: {inv_result['confidence_score']*100:.1f}%).",
            "success",
        )
    else:
        flash("No attributable steganographic or cryptographic fingerprint found in the sample.", "danger")

    return redirect(url_for("view_investigation", case_number=inv_result["case_number"]))


@app.route("/investigation/<case_number>")
def view_investigation(case_number: str):
    case = TracingService.get_investigation(case_number)
    if not case:
        flash(f"Investigation case '{case_number}' not found.", "warning")
        return redirect(url_for("investigation"))

    return render_template(
        "investigation_detail.html",
        case=case,
        active_page="investigation",
    )


# =============================================================================
# REPORTS & EVIDENCE
# =============================================================================

@app.route("/reports")
def reports():
    metadata = ReportService.get_run_metadata()
    fp_tests = ReportService.get_fingerprint_tests()
    ledger_tests = ReportService.get_ledger_tests()
    timing_tests = ReportService.get_timing_tests()

    return render_template(
        "reports.html",
        metadata=metadata,
        fp_tests=fp_tests,
        ledger_tests=ledger_tests,
        timing_tests=timing_tests,
        active_page="reports",
    )


# =============================================================================
# SYSTEM INFORMATION
# =============================================================================

@app.route("/system-info")
def system_info():
    import platform
    import cryptography
    import PIL
    import importlib.metadata

    env_info = {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "cryptography_version": cryptography.__version__,
        "pillow_version": PIL.__version__,
        "flask_version": importlib.metadata.version("flask"),
        "root_directory": str(ROOT_DIR),
        "asymmetric_algorithm": "Ed25519 (Edwards-curve Digital Signature Algorithm, RFC 8032)",
        "hash_algorithm": "SHA-256 (FIPS PUB 180-4)",
        "merkle_tree": "Binary Merkle Tree with canonical pair concatenation",
        "steganography_l1": "Zero-Width Unicode (ZWSP \\u200b, ZWNJ \\u200c, ZWJ \\u200d)",
        "steganography_l2": "Base-4 Syntactic Permutations (Instruction prefix, calc phrase, mobile phrase, part A format)",
        "steganography_l3": "Visual Corner Micro-Pattern (16-bit binary cell matrix) + faint diagonal watermark",
        "ledger_model": "Permissioned append-only cryptographic block chain (local PoC single-node)",
    }

    return render_template(
        "system_info.html",
        env_info=env_info,
        active_page="system-info",
    )


# =============================================================================
# DEMO CONTROLS API
# =============================================================================

@app.route("/api/demo/seed", methods=["POST"])
def api_seed_demo():
    res = DemoService.seed_demo_data()
    return jsonify(res)


@app.route("/api/demo/reset", methods=["POST"])
def api_reset_demo():
    res = DemoService.reset_demo_data()
    return jsonify(res)


# =============================================================================
# FILE SERVING
# =============================================================================

@app.route("/static/generated_copies/<path:filename>")
def serve_generated_copy(filename):
    return send_from_directory(str(COPIES_DIR), filename)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
