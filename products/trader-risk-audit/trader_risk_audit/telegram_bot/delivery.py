from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from trader_risk_audit.pilot_queue import PilotQueue
from trader_risk_audit.reporting.claim_guard import (
    REQUIRED_DISCLAIMER,
    ensure_report_claims_valid,
)


class TelegramDeliveryError(ValueError):
    pass


class TelegramDeliverySender(Protocol):
    def send_text(self, text: str) -> None: ...

    def send_document(self, path: Path) -> None: ...


@dataclass(frozen=True)
class TelegramDeliveryResult:
    audit_id: str
    status: str
    report_path: Path
    packet_path: Path


def deliver_approved_report(
    *,
    queue: PilotQueue,
    audit_id: str,
    report_path: str | Path,
    delivery_packet_path: str | Path,
    sender: TelegramDeliverySender,
) -> TelegramDeliveryResult:
    request = queue.get_request(audit_id)
    if request.status != "ready_for_review":
        raise TelegramDeliveryError("delivery requires ready_for_review status")

    report = Path(report_path)
    packet = Path(delivery_packet_path)
    _require_existing_file(report, label="report")
    _require_existing_file(packet, label="delivery packet")

    report_text = report.read_text(encoding="utf-8")
    packet_text = packet.read_text(encoding="utf-8")
    ensure_report_claims_valid(report_text)
    if REQUIRED_DISCLAIMER.casefold() not in packet_text.casefold():
        raise TelegramDeliveryError("delivery packet is missing required disclaimer")

    sender.send_text(packet_text)
    sender.send_document(report)
    delivered = queue.set_status(audit_id, "delivered")
    return TelegramDeliveryResult(
        audit_id=delivered.audit_id,
        status=delivered.status,
        report_path=report,
        packet_path=packet,
    )


def build_approved_delivery_copy(
    *,
    audit_id: str,
    report_path: str | Path,
    delivery_packet_path: str | Path,
) -> str:
    report = Path(report_path)
    packet = Path(delivery_packet_path)
    _require_existing_file(report, label="report")
    _require_existing_file(packet, label="delivery packet")

    packet_text = packet.read_text(encoding="utf-8")
    if REQUIRED_DISCLAIMER.casefold() not in packet_text.casefold():
        raise TelegramDeliveryError("delivery packet is missing required disclaimer")
    return "\n".join(
        (
            f"Audit {audit_id} approved for delivery.",
            "Status: ready_for_review",
            "Operator approval required before sending.",
            f"Report: {report}",
            "",
            packet_text,
        )
    )


def _require_existing_file(path: Path, *, label: str) -> None:
    if not path.is_file():
        raise TelegramDeliveryError(f"{label} file is missing")
