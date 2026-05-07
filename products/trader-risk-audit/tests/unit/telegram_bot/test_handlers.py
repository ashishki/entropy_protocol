from __future__ import annotations

import json
from pathlib import Path

import pytest

from trader_risk_audit.telegram_bot.bot import TelegramBotConfigError, load_bot_config
from trader_risk_audit.telegram_bot.handlers import TelegramPilotHandlers
from trader_risk_audit.telegram_bot.storage import (
    TelegramAuditStorage,
    TelegramDocumentUpload,
)


def test_bot_requires_explicit_enable_and_token(tmp_path: Path) -> None:
    with pytest.raises(TelegramBotConfigError, match="ENABLED"):
        load_bot_config({})

    with pytest.raises(TelegramBotConfigError, match="TOKEN"):
        load_bot_config({"TRA_TELEGRAM_BOT_ENABLED": "true"})

    config = load_bot_config(
        {
            "TRA_TELEGRAM_BOT_ENABLED": "true",
            "TRA_TELEGRAM_BOT_TOKEN": "test-token-from-env",
            "TRA_TELEGRAM_WORKSPACE_DIR": str(tmp_path),
        }
    )

    assert config.enabled is True
    assert config.token == "test-token-from-env"
    assert config.workspace_dir == tmp_path


def test_core_commands_return_safe_messages(tmp_path: Path) -> None:
    handlers = TelegramPilotHandlers(TelegramAuditStorage(tmp_path))

    responses = [
        handlers.handle_command("/start"),
        handlers.handle_command("/help"),
        handlers.handle_command("/new_audit"),
        handlers.handle_command("/status", audit_id="audit_demo_001"),
        handlers.handle_command("/cancel"),
    ]

    joined = "\n".join(response.text for response in responses).casefold()
    assert "audit_demo_001 status: received" in joined
    assert "api keys" in joined
    assert "broker credentials" in joined
    assert "timestamp,symbol,side,quantity,price" not in joined
    assert "buy,1,100" not in joined
    assert "investment advice" not in joined


def test_document_upload_creates_local_audit_request(tmp_path: Path) -> None:
    handlers = TelegramPilotHandlers(TelegramAuditStorage(tmp_path))
    upload = TelegramDocumentUpload(
        file_name="../trades.csv",
        content=b"timestamp,symbol,side,quantity,price\n2026-03-01,EURUSD,buy,1,100\n",
    )

    first_response = handlers.handle_document_upload(upload)
    second_response = handlers.handle_document_upload(upload)

    assert first_response.audit_id == second_response.audit_id
    assert first_response.status == "received"
    assert first_response.audit_id is not None
    workspace_root = tmp_path / first_response.audit_id
    stored_file = workspace_root / "input" / "trades.csv"
    metadata = json.loads(
        (workspace_root / "metadata.json").read_text(encoding="utf-8")
    )

    assert stored_file.read_bytes() == upload.content
    assert metadata["status"] == "received"
    assert metadata["file_references"] == {"telegram_upload": "input/trades.csv"}
    assert "Status: received" in first_response.text
    assert "timestamp,symbol,side,quantity,price" not in first_response.text
