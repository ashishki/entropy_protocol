from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from trader_risk_audit.cli import main
from trader_risk_audit.pilot_queue import PilotQueue
from trader_risk_audit.reporting.claim_guard import REQUIRED_DISCLAIMER
from trader_risk_audit.telegram_bot.delivery import deliver_approved_report
from trader_risk_audit.telegram_bot.handlers import TelegramPilotHandlers
from trader_risk_audit.telegram_bot.storage import (
    TelegramAuditStorage,
    TelegramDocumentUpload,
)


@dataclass
class MockTelegramClient:
    texts: list[str] = field(default_factory=list)
    documents: list[Path] = field(default_factory=list)
    network_used: bool = False

    def send_text(self, text: str) -> None:
        self.texts.append(text)

    def send_document(self, path: Path) -> None:
        self.documents.append(path)


def test_full_mocked_telegram_pilot_flow(tmp_path: Path) -> None:
    client = MockTelegramClient()
    handlers = TelegramPilotHandlers(
        TelegramAuditStorage(tmp_path / "telegram_workspaces")
    )

    new_audit = handlers.handle_command("/new_audit")
    upload = handlers.handle_document_upload(
        TelegramDocumentUpload(
            file_name="trades.csv",
            content=Path("tests/fixtures/pilot/trades.csv").read_bytes(),
        )
    )

    assert new_audit.status == "awaiting_files"
    assert upload.audit_id is not None
    workspace_root = tmp_path / "telegram_workspaces" / upload.audit_id
    assert (workspace_root / "input" / "trades.csv").exists()

    queue = PilotQueue(tmp_path / "pilot_queue.json")
    queue.upsert_request(
        upload.audit_id,
        status="received",
        file_references={"telegram_upload": "input/trades.csv"},
    )
    queue.set_status(upload.audit_id, "needs_policy_mapping")
    queue.set_status(upload.audit_id, "ready_to_run")
    queue.set_status(upload.audit_id, "processing")

    output_dir = tmp_path / "audit_output"
    assert (
        main(
            [
                "audit",
                "--trades",
                "tests/fixtures/pilot/trades.csv",
                "--policy",
                "tests/fixtures/pilot/policy.yaml",
                "--output-dir",
                str(output_dir),
            ]
        )
        == 0
    )

    packet = output_dir / "telegram_packet.txt"
    packet.write_text(
        f"Trader Risk Audit Summary\nReport approved.\n{REQUIRED_DISCLAIMER}\n",
        encoding="utf-8",
    )
    queue.upsert_request(
        upload.audit_id,
        status="ready_for_review",
        file_references={
            "report_markdown": str(output_dir / "report.md"),
            "delivery_packet": str(packet),
        },
    )

    result = deliver_approved_report(
        queue=queue,
        audit_id=upload.audit_id,
        report_path=output_dir / "report.md",
        delivery_packet_path=packet,
        sender=client,
    )

    assert result.status == "delivered"
    assert queue.get_request(upload.audit_id).status == "delivered"
    assert client.texts == [packet.read_text(encoding="utf-8")]
    assert client.documents == [output_dir / "report.md"]


def test_telegram_pilot_flow_uses_mocked_client_only(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.delenv("TRA_TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TRA_TELEGRAM_BOT_ENABLED", raising=False)
    client = MockTelegramClient()
    queue = PilotQueue(tmp_path / "queue.json")
    queue.upsert_request("audit_mocked", status="ready_for_review")
    report = tmp_path / "report.md"
    packet = tmp_path / "packet.txt"
    report.write_text(f"# Report\n\n{REQUIRED_DISCLAIMER}\n", encoding="utf-8")
    packet.write_text(f"Summary\n{REQUIRED_DISCLAIMER}\n", encoding="utf-8")

    deliver_approved_report(
        queue=queue,
        audit_id="audit_mocked",
        report_path=report,
        delivery_packet_path=packet,
        sender=client,
    )

    assert client.network_used is False
    assert client.texts
    assert client.documents == [report]


def test_telegram_pilot_flow_redacts_confidential_data(tmp_path: Path) -> None:
    client = MockTelegramClient()
    handlers = TelegramPilotHandlers(TelegramAuditStorage(tmp_path / "workspaces"))
    upload = handlers.handle_document_upload(
        TelegramDocumentUpload(
            file_name="trades.csv",
            content=Path("tests/fixtures/pilot/trades.csv").read_bytes(),
        )
    )
    queue = PilotQueue(tmp_path / "queue.json")
    queue.upsert_request(upload.audit_id or "audit_redacted", status="ready_for_review")
    report = tmp_path / "report.md"
    packet = tmp_path / "packet.txt"
    report.write_text(f"# Report\n\n{REQUIRED_DISCLAIMER}\n", encoding="utf-8")
    packet.write_text(f"Summary\n{REQUIRED_DISCLAIMER}\n", encoding="utf-8")

    deliver_approved_report(
        queue=queue,
        audit_id=upload.audit_id or "audit_redacted",
        report_path=report,
        delivery_packet_path=packet,
        sender=client,
    )

    emitted_text = "\n".join(
        (
            handlers.handle_command("/new_audit").text,
            upload.text,
            *client.texts,
            *(str(path) for path in client.documents),
        )
    )
    forbidden_fragments = (
        "timestamp,symbol,side,quantity,price",
        "2026-03-01,EURUSD,buy,1,100",
        "@trader",
        "trader@example.com",
        "account_123456",
        "customer identifier",
    )
    for fragment in forbidden_fragments:
        assert fragment not in emitted_text
