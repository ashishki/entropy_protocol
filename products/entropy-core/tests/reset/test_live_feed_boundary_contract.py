"""Live-feed dry-run boundary contract tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BOUNDARY = PROJECT_ROOT / "docs" / "protocols" / "LIVE_FEED_DRY_RUN_BOUNDARY.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
PHASE_HANDOFF = PROJECT_ROOT / "PHASE_HANDOFF.md"


def test_live_feed_boundary_contract_records_allowed_operations() -> None:
    text = BOUNDARY.read_text(encoding="utf-8")

    assert "Status: LIVE_FEED_DRY_RUN_BOUNDARY_LOCAL_ONLY" in text
    for operation in (
        "checked-in fixture schema review",
        "deterministic local market-data fixture replay",
        "local message parsing dry run",
        "local normalization dry run",
        "dry-run clock and timestamp validation",
        "local logging and counter design",
        "local failure-state fixture design",
    ):
        assert operation in text


def test_live_feed_boundary_contract_blocks_external_effects() -> None:
    text = BOUNDARY.read_text(encoding="utf-8")

    for blocked in (
        "live data provider activation: blocked",
        "live feed network connection: blocked",
        "credential loading: blocked",
        "credential deployment: blocked",
        "order placement: blocked",
        "broker/exchange execution: blocked",
        "live capital activation: blocked",
        "production label: blocked",
        "capital-ready label: blocked",
        "external telemetry emission: blocked",
        "holdout read: blocked",
        "holdout unlock: blocked",
    ):
        assert blocked in text
    for false_state in (
        "holdout path opened: false",
        "holdout read executed: false",
        "holdout unlock requested: false",
        "orders sent: false",
        "broker/exchange connection opened: false",
        "live feed connection opened: false",
        "credentials deployed: false",
        "live capital active: false",
    ):
        assert false_state in text


def test_state_docs_record_phase11_local_only_scope() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8").lower()
    handoff = PHASE_HANDOFF.read_text(encoding="utf-8").lower()
    combined = f"{prompt}\n{handoff}"

    assert "phase: 11" in prompt
    assert "phase: 11 live-feed dry run readiness" in handoff
    assert "current active task is t47 live-feed fixture manifest" in prompt
    assert "active task: t47 live-feed fixture manifest" in handoff
    assert "phase 11 is local-only live-feed dry-run readiness" in combined
    for boundary in (
        "order placement",
        "live capital",
        "broker/exchange execution",
        "credentialed production deployment",
        "holdout access",
    ):
        assert boundary in combined
