from __future__ import annotations

from pathlib import Path

DOC = Path("docs/HYPOTHESIS_EVIDENCE_DASHBOARD_RU.md")

REQUIRED_EVENTS = (
    "prospect_qualified",
    "intake_started",
    "valid_export",
    "policy_built",
    "audit_run",
    "preview_generated",
    "cta_accepted",
    "paid_report",
    "repeat_commitment",
    "referral",
)


def test_hypothesis_docs_define_gate_events() -> None:
    text = " ".join(DOC.read_text(encoding="utf-8").casefold().split())

    for event in REQUIRED_EVENTS:
        assert event in text
    for phrase in (
        "gate evidence",
        "vanity/demo events",
        "public_sample_demo",
        "internal_demo",
        "demo_artifact",
        "paid_report",
        "repeat_commitment",
        "referral",
    ):
        assert phrase in text


def test_hypothesis_docs_reject_vanity_metrics() -> None:
    text = " ".join(DOC.read_text(encoding="utf-8").casefold().split())

    for phrase in (
        "uploads/api connections alone are not pmf",
        "does not prove willingness-to-pay",
        "does not replace paid_report",
        "does not replace repeat_commitment",
        "does not replace referral",
    ):
        assert phrase in text
