from __future__ import annotations

from pathlib import Path

import pytest

from trader_risk_audit.evidence import (
    AGGREGATE_EVIDENCE_FIELDS,
    EvidenceValidationError,
    load_aggregate_evidence_log,
    summarize_aggregate_evidence,
)


def test_aggregate_evidence_log_validates_and_summarizes(tmp_path: Path) -> None:
    log = tmp_path / "aggregate.csv"
    log.write_text(
        ",".join(AGGREGATE_EVIDENCE_FIELDS)
        + "\n"
        + (
            "2026-05-19,batch_001,market,prop_funded,problem_interview,3,"
            "max_daily_loss,spreadsheet,missing_fees,not_asked,not_asked,"
            "ask_report_review\n"
        )
        + (
            "2026-05-20,batch_001,internal_demo,prop_funded,report_review,2,"
            "not_applicable,coach_review,none,export_willing_yes,"
            "pilot_yes_free_first,return_to_t116\n"
        ),
        encoding="utf-8",
    )

    rows = load_aggregate_evidence_log(log)
    summary = summarize_aggregate_evidence(rows)

    assert summary.rows == 2
    assert summary.total_count == 5
    assert summary.market_count == 3
    assert summary.demo_count == 2
    assert summary.export_willing_yes == 2
    assert summary.pilot_yes == 2
    assert summary.return_to_t116 == 2


def test_aggregate_evidence_log_rejects_identifiers(tmp_path: Path) -> None:
    log = tmp_path / "aggregate.csv"
    log.write_text(
        ",".join(AGGREGATE_EVIDENCE_FIELDS)
        + "\n"
        + (
            "2026-05-19,batch_001,market,prop_funded,problem_interview,1,"
            "max_daily_loss,spreadsheet,missing_fees,not_asked,not_asked,"
            "contact_trader@example.com\n"
        ),
        encoding="utf-8",
    )

    with pytest.raises(EvidenceValidationError):
        load_aggregate_evidence_log(log)


def test_aggregate_evidence_log_rejects_unknown_tags(tmp_path: Path) -> None:
    log = tmp_path / "aggregate.csv"
    log.write_text(
        ",".join(AGGREGATE_EVIDENCE_FIELDS)
        + "\n"
        + (
            "2026-05-19,batch_001,market,prop_funded,problem_interview,1,"
            "max_daily_loss,spreadsheet,missing_fees,not_asked,not_asked,"
            "send_live_signal_offer\n"
        ),
        encoding="utf-8",
    )

    with pytest.raises(EvidenceValidationError, match="next_action_tag"):
        load_aggregate_evidence_log(log)
