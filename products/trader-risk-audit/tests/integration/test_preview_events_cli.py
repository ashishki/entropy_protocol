from __future__ import annotations

from pathlib import Path

from trader_risk_audit.cli import main


def test_preview_events_cli_summary(tmp_path: Path, capsys) -> None:
    event_log = tmp_path / "preview_events.csv"

    append_result = main(
        [
            "evidence",
            "preview-event-append",
            "--event-log",
            str(event_log),
            "--event-type",
            "preview_generated",
            "--timestamp",
            "2026-05-15T10:00:00Z",
            "--intake-id",
            "intake_safe_001",
            "--source-type",
            "csv_export",
        ]
    )
    cta_result = main(
        [
            "evidence",
            "preview-event-append",
            "--event-log",
            str(event_log),
            "--event-type",
            "cta_accepted",
            "--timestamp",
            "2026-05-15T10:02:00Z",
            "--intake-id",
            "intake_safe_001",
            "--source-type",
            "csv_export",
            "--objection-tag",
            "price",
        ]
    )
    summary_result = main(
        [
            "evidence",
            "preview-event-summary",
            "--event-log",
            str(event_log),
        ]
    )

    stdout = capsys.readouterr().out
    assert append_result == 0
    assert cta_result == 0
    assert summary_result == 0
    assert "Preview Event Summary" in stdout
    assert "Preview generated: 1" in stdout
    assert "CTA accepted market: 1" in stdout
