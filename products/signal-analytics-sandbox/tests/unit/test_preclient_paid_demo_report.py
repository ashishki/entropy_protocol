from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT = PROJECT_ROOT / "docs/pilot/reports/preclient/PAID_STYLE_DEMO_REPORT.md"


def test_preclient_paid_demo_report_selects_channel_from_evidence() -> None:
    report = REPORT.read_text(encoding="utf-8")

    assert "Status: `internal_demo_only`" in report
    assert "Selected channel: `pifagortrade`" in report
    assert "## Selection Basis" in report
    assert "evidence-based" in report
    assert "V1 evaluable text claims | 14 | 49 | 107" in report
    assert "model-reviewed packet candidates | 1 | 1 | 7" in report
    assert "docs/pilot/preclient_FREE_DASHBOARD_CARDS.json" in report
    assert "docs/pilot/preclient_MODEL_REVIEW_PACKET.md" in report


def test_preclient_paid_demo_report_contains_locked_paid_sections() -> None:
    report = REPORT.read_text(encoding="utf-8")

    for section in (
        "## Locked Section: Evidence Appendix Preview",
        "## Locked Section: Post-Factum Vs Real-Time Distinction",
        "## Locked Section: Setup And RR Review",
        "## Locked Section: Counterexamples",
        "## Locked Section: Limitations",
    ):
        assert section in report

    assert "docs/pilot/preclient_EVIDENCE_APPENDIX.md" in report
    assert "post-factum candidates" in report
    assert "dashboard-safe RR rows: `0`" in report
    assert "long ETH](https://t.me/pifagortrade/2647)" in report


def test_preclient_paid_demo_report_remains_internal_and_avoids_promises() -> None:
    report = REPORT.read_text(encoding="utf-8")
    lower = report.lower()

    assert "Decision: `internal_demo_only`" in report
    assert "external gate remains `approve_internal_only`" in report
    assert "no public display or external delivery is approved" in lower
    for forbidden in (
        "future profit",
        "guaranteed",
        "pricing promise",
        "private-source promise",
        "private group",
        "follow this author",
        "investment advice",
    ):
        assert forbidden not in lower
