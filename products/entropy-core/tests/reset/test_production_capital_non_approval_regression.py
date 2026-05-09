"""Production/capital non-approval regression tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
PHASE_HANDOFF = PROJECT_ROOT / "PHASE_HANDOFF.md"
PHASE13_DOCS = (
    PROJECT_ROOT / "docs" / "approvals" / "PRODUCT_HYPOTHESIS_CONFIRMATION_REQUEST.md",
    PROJECT_ROOT / "docs" / "approvals" / "PRODUCT_VALIDATION_APPROVAL_INTAKE_CONTRACT.md",
    PROJECT_ROOT / "docs" / "approvals" / "PRODUCT_HYPOTHESIS_VALIDATION_PATH_DECISION.md",
)


def test_non_approval_sources_are_rejected() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in PHASE13_DOCS)

    for source in (
        "this request packet",
        "roadmap phases",
        "review recommendations",
        "passing tests",
        "protocol documents",
        "readiness artifacts",
        "generated scaffolds",
        "local dry-run packets",
    ):
        assert source in combined
    for rejection in (
        "generated approval: rejected",
        "inferred approval: rejected",
        "stale approval: rejected",
        "revoked approval: rejected",
        "incomplete approval: rejected",
        "overbroad approval: rejected",
    ):
        assert rejection in combined


def test_restricted_action_flags_remain_absent() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in PHASE13_DOCS)

    forbidden_positive_flags = (
        "holdout read: approved",
        "holdout unlock: approved",
        "live order placement: approved",
        "live broker/exchange execution: approved",
        "production credential loading: approved",
        "live capital action: approved",
        "production label: approved",
        "capital-ready label: approved",
        "product hypothesis confirmation status: confirmed",
    )
    for flag in forbidden_positive_flags:
        assert flag not in combined
    for blocked in (
        "holdout read: blocked",
        "holdout unlock: blocked",
        "live order placement: blocked",
        "live broker/exchange execution: blocked",
        "production credential loading: blocked",
        "live capital action: blocked",
        "production label: blocked",
        "capital-ready label: blocked",
    ):
        assert blocked in combined


def test_state_docs_preserve_no_current_approval() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8").lower()
    handoff = PHASE_HANDOFF.read_text(encoding="utf-8").lower()
    combined = f"{prompt}\n{handoff}"

    assert "current active task is t66 local replay evidence delta decision" in prompt
    assert "active task: t66 local replay evidence delta decision" in handoff
    assert "no approval event currently exists" in combined
    for boundary in (
        "real external side effects",
        "holdout reads",
        "holdout unlocks",
        "live order placement",
        "live capital actions",
        "live broker/exchange execution",
        "production credential loading",
        "credentialed production deployment",
    ):
        assert boundary in combined
