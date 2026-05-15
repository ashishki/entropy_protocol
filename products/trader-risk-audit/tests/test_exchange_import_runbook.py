from __future__ import annotations

from pathlib import Path

RUNBOOK = Path("docs/AUDIT_WORKSPACE_RUNBOOK_RU.md")
INTAKE = Path("docs/PILOT_INTAKE_CONTRACT_RU.md")
PLAN = Path("docs/EXCHANGE_API_IMPORT_PLAN_RU.md")


def test_exchange_runbook_covers_csv_and_api_paths() -> None:
    text = _combined_docs()

    assert "csv_export" in text
    assert "bybit_read_only_api" in text
    assert "binance_read_only_api" in text
    assert "CSV upload" in text
    assert "read-only API import" in text
    assert "fallback" in text


def test_exchange_runbook_covers_key_safety() -> None:
    text = _combined_docs()

    assert "read-only key" in text
    assert "IP allowlisting" in text
    for forbidden_permission in (
        "trading/order",
        "withdrawal",
        "transfer",
        "leverage/margin",
        "account mutation",
    ):
        assert forbidden_permission in text


def test_exchange_runbook_preserves_boundaries() -> None:
    text = _combined_docs()

    for boundary in (
        "no-advice",
        "no-live-control",
        "no-order-blocking",
        "local secret",
        "no hosted-secret",
        "not SaaS onboarding",
    ):
        assert boundary in text

    assert "must not place" in text
    assert "must not store API keys" in text


def _combined_docs() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8") for path in (RUNBOOK, INTAKE, PLAN)
    )
