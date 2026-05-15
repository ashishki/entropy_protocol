from __future__ import annotations

from pathlib import Path

from trader_risk_audit.cli import main
from trader_risk_audit.evidence import (
    HypothesisFunnelEvent,
    append_hypothesis_funnel_event,
)


def test_evidence_export_writes_safe_reports(tmp_path: Path, capsys) -> None:
    funnel_log = tmp_path / "hypothesis_funnel_events.csv"
    append_hypothesis_funnel_event(
        funnel_log,
        HypothesisFunnelEvent(
            event_type="paid_report",
            timestamp="2026-05-15T10:00:00Z",
            intake_id="intake_market_001",
            source_type="csv_export",
            tags=("privacy",),
        ),
    )
    output_dir = tmp_path / "export"

    result = main(
        [
            "evidence",
            "export",
            "--output-dir",
            str(output_dir),
            "--funnel-log",
            str(funnel_log),
        ]
    )
    stdout = capsys.readouterr().out
    csv_path = output_dir / "hypothesis_evidence_summary.csv"
    markdown_path = output_dir / "hypothesis_evidence_summary.md"
    csv_text = csv_path.read_text(encoding="utf-8")
    markdown = markdown_path.read_text(encoding="utf-8")

    assert result == 0
    assert "hypothesis_evidence_summary.csv" in stdout
    assert "hypothesis_evidence_summary.md" in stdout
    assert "paid_reports,1" in csv_text
    assert "gate_verdict,needs_more_evidence" in csv_text
    assert "objection_tags,privacy=1" in csv_text
    assert "Hypothesis Gate Decision" in markdown
    assert "funnel_event_log_sha256" in markdown
    for private_text in (
        str(tmp_path),
        "timestamp,symbol",
        "trader@example.com",
        "@trader",
        "payment_id",
        "api_key",
    ):
        assert private_text not in stdout
        assert private_text not in csv_text
        assert private_text not in markdown
