"""Reset tests for the Core V2 evidence completeness matrix."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "docs" / "core" / "V2_EVIDENCE_COMPLETENESS_MATRIX.md"


def matrix_text() -> str:
    return " ".join(MATRIX.read_text(encoding="utf-8").lower().split())


def test_matrix_maps_v2_tasks_to_evidence() -> None:
    text = matrix_text()

    for task_id in [f"t{number}" for number in range(123, 137)]:
        assert task_id in text
    for evidence_ref in (
        "docs/core/schema_evolution_policy.md",
        "src/entropy/artifacts/schema_compatibility.py",
        "docs/core/evidence_lookup_policy.md",
        "src/entropy/artifacts/evidence_lookup.py",
        "docs/core/product_bridge_adoption_policy.md",
        "src/entropy/artifacts/product_bridge_adoption.py",
        "tests/fixtures/artifacts/adoption/",
        "tests/reset/test_v2_restricted_surface_sweep.py",
    ):
        assert evidence_ref in text
    assert ".venv/bin/python -m pytest -q" in text


def test_matrix_labels_gaps_without_scope_expansion() -> None:
    text = matrix_text()

    for gap_label in (
        "internal review follow-up, not product readiness",
        "internal validation follow-up, not hosted service readiness",
        "internal evidence limitation, not live/holdout/capital readiness",
    ):
        assert gap_label in text
    for blocked_claim in (
        "not evidence for public sdk availability",
        "hosted service readiness",
        "product runtime ownership",
        "external compliance certification",
        "capital readiness",
        "oos/performance confirmation",
    ):
        assert blocked_claim in text


def test_matrix_references_reviews_and_evidence_index() -> None:
    text = matrix_text()

    for review_ref in (
        "docs/audit/schema_evolution_foundations_review.md",
        "docs/audit/evidence_query_hardening_review.md",
        "docs/audit/product_bridge_adoption_readiness_review.md",
        "docs/audit/v2_internal_kernel_review.md",
    ):
        assert review_ref in text
    for phase_row in (
        "28 schema evolution foundations",
        "29 evidence query hardening",
        "30 product bridge adoption readiness",
        "31 v2 internal kernel review",
    ):
        assert phase_row in text
    for evidence_row in ("t123", "t126", "t127", "t130", "t131", "t134", "t135", "t136"):
        assert evidence_row in text
