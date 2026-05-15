from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from trader_risk_audit.policy.profiles import format_policy_profile_selector_copy
from trader_risk_audit.telegram_bot.storage import (
    TelegramAuditStorage,
    TelegramDocumentUpload,
)


@dataclass(frozen=True)
class TelegramHandlerResponse:
    text: str
    audit_id: str | None = None
    status: str | None = None


@dataclass(frozen=True)
class TelegramDemoSample:
    audit_id: str
    source_label: str
    report_path: Path
    delivery_packet_path: Path
    starter_profile: str


class TelegramPilotHandlers:
    def __init__(
        self,
        storage: TelegramAuditStorage,
        *,
        demo_sample: TelegramDemoSample | None = None,
    ) -> None:
        self._storage = storage
        self._demo_sample = demo_sample

    def handle_command(
        self,
        command: str,
        *,
        audit_id: str | None = None,
    ) -> TelegramHandlerResponse:
        normalized = command.strip().casefold()
        if normalized == "/start":
            return TelegramHandlerResponse(
                text=(
                    "Trader Risk Audit demo is ready. Use /new_audit to upload "
                    "audit files, or /demo_sample to view the public sample demo."
                )
            )
        if normalized == "/help":
            return TelegramHandlerResponse(
                text=(
                    "Commands: /start, /new_audit, /profiles, /demo_sample, "
                    "/status, /cancel. Send only CSV, YAML, Markdown, TXT, or "
                    "XLSX candidate files. Do not send API keys or broker "
                    "credentials."
                )
            )
        if normalized == "/new_audit":
            return TelegramHandlerResponse(
                text=(
                    "Send trade export, written risk rules, and intake metadata. "
                    "Select soft, medium, hard, or custom policy profile; custom "
                    "requires written risk rules. "
                    "Files are stored locally for operator review. To avoid sharing "
                    "private files first, use /demo_sample."
                ),
                status="awaiting_files",
            )
        if normalized == "/profiles":
            return TelegramHandlerResponse(text=format_policy_profile_selector_copy())
        if normalized == "/demo_sample":
            return self._demo_sample_response()
        if normalized == "/status":
            return TelegramHandlerResponse(
                text=_status_message(audit_id),
                audit_id=audit_id,
                status="received" if audit_id else None,
            )
        if normalized == "/cancel":
            return TelegramHandlerResponse(
                text="Current intake draft is cancelled. No audit was run.",
                status="cancelled",
            )
        return TelegramHandlerResponse(
            text="Unsupported command. Use /help for allowed intake commands."
        )

    def handle_document_upload(
        self,
        upload: TelegramDocumentUpload,
    ) -> TelegramHandlerResponse:
        stored = self._storage.store_upload(upload)
        if stored.status == "needs_user_fix":
            text = (
                f"Audit request {stored.audit_id} received but is not runnable. "
                f"{stored.validation_feedback}"
            )
        else:
            text = (
                f"Audit request {stored.audit_id} received. Status: received. "
                "Operator review is required before any report delivery."
            )
        return TelegramHandlerResponse(
            text=text,
            audit_id=stored.audit_id,
            status=stored.status,
        )

    def _demo_sample_response(self) -> TelegramHandlerResponse:
        if self._demo_sample is None:
            return TelegramHandlerResponse(
                text=(
                    "Public sample demo is not configured. Use /new_audit to start "
                    "a local pilot request."
                )
            )
        sample = self._demo_sample
        return TelegramHandlerResponse(
            text=(
                f"Demo audit {sample.audit_id} is ready for operator-approved "
                f"delivery. Source: {sample.source_label}. Starter profile: "
                f"{sample.starter_profile}. Report: {sample.report_path}. "
                f"Delivery packet: {sample.delivery_packet_path}."
            ),
            audit_id=sample.audit_id,
            status="ready_for_review",
        )


def _status_message(audit_id: str | None) -> str:
    if audit_id is None:
        return "No audit id is active. Use /new_audit to start."
    return f"Audit request {audit_id} status: received."
