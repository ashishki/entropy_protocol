from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from trader_risk_audit.cli import main
from trader_risk_audit.pilot_queue import QUEUE_STATUSES, PilotQueue, PilotQueueError


def test_queue_persists_allowed_statuses(tmp_path: Path) -> None:
    queue_file = tmp_path / "queue.json"
    queue = PilotQueue(queue_file)

    for index, status in enumerate(QUEUE_STATUSES):
        queue.upsert_request(
            f"audit_{index}",
            status=status,
            created_at=datetime(2026, 5, 7, 12, index, tzinfo=UTC),
        )

    payload = json.loads(queue_file.read_text(encoding="utf-8"))
    persisted_statuses = {item["status"] for item in payload["requests"].values()}
    reloaded_statuses = {item.status for item in PilotQueue(queue_file).list_requests()}

    assert persisted_statuses == set(QUEUE_STATUSES)
    assert reloaded_statuses == set(QUEUE_STATUSES)

    with pytest.raises(PilotQueueError, match="unsupported"):
        queue.upsert_request("audit_bad", status="auto_deliver_report")


def test_queue_cli_omits_confidential_data(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    queue_file = tmp_path / "queue.json"
    PilotQueue(queue_file).upsert_request(
        "audit_safe",
        file_references={
            "trades": "input/trades.csv",
            "operator_notes": "operator_notes/review.md",
            "absolute_report": tmp_path / "customer" / "report.md",
        },
        created_at=datetime(2026, 5, 7, 12, 0, tzinfo=UTC),
    )

    assert main(["queue", "list", "--queue-file", str(queue_file)]) == 0
    list_output = capsys.readouterr().out
    assert (
        main(
            [
                "queue",
                "show",
                "--queue-file",
                str(queue_file),
                "--audit-id",
                "audit_safe",
            ]
        )
        == 0
    )
    show_output = capsys.readouterr().out
    combined = f"{list_output}\n{show_output}"

    assert "audit_safe" in combined
    assert "input/trades.csv" in combined
    assert "report.md" in combined
    assert "timestamp,symbol,side,quantity,price" not in combined
    assert "2026-03-01,EURUSD,buy,1,100" not in combined
    assert "private coaching note" not in combined


def test_queue_cli_status_and_reject_transitions(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    queue_file = tmp_path / "queue.json"
    queue = PilotQueue(queue_file)
    queue.upsert_request("audit_transition")

    assert (
        main(
            [
                "queue",
                "status",
                "--queue-file",
                str(queue_file),
                "--audit-id",
                "audit_transition",
                "--status",
                "ready_to_run",
            ]
        )
        == 0
    )
    assert "ready_to_run" in capsys.readouterr().out
    assert (
        PilotQueue(queue_file).get_request("audit_transition").status == "ready_to_run"
    )

    assert (
        main(
            [
                "queue",
                "reject",
                "--queue-file",
                str(queue_file),
                "--audit-id",
                "audit_transition",
                "--reason",
                "unsupported export format",
            ]
        )
        == 0
    )
    reject_output = capsys.readouterr().out
    rejected = PilotQueue(queue_file).get_request("audit_transition")

    assert rejected.status == "rejected"
    assert rejected.rejection_reason == "unsupported export format"
    assert "unsupported export format" in reject_output

    with pytest.raises(PilotQueueError, match="non-sensitive"):
        queue.reject("audit_transition", "timestamp,symbol,side,quantity,price")
