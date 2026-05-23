from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_ai_development_plan_has_execution_tracks_and_phases() -> None:
    plan = (PROJECT_ROOT / "docs/AI_DEVELOPMENT_PLAN_RU.md").read_text(encoding="utf-8")

    for required in (
        "External-ready trust",
        "Quant quality",
        "Review operations",
        "Provider/media coverage",
        "Product packaging",
        "Phase 28 - External-Ready Review Sprint",
        "Phase 35 - Reliability And Scaling",
        "Phase 36 - Channel Impact Framework And Cross-Channel Completion",
        "Phase 37 - Pre-Client Artifact Hardening",
    ):
        assert required in plan


def test_ai_development_plan_preserves_product_guardrails() -> None:
    plan = (PROJECT_ROOT / "docs/AI_DEVELOPMENT_PLAN_RU.md").read_text(encoding="utf-8")

    for required in (
        "No private Telegram scraping",
        "Никакого investment advice",
        "Unsupported providers/proxies считаются exclusions",
        "Customer-facing отчет проходит external-ready gate",
        "approve_internal_only",
    ):
        assert required in plan


def test_ai_development_plan_names_next_action_and_validation() -> None:
    plan = (PROJECT_ROOT / "docs/AI_DEVELOPMENT_PLAN_RU.md").read_text(encoding="utf-8")

    assert "Phase 37 - Pre-Client Artifact Hardening" in plan
    assert ".venv/bin/python -m pytest tests/ -q" in plan
    assert ".venv/bin/ruff check src/ tests/ scripts/" in plan
