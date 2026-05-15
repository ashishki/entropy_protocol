"""Holdout approval absence denial packet tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DENIAL = PROJECT_ROOT / "docs" / "approvals" / "HOLDOUT_APPROVAL_ABSENCE_DENIAL.md"


def test_denial_packet_records_missing_prerequisites() -> None:
    text = DENIAL.read_text(encoding="utf-8")

    assert "Status: HOLDOUT_APPROVAL_DENIED_NO_APPROVAL" in text
    for prerequisite in (
        "explicit human holdout approval: missing",
        "explicit human phase-gate approval: missing",
        "approval intake accepted event: missing",
        "leakage guard status: incomplete",
    ):
        assert prerequisite in text
    assert "decision: DENIED" in text
    assert "MISSING_EXPLICIT_HUMAN_HOLDOUT_APPROVAL" in text
    assert "HOLDOUT_LEAKAGE_GUARD_INCOMPLETE" in text


def test_denial_packet_preserves_no_read_boundary() -> None:
    text = DENIAL.read_text(encoding="utf-8").lower()

    assert "does not open,\nread, unlock, or inspect holdout data" in text
    assert "holdout path opened: false" in text
    assert "holdout read executed: false" in text
    assert "holdout unlock requested: false" in text
    assert "holdout read: blocked" in text
    assert "holdout unlock: blocked" in text


def test_denial_packet_rejects_claim_surfaces() -> None:
    text = DENIAL.read_text(encoding="utf-8")

    for rejected in (
        "OOS/performance conclusion: rejected",
        "production readiness: rejected",
        "capital-ready conclusion: rejected",
        "live feed activation: rejected",
        "broker/exchange activation: rejected",
    ):
        assert rejected in text
    for evidence in (
        "docs/approvals/HOLDOUT_APPROVAL_INTAKE_CONTRACT.md",
        "docs/protocols/HOLDOUT_LEAKAGE_GUARD_PROTOCOL.md",
        "docs/approvals/HOLDOUT_APPROVAL_REQUEST_PACKET.md",
    ):
        assert f"`{evidence}`" in text
        assert (PROJECT_ROOT / evidence).is_file()
