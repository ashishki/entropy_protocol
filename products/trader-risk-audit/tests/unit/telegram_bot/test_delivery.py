from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from trader_risk_audit.pilot_queue import PilotQueue
from trader_risk_audit.reporting.claim_guard import REQUIRED_DISCLAIMER
from trader_risk_audit.telegram_bot.delivery import (
    TelegramDeliveryError,
    deliver_approved_report,
)


@dataclass
class FakeSender:
    texts: list[str] = field(default_factory=list)
    documents: list[Path] = field(default_factory=list)

    def send_text(self, text: str) -> None:
        self.texts.append(text)

    def send_document(self, path: Path) -> None:
        self.documents.append(path)


def test_delivery_requires_ready_for_review_status(tmp_path: Path) -> None:
    queue = PilotQueue(tmp_path / "queue.json")
    queue.upsert_request("audit_delivery", status="received")
    report, packet = _write_delivery_artifacts(tmp_path)

    with pytest.raises(TelegramDeliveryError, match="ready_for_review"):
        deliver_approved_report(
            queue=queue,
            audit_id="audit_delivery",
            report_path=report,
            delivery_packet_path=packet,
            sender=FakeSender(),
        )

    queue.set_status("audit_delivery", "ready_for_review")
    missing = tmp_path / "missing.md"
    with pytest.raises(TelegramDeliveryError, match="report file is missing"):
        deliver_approved_report(
            queue=queue,
            audit_id="audit_delivery",
            report_path=missing,
            delivery_packet_path=packet,
            sender=FakeSender(),
        )


def test_delivery_requires_claim_guard_pass(tmp_path: Path) -> None:
    queue = PilotQueue(tmp_path / "queue.json")
    queue.upsert_request("audit_claims", status="ready_for_review")
    report, packet = _write_delivery_artifacts(
        tmp_path,
        report_text="This report guarantees profit.",
    )

    with pytest.raises(ValueError, match="claim guard"):
        deliver_approved_report(
            queue=queue,
            audit_id="audit_claims",
            report_path=report,
            delivery_packet_path=packet,
            sender=FakeSender(),
        )


def test_delivery_sends_summary_report_and_marks_delivered(tmp_path: Path) -> None:
    queue = PilotQueue(tmp_path / "queue.json")
    queue.upsert_request("audit_success", status="ready_for_review")
    report, packet = _write_delivery_artifacts(tmp_path)
    sender = FakeSender()

    result = deliver_approved_report(
        queue=queue,
        audit_id="audit_success",
        report_path=report,
        delivery_packet_path=packet,
        sender=sender,
    )

    assert result.status == "delivered"
    assert queue.get_request("audit_success").status == "delivered"
    assert sender.texts == [packet.read_text(encoding="utf-8")]
    assert sender.documents == [report]
    assert REQUIRED_DISCLAIMER in sender.texts[0]


def _write_delivery_artifacts(
    tmp_path: Path,
    *,
    report_text: str | None = None,
) -> tuple[Path, Path]:
    report = tmp_path / "report.md"
    packet = tmp_path / "telegram_packet.txt"
    report.write_text(
        report_text
        or f"# Trader Risk Audit Report\n\n{REQUIRED_DISCLAIMER}\n\n## Summary\n",
        encoding="utf-8",
    )
    packet.write_text(
        f"Trader Risk Audit Summary\n{REQUIRED_DISCLAIMER}\n",
        encoding="utf-8",
    )
    return report, packet
