"""Core V2 product bridge adoption policy contract tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
POLICY = PROJECT_ROOT / "docs" / "core" / "PRODUCT_BRIDGE_ADOPTION_POLICY.md"


def _policy_text() -> str:
    return POLICY.read_text(encoding="utf-8").lower()


def test_policy_distinguishes_core_validation_from_product_runtime() -> None:
    text = _policy_text()

    assert "## core validation boundary" in text
    for allowed in (
        "product bridge profile identifiers",
        "artifact schema overlays",
        "synthetic fixture validation",
        "no-claim and blocked-surface checks",
        "local readiness results for core adoption",
    ):
        assert allowed in text
    for forbidden in (
        "product runtime behavior",
        "product report authorship",
        "product policy interpretation",
        "product workspace edits",
        "customer delivery decisions",
        "hosted service behavior",
    ):
        assert forbidden in text


def test_policy_defines_readiness_inputs_fixtures_failures_and_evidence() -> None:
    text = _policy_text()

    for heading in (
        "## adoption readiness inputs",
        "## synthetic fixture requirements",
        "## failure handling",
        "## evidence expectations",
    ):
        assert heading in text

    for field in (
        "profile_id",
        "artifact_contract_version",
        "synthetic_fixture_refs",
        "evidence_refs",
        "allowed_core_primitives",
        "forbidden_product_calls",
        "no_claim_boundaries",
        "blocked_surfaces",
        "owner",
        "reviewer",
    ):
        assert f"`{field}`" in text

    assert "real customer data" in text
    assert "private product artifacts" in text
    assert "safe reason codes" in text


def test_policy_preserves_blocked_surfaces() -> None:
    text = _policy_text()

    assert "## blocked surfaces" in text
    for blocked in (
        "product workspace edits from core",
        "product runtime ownership",
        "product report authorship",
        "external delivery approval",
        "public sdk",
        "hosted service or saas",
        "public api",
        "live feeds by default",
        "broker/exchange execution",
        "order placement or order blocking",
        "holdout read or unlock",
        "production credentials",
        "capital-ready labels",
        "external compliance certification",
        "enterprise sla claims",
    ):
        assert blocked in text
