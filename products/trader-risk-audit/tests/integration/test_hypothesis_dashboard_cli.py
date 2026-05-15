from __future__ import annotations

from pathlib import Path

from trader_risk_audit.cli import main
from trader_risk_audit.evidence import (
    EvidenceRow,
    HypothesisFunnelEvent,
    append_customer_log_row,
    append_hypothesis_funnel_event,
)


def test_dashboard_cli_counts_funnel(tmp_path: Path, capsys) -> None:
    customer_log = tmp_path / "pilot_customer_log.csv"
    funnel_log = tmp_path / "hypothesis_funnel_events.csv"
    append_customer_log_row(customer_log, _legacy_row())
    for event_type in (
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
    ):
        tags = ("privacy",) if event_type == "cta_accepted" else ()
        append_hypothesis_funnel_event(
            funnel_log,
            _event(event_type, tags=tags),
        )

    result = main(
        [
            "evidence",
            "hypothesis-dashboard",
            "--customer-log",
            str(customer_log),
            "--funnel-log",
            str(funnel_log),
        ]
    )
    output = capsys.readouterr().out

    assert result == 0
    assert "Qualified prospects: 2" in output
    assert "Intake started: 1" in output
    assert "Valid exports/rules: 2" in output
    assert "Policy built: 1" in output
    assert "Audit run: 1" in output
    assert "Preview generated: 1" in output
    assert "CTA accepted: 1" in output
    assert "Paid reports: 2" in output
    assert "Repeat commitments: 2" in output
    assert "Referrals: 1" in output
    assert "CTA accept ratio: 1/1 (100%)" in output
    assert "Next action:" in output


def test_dashboard_excludes_demo_from_paid_gate(tmp_path: Path, capsys) -> None:
    funnel_log = tmp_path / "hypothesis_funnel_events.csv"
    append_hypothesis_funnel_event(funnel_log, _event("paid_report"))
    append_hypothesis_funnel_event(
        funnel_log,
        _event(
            "paid_report",
            intake_id="demo_intake",
            source_type="public_sample_demo",
            evidence_source="demo_artifact",
        ),
    )

    result = main(["evidence", "hypothesis-dashboard", "--funnel-log", str(funnel_log)])
    output = capsys.readouterr().out

    assert result == 0
    assert "Paid reports: 1" in output
    assert "Demo/artifact events: 1" in output
    assert "Gate status: needs_more_evidence" in output


def test_dashboard_output_is_privacy_safe(tmp_path: Path, capsys) -> None:
    funnel_log = tmp_path / "hypothesis_funnel_events.csv"
    append_hypothesis_funnel_event(
        funnel_log,
        _event("valid_export", tags=("unsupported_pnl", "export_missing_fees")),
    )

    result = main(["evidence", "hypothesis-dashboard", "--funnel-log", str(funnel_log)])
    output = capsys.readouterr().out

    assert result == 0
    assert "unsupported_pnl=1" in output
    assert "export_missing_fees=1" in output
    for private_text in (
        "timestamp,symbol",
        "trader@example.com",
        "@trader",
        "payment_id",
        "transaction_id",
        "api_key",
    ):
        assert private_text not in output


def _legacy_row() -> EvidenceRow:
    return EvidenceRow(
        prospect_source="warm_network",
        icp="prop/funded trader",
        call_date="2026-05-15",
        export_provided=True,
        rules_provided=True,
        paid_amount="99",
        objections="privacy",
        report_delivered=True,
        repeat_requested=True,
        referral=False,
    )


def _event(
    event_type: str,
    *,
    intake_id: str = "intake_market_001",
    source_type: str = "csv_export",
    evidence_source: str = "market",
    tags: tuple[str, ...] = (),
) -> HypothesisFunnelEvent:
    return HypothesisFunnelEvent(
        event_type=event_type,
        timestamp="2026-05-15T10:00:00Z",
        intake_id=intake_id,
        source_type=source_type,
        evidence_source=evidence_source,
        tags=tags,
    )
