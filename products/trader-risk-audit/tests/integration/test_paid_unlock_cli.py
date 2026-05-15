from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.cli import main


def test_paid_unlock_cli_status_flow(tmp_path: Path, capsys) -> None:
    state_file = tmp_path / "paid_unlock.json"

    requested = main(
        [
            "preview",
            "unlock",
            "--state-file",
            str(state_file),
            "--audit-id",
            "audit_demo",
            "--status",
            "paid_requested",
            "--manual-payment-evidence",
            "manual_paid_intent",
        ]
    )
    reviewed = main(
        [
            "preview",
            "unlock",
            "--state-file",
            str(state_file),
            "--status",
            "operator_reviewed",
            "--claim-safe",
        ]
    )
    delivered = main(
        [
            "preview",
            "unlock",
            "--state-file",
            str(state_file),
            "--status",
            "delivered",
            "--delivered-ref",
            "telegram_packet_reviewed.txt",
        ]
    )

    stdout = capsys.readouterr().out
    payload = json.loads(state_file.read_text(encoding="utf-8"))
    assert requested == 0
    assert reviewed == 0
    assert delivered == 0
    assert payload["status"] == "delivered"
    assert payload["manual_payment_evidence"] == "manual_paid_intent"
    assert payload["delivered_ref"] == "telegram_packet_reviewed.txt"
    assert "preview unlock status: delivered" in stdout
