"""Core V2 evidence lookup policy contract tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
POLICY = PROJECT_ROOT / "docs" / "core" / "EVIDENCE_LOOKUP_POLICY.md"


def _policy_text() -> str:
    return POLICY.read_text(encoding="utf-8").lower()


def test_policy_distinguishes_local_lookup_from_rag_and_service_scope() -> None:
    text = _policy_text()

    assert "## local lookup boundary" in text
    for blocked_scope in (
        "runtime rag",
        "embedding search",
        "hosted search",
        "public api",
        "public sdk",
        "service behavior",
        "external provider integration",
        "autonomous agent retrieval",
    ):
        assert blocked_scope in text

    assert "must not retrieve from the network" in text


def test_policy_defines_inputs_results_missing_evidence_and_redaction() -> None:
    text = _policy_text()

    for heading in (
        "## allowed query inputs",
        "## result metadata",
        "## missing evidence behavior",
        "## redaction expectations",
    ):
        assert heading in text

    for field in (
        "query",
        "status",
        "topic",
        "artifact_type",
        "locations",
        "scope_covered",
        "last_verified",
        "canonical",
        "reason_code",
        "approval_state",
    ):
        assert f"`{field}`" in text

    assert "insufficient_evidence" in text
    assert "must not fabricate citations" in text


def test_policy_preserves_blocked_surfaces() -> None:
    text = _policy_text()

    assert "## blocked surfaces" in text
    for blocked in (
        "holdout read or unlock",
        "oos/performance conclusions",
        "live feeds by default",
        "broker/exchange execution",
        "order placement or order blocking",
        "live capital",
        "production credentials",
        "production labels",
        "capital-ready labels",
        "public sdk",
        "hosted service or saas",
        "public api",
        "runtime rag or embeddings",
        "external compliance certification",
        "enterprise sla claims",
    ):
        assert blocked in text
