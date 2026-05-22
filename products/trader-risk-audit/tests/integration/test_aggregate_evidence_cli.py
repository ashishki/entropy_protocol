from __future__ import annotations

from pathlib import Path

from trader_risk_audit.cli import main
from trader_risk_audit.evidence import AGGREGATE_EVIDENCE_FIELDS


def test_aggregate_evidence_validate_cli_outputs_safe_summary(
    tmp_path: Path,
    capsys,
) -> None:
    log = tmp_path / "aggregate.csv"
    log.write_text(
        ",".join(AGGREGATE_EVIDENCE_FIELDS)
        + "\n"
        + (
            "2026-05-19,batch_001,market,prop_funded,problem_interview,3,"
            "max_daily_loss,spreadsheet,missing_fees,not_asked,not_asked,"
            "ask_report_review\n"
        ),
        encoding="utf-8",
    )

    result = main(["evidence", "aggregate-validate", "--log-file", str(log)])
    stdout = capsys.readouterr().out

    assert result == 0
    assert "Aggregate Evidence Validation" in stdout
    assert "Rows: 1" in stdout
    assert "Market count: 3" in stdout
    assert str(tmp_path) not in stdout
    assert "trader@example.com" not in stdout
    assert "timestamp,symbol" not in stdout


def test_aggregate_evidence_validate_cli_rejects_raw_rows(
    tmp_path: Path,
    capsys,
) -> None:
    log = tmp_path / "aggregate.csv"
    log.write_text(
        ",".join(AGGREGATE_EVIDENCE_FIELDS)
        + "\n"
        + (
            "2026-05-19,batch_001,market,prop_funded,problem_interview,1,"
            "max_daily_loss,spreadsheet,missing_fees,not_asked,not_asked,"
            "timestamp,symbol\n"
        ),
        encoding="utf-8",
    )

    result = main(["evidence", "aggregate-validate", "--log-file", str(log)])
    stdout = capsys.readouterr().out

    assert result == 2
    assert "must be non-sensitive" in stdout or "must be one of" in stdout
    assert str(tmp_path) not in stdout
