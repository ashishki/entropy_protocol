"""Live-feed adapter dry-run contract tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACT = PROJECT_ROOT / "docs" / "protocols" / "LIVE_FEED_ADAPTER_DRY_RUN_CONTRACT.md"
MANIFEST = PROJECT_ROOT / "docs" / "protocols" / "LIVE_FEED_FIXTURE_MANIFEST.md"


def test_adapter_dry_run_contract_records_local_checks() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    assert "Status: LIVE_FEED_ADAPTER_DRY_RUN_CONTRACT_LOCAL_ONLY" in text
    assert "`docs/protocols/LIVE_FEED_FIXTURE_MANIFEST.md`" in text
    assert MANIFEST.is_file()
    for check in (
        "parser input contract: checked-in fixture messages only",
        "parser output contract: deterministic normalized message objects",
        "normalization check: schema-bound field normalization",
        "timestamp check: fixed replay clock only",
        "replay ordering check: deterministic fixture order",
        "failure-state check: malformed local fixture handling",
        "idempotence check: repeated replay produces identical normalized output",
    ):
        assert check in text
    assert "adapter mode: local dry run" in text
    assert "source data: checked-in deterministic fixtures" in text


def test_adapter_dry_run_contract_rejects_external_paths() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    for blocked in (
        "network sockets opened: false",
        "live feed connection opened: false",
        "credential loading: blocked",
        "provider activation: blocked",
        "order placement: blocked",
        "broker/exchange execution: blocked",
        "external telemetry emission: blocked",
    ):
        assert blocked in text
    for rejected in (
        "live provider endpoint: rejected",
        "raw API key: rejected",
        "credential environment variable: rejected",
        "network socket: rejected",
        "websocket stream: rejected",
        "REST polling: rejected",
        "order router: rejected",
        "broker/exchange session: rejected",
        "live capital action: rejected",
        "holdout read: rejected",
        "holdout unlock: rejected",
    ):
        assert rejected in text


def test_adapter_dry_run_contract_rejects_claims() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    for rejected in (
        "production readiness: rejected",
        "capital-ready conclusion: rejected",
        "OOS/performance conclusion: rejected",
        "live-feed activation: rejected",
        "broker/exchange activation: rejected",
    ):
        assert rejected in text
    assert "orders sent: false" in text
    assert "live capital active: false" in text
    assert "current holdout approval event: absent" in text
