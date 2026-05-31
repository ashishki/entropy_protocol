"""Reset tests for the Core V2 kernel foundation inventory."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "docs" / "core" / "V2_KERNEL_FOUNDATION_INVENTORY.md"


def inventory_text() -> str:
    return " ".join(INVENTORY.read_text(encoding="utf-8").lower().split())


def test_inventory_lists_v2_foundations() -> None:
    text = inventory_text()

    assert "schema evolution foundations" in text
    assert "schema_compatibility.py" in text
    assert "evidence query hardening" in text
    assert "evidence_lookup.py" in text
    assert "product bridge adoption readiness" in text
    assert "product_bridge_adoption.py" in text
    assert "tests/fixtures/artifacts/adoption/" in text


def test_inventory_preserves_internal_kernel_boundary() -> None:
    text = inventory_text()

    assert "internal entropy core kernel only" in text
    assert "core v2 does not own" in text
    for blocked_surface in (
        "public sdk",
        "hosted service",
        "runtime rag",
        "product runtime execution",
        "product report authorship",
        "product workspace edits",
        "external delivery approval",
        "external compliance certification",
    ):
        assert blocked_surface in text


def test_inventory_records_evidence_gaps_without_readiness_claims() -> None:
    text = inventory_text()

    assert "internal evidence gap, not a product-readiness blocker" in text
    assert "not hosted/live/holdout/capital readiness evidence" in text
    assert "not public sdk or compliance readiness evidence" in text
    for unsupported_claim in (
        "does not claim product readiness",
        "hosted service readiness",
        "live execution readiness",
        "holdout readiness",
        "capital readiness",
        "oos/performance confirmation",
    ):
        assert unsupported_claim in text
