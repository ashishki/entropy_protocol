from __future__ import annotations

from dataclasses import dataclass

from trader_risk_audit.telegram_bot.storage import (
    TelegramAuditStorage,
    TelegramDocumentUpload,
)


@dataclass(frozen=True)
class TelegramHandlerResponse:
    text: str
    audit_id: str | None = None
    status: str | None = None


class TelegramPilotHandlers:
    def __init__(self, storage: TelegramAuditStorage) -> None:
        self._storage = storage

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
                    "Trader Risk Audit intake is ready. Use /new_audit to start a "
                    "local pilot request."
                )
            )
        if normalized == "/help":
            return TelegramHandlerResponse(
                text=(
                    "Commands: /new_audit, /status, /cancel. Send only CSV, YAML, "
                    "Markdown, TXT, or XLSX candidate files. Do not send API keys "
                    "or broker credentials."
                )
            )
        if normalized == "/new_audit":
            return TelegramHandlerResponse(
                text=(
                    "Send trade export, written risk rules, and intake metadata. "
                    "Files are stored locally for operator review."
                ),
                status="awaiting_files",
            )
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
        return TelegramHandlerResponse(
            text=(
                f"Audit request {stored.audit_id} received. Status: received. "
                "Operator review is required before any report delivery."
            ),
            audit_id=stored.audit_id,
            status=stored.status,
        )


def _status_message(audit_id: str | None) -> str:
    if audit_id is None:
        return "No audit id is active. Use /new_audit to start."
    return f"Audit request {audit_id} status: received."
