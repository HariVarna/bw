"""Automated Test Suite for Flask Web Application Endpoints and Services."""

import json
import pytest
from webapp.app import app
from webapp.services.demo_service import DemoService
from webapp.services.access_ledger_service import AccessLedgerService


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        # Seed clean demo dataset for tests
        DemoService.seed_demo_data()
        yield client


def test_index_redirect(client):
    res = client.get("/")
    assert res.status_code == 302
    assert "/dashboard" in res.location


def test_dashboard_view(client):
    res = client.get("/dashboard")
    assert res.status_code == 200
    html = res.data.decode("utf-8")
    assert "Examination Security Dashboard" in html
    assert "Registered Exams" in html
    assert "Append-Only Blockchain Integrity Engine" not in html # that's on ledger page
    assert "7-STAGE PROTOCOL" in html
    assert "Ledger Health & Integrity" in html


def test_examinations_view(client):
    res = client.get("/examinations")
    assert res.status_code == 200
    html = res.data.decode("utf-8")
    assert "QP-2026-CS801-AUTUMN" in html


def test_create_examination(client):
    res = client.post("/examinations/new", data={"paper_id": "QP-2026-TEST-99"}, follow_redirects=True)
    assert res.status_code == 200
    html = res.data.decode("utf-8")
    assert "QP-2026-TEST-99" in html


def test_custodians_view(client):
    res = client.get("/custodians")
    assert res.status_code == 200
    html = res.data.decode("utf-8")
    assert "CUST-01-COE" in html
    assert "Controller of Examinations" in html


def test_register_custodian(client):
    res = client.post(
        "/custodians/register",
        data={
            "custodian_id": "CUST-99-TEST",
            "name": "Test Officer",
            "role": "SUPERINTENDENT",
            "center_code": "CENTER-999",
        },
        follow_redirects=True,
    )
    assert res.status_code == 200
    html = res.data.decode("utf-8")
    assert "CUST-99-TEST" in html


def test_copies_view(client):
    res = client.get("/copies")
    assert res.status_code == 200
    html = res.data.decode("utf-8")
    assert "CPY-01" in html
    assert "L1/L2/L3 ARMORED" in html


def test_ledger_view(client):
    res = client.get("/ledger")
    assert res.status_code == 200
    html = res.data.decode("utf-8")
    assert "Append-Only Blockchain Integrity Engine" in html
    assert "Blockchain Blocks" in html
    assert "Recorded Custody Access Events" in html


def test_api_verify_ledger(client):
    res = client.post("/api/ledger/verify")
    assert res.status_code == 200
    data = res.get_json()
    assert data["is_valid"] is True
    assert data["total_blocks"] >= 2
    assert len(data["errors"]) == 0


def test_investigation_view(client):
    res = client.get("/investigation")
    assert res.status_code == 200
    html = res.data.decode("utf-8")
    assert "Initiate Forensic Leak Attribution" in html
    assert "leak_sample_digital_copy3.txt" in html


def test_trace_leak_preloaded_sample(client):
    res = client.post(
        "/investigation/trace",
        data={"preloaded_sample": "leak_sample_digital_copy3.txt"},
        follow_redirects=True,
    )
    assert res.status_code == 200
    html = res.data.decode("utf-8")
    assert "Forensic Attribution Verdict" in html
    assert "CPY-03" in html
    assert "MATCH VERIFIED" in html or "POSITIVE ATTRIBUTION" in html


def test_reports_view(client):
    res = client.get("/reports")
    assert res.status_code == 200
    html = res.data.decode("utf-8")
    assert "Official Protocol Evidence & Benchmark Reports" in html
    assert "Test 1: Multi-Layer Fingerprint Tracing" in html


def test_system_info_view(client):
    res = client.get("/system-info")
    assert res.status_code == 200
    html = res.data.decode("utf-8")
    assert "Architecture & Technical Specifications" in html
    assert "Ed25519 (RFC 8032)" in html
