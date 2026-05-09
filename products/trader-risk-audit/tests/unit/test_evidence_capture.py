from __future__ import annotations

from pathlib import Path

import pytest

from trader_risk_audit.cli import main
from trader_risk_audit.evidence import (
    EvidenceRow,
    EvidenceValidationError,
    append_customer_log_row,
    is_demo_evidence,
    load_customer_log,
    summarize_validation_gate,
)


def test_evidence_capture_appends_customer_log_row(tmp_path: Path) -> None:
    log = tmp_path / "pilot_customer_log.csv"
    row = _market_row()

    append_customer_log_row(log, row)
    text = log.read_text(encoding="utf-8")
    loaded = load_customer_log(log)

    assert text.startswith(
        "prospect_source,icp,call_date,export_provided,rules_provided,"
        "paid_amount,objections,report_delivered,repeat_requested,referral"
    )
    assert loaded == (row,)
    assert "trader@example.com" not in text
    assert "@trader" not in text
    with pytest.raises(EvidenceValidationError, match="identifiers"):
        append_customer_log_row(log, _market_row(objections="email trader@example.com"))


def test_evidence_capture_separates_demo_from_market_validation() -> None:
    demo = _market_row(prospect_source="public_sample_demo", paid_amount="999")
    market = _market_row()
    summary = summarize_validation_gate((demo, market))

    assert is_demo_evidence(demo)
    assert not is_demo_evidence(market)
    assert summary.qualified_prospects == 1
    assert summary.paid_audits == 1
    assert summary.repeat_commitments == 1
    assert summary.referrals == 0


def test_evidence_capture_summarizes_validation_gate(
    tmp_path: Path,
    capsys,
) -> None:
    log = tmp_path / "pilot_customer_log.csv"
    rows = (
        _market_row(),
        _market_row(paid_amount="0", repeat_requested=False),
        _market_row(
            export_provided=False,
            rules_provided=False,
            paid_amount="0",
            repeat_requested=False,
        ),
        _market_row(prospect_source="public_sample_demo", paid_amount="99"),
    )
    for row in rows:
        append_customer_log_row(log, row)

    result = main(["evidence", "summary", "--log-file", str(log)])
    output = capsys.readouterr().out

    assert result == 0
    assert "Qualified prospects: 3/10" in output
    assert "Exports and rules: 2/5" in output
    assert "Paid audits: 1/3" in output
    assert "Repeat commitments: 1/2" in output


def _market_row(
    *,
    prospect_source: str = "warm_network",
    paid_amount: str = "99",
    export_provided: bool = True,
    rules_provided: bool = True,
    repeat_requested: bool = True,
    objections: str = "privacy",
) -> EvidenceRow:
    return EvidenceRow(
        prospect_source=prospect_source,
        icp="prop/funded trader",
        call_date="2026-05-09",
        export_provided=export_provided,
        rules_provided=rules_provided,
        paid_amount=paid_amount,
        objections=objections,
        report_delivered=True,
        repeat_requested=repeat_requested,
        referral=False,
    )
