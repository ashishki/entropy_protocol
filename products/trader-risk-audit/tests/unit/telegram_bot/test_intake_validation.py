from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.telegram_bot.handlers import TelegramPilotHandlers
from trader_risk_audit.telegram_bot.storage import (
    TelegramAuditStorage,
    TelegramDocumentUpload,
)


def test_invalid_upload_returns_safe_feedback(tmp_path: Path) -> None:
    handlers = TelegramPilotHandlers(TelegramAuditStorage(tmp_path))
    response = handlers.handle_document_upload(
        TelegramDocumentUpload(
            file_name="trades.csv",
            content=(
                b"timestamp,symbol,side,quantity\n"
                b"2026-03-01T10:00:00+00:00,EURUSD,hold,1\n"
            ),
        )
    )
    assert response.audit_id is not None
    metadata = json.loads(
        (tmp_path / response.audit_id / "metadata.json").read_text(encoding="utf-8")
    )
    text = response.text.casefold()

    assert response.status == "needs_user_fix"
    assert metadata["status"] == "needs_user_fix"
    assert "not runnable" in text
    assert "missing canonical fields: price" in text
    assert "2026-03-01t10:00:00+00:00,eurusd,hold,1" not in text
    assert "timestamp,symbol,side,quantity" not in text
