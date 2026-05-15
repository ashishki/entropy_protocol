from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from trader_risk_audit.pilot_queue import PilotQueue
from trader_risk_audit.telegram_bot.delivery import (
    build_approved_delivery_copy,
    deliver_approved_report,
)
from trader_risk_audit.telegram_bot.handlers import (
    TelegramDemoSample,
    TelegramPilotHandlers,
)
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


def test_telegram_demo_happy_path_uses_mocked_client(tmp_path: Path) -> None:
    client = MockTelegramClient()
    handlers = TelegramPilotHandlers(
        TelegramAuditStorage(tmp_path / "telegram_workspaces"),
        demo_sample=_public_sample(),
    )

    start = handlers.handle_command("/start")
    new_audit = handlers.handle_command("/new_audit")
    demo = handlers.handle_command("/demo_sample")
    upload = handlers.handle_document_upload(
        TelegramDocumentUpload(
            file_name="trades.csv",
            content=Path("demo/public_sample_001/trades.csv").read_bytes(),
        )
    )

    assert "/new_audit" in start.text
    assert "/demo_sample" in start.text
    assert new_audit.status == "awaiting_files"
    assert "operator review" in new_audit.text.casefold()
    assert demo.audit_id == "demo_public_sample_001"
    assert demo.status == "ready_for_review"
    assert upload.audit_id is not None
    assert upload.status == "received"

    queue = PilotQueue(tmp_path / "queue.json")
    queue.upsert_request(
        demo.audit_id or "demo_public_sample_001",
        status="ready_for_review",
        file_references={
            "report_markdown": "demo/public_sample_001/output/report.md",
            "delivery_packet": "demo/public_sample_001/output/telegram_packet.txt",
        },
    )
    copy = build_approved_delivery_copy(
        audit_id=demo.audit_id or "demo_public_sample_001",
        report_path="demo/public_sample_001/output/report.md",
        delivery_packet_path="demo/public_sample_001/output/telegram_packet.txt",
    )
    result = deliver_approved_report(
        queue=queue,
        audit_id=demo.audit_id or "demo_public_sample_001",
        report_path="demo/public_sample_001/output/report.md",
        delivery_packet_path="demo/public_sample_001/output/telegram_packet.txt",
        sender=client,
    )

    assert "approved for delivery" in copy
    assert result.status == "delivered"
    assert client.network_used is False
    assert client.texts == [
        Path("demo/public_sample_001/output/telegram_packet.txt").read_text(
            encoding="utf-8"
        )
    ]
    assert client.documents == [Path("demo/public_sample_001/output/report.md")]


def test_telegram_demo_happy_path_redacts_sensitive_fields(tmp_path: Path) -> None:
    handlers = TelegramPilotHandlers(
        TelegramAuditStorage(tmp_path / "telegram_workspaces"),
        demo_sample=_public_sample(),
    )
    upload = handlers.handle_document_upload(
        TelegramDocumentUpload(
            file_name="../rules.yaml",
            content=b"schema_version: '1'\naccount_scope: [acct_demo]\n",
        )
    )

    emitted_text = "\n".join(
        (
            handlers.handle_command("/start").text,
            handlers.handle_command("/new_audit").text,
            handlers.handle_command("/demo_sample").text,
            handlers.handle_command("/status", audit_id=upload.audit_id).text,
            upload.text,
        )
    )
    forbidden_fragments = (
        "timestamp,symbol,side,quantity,price",
        "2026-02-03t09:30:00z",
        "@trader",
        "trader@example.com",
        "broker account",
        "private note",
        "acct_public_sample_001",
    )
    lowered = emitted_text.casefold()
    for fragment in forbidden_fragments:
        assert fragment not in lowered


def test_telegram_demo_happy_path_stays_inside_adr_boundary(tmp_path: Path) -> None:
    handlers = TelegramPilotHandlers(
        TelegramAuditStorage(tmp_path / "telegram_workspaces"),
        demo_sample=_public_sample(),
    )

    joined = "\n".join(
        (
            handlers.handle_command("/help").text,
            handlers.handle_command("/new_audit").text,
            handlers.handle_command("/demo_sample").text,
            Path("docs/TELEGRAM_DEMO_FLOW_RU.md").read_text(encoding="utf-8"),
        )
    ).casefold()

    required_boundaries = (
        "operator-approved",
        "adr-001",
        "no broker apis",
        "signal parsing",
        "order blocking",
        "auto-advice",
        "live trading behavior",
    )
    for phrase in required_boundaries:
        assert phrase in joined

    forbidden_runtime_claims = (
        "connect broker",
        "parse signal channel",
        "block orders automatically",
        "execute trades",
        "guarantees profit",
    )
    for phrase in forbidden_runtime_claims:
        assert phrase not in joined


def _public_sample() -> TelegramDemoSample:
    return TelegramDemoSample(
        audit_id="demo_public_sample_001",
        source_label="public/internal demo evidence, not paid pilot evidence",
        report_path=Path("demo/public_sample_001/output/report.md"),
        delivery_packet_path=Path("demo/public_sample_001/output/telegram_packet.txt"),
        starter_profile="hard",
    )
