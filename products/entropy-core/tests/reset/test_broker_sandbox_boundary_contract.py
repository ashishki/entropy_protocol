"""Broker sandbox boundary contract tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BOUNDARY = PROJECT_ROOT / "docs" / "protocols" / "BROKER_SANDBOX_BOUNDARY.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
PHASE_HANDOFF = PROJECT_ROOT / "PHASE_HANDOFF.md"


def test_broker_sandbox_boundary_records_allowed_operations() -> None:
    text = BOUNDARY.read_text(encoding="utf-8")

    assert "Status: BROKER_SANDBOX_BOUNDARY_SANDBOX_ONLY" in text
    for operation in (
        "local sandbox order scenario review",
        "deterministic sandbox fixture design",
        "sandbox order validation contract design",
        "execution risk limit contract design",
        "local rejection-state fixture design",
        "kill-switch audit contract design",
        "no-capital dry-run packet assembly",
    ):
        assert operation in text
    for control in (
        "sandbox mode required: true",
        "deterministic fixture binding required: true",
        "order validation controls required: true",
        "execution risk limits required: true",
        "kill-switch audit required: true",
        "no-capital dry run required: true",
        "production credential isolation required: true",
    ):
        assert control in text


def test_broker_sandbox_boundary_blocks_live_effects() -> None:
    text = BOUNDARY.read_text(encoding="utf-8")

    for blocked in (
        "live broker/exchange execution: blocked",
        "live order placement: blocked",
        "production credential loading: blocked",
        "production credential deployment: blocked",
        "live capital activation: blocked",
        "real account identifier usage: blocked",
        "production label: blocked",
        "capital-ready label: blocked",
        "external order telemetry: blocked",
        "holdout read: blocked",
        "holdout unlock: blocked",
    ):
        assert blocked in text
    for false_state in (
        "live orders sent: false",
        "sandbox orders emitted from code: false",
        "live broker/exchange connection opened: false",
        "production credentials deployed: false",
        "live capital active: false",
        "holdout path opened: false",
        "holdout read executed: false",
        "holdout unlock requested: false",
    ):
        assert false_state in text


def test_state_docs_record_phase12_sandbox_only_scope() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8").lower()
    handoff = PHASE_HANDOFF.read_text(encoding="utf-8").lower()
    combined = f"{prompt}\n{handoff}"

    assert "phase: 12" in prompt
    assert "phase: 12 broker sandbox and execution risk audit" in handoff
    assert "current active task is t52 broker sandbox fixture manifest" in prompt
    assert "active task: t52 broker sandbox fixture manifest" in handoff
    assert "phase 12 is sandbox-only broker/exchange execution risk audit" in combined
    for boundary in (
        "live order placement",
        "live capital",
        "live broker/exchange execution",
        "production credentials",
        "holdout access",
    ):
        assert boundary in combined
