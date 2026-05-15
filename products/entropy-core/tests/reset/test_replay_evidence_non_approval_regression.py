"""Replay evidence non-approval regression tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
APPROVAL = PROJECT_ROOT / "docs" / "approvals" / "LOCAL_BROKER_SANDBOX_REPLAY_APPROVAL_EVENT.md"
RESULT = PROJECT_ROOT / "docs" / "protocols" / "BROKER_SANDBOX_NO_CAPITAL_REPLAY_RESULT.md"
DELTA = PROJECT_ROOT / "docs" / "approvals" / "LOCAL_REPLAY_EVIDENCE_DELTA_DECISION.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
PHASE_HANDOFF = PROJECT_ROOT / "PHASE_HANDOFF.md"


def test_replay_packets_are_not_restricted_approvals() -> None:
    combined = _combined_replay_text()

    for fragment in (
        "maximum allowed effect: local_no_effect_only",
        "restricted validation execution: not_approved",
        "external side effect execution: not_approved",
        "evidence sufficient for restricted validation approval: false",
        "no approval event created: true",
    ):
        assert fragment in combined
    for blocked in (
        "sandbox order emission from code: blocked",
        "live order placement: blocked",
        "live broker/exchange execution: blocked",
        "production credential loading: blocked",
        "live capital action: blocked",
        "holdout read: blocked",
        "holdout unlock: blocked",
    ):
        assert blocked in combined


def test_replay_evidence_cannot_create_claim_labels() -> None:
    combined = _combined_replay_text()

    for status in (
        "product hypothesis confirmation status: not_confirmed",
        "product hypothesis rejection status: not_rejected",
        "product hypothesis confirmation status: not_confirmed",
        "product hypothesis rejection status: not_rejected",
        "production/capital readiness status: not_claimed",
        "oos/performance conclusion status: not_claimed",
        "no production readiness claimed: true",
        "no capital-ready status claimed: true",
        "no oos/performance conclusion claimed: true",
        "evidence sufficient for product confirmation: false",
        "evidence sufficient for product rejection: false",
    ):
        assert status in combined
    for blocked_claim in (
        "oos/performance conclusion: blocked",
        "production label: blocked",
        "capital-ready label: blocked",
    ):
        assert blocked_claim in combined


def test_state_docs_keep_restricted_surfaces_blocked() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8").lower()
    handoff = PHASE_HANDOFF.read_text(encoding="utf-8").lower()
    combined = f"{prompt}\n{handoff}"

    assert "t122 core v1 productization review completed" in prompt
    assert "active task: none - core v1 checkpoint complete" in handoff
    assert "t66-t68 remain pending but deferred" in combined
    assert "phase 14 replay work complete through t65" in combined
    for boundary in (
        "real external side effects",
        "holdout reads",
        "holdout unlocks",
        "live capital actions",
        "live broker/exchange execution",
        "production credential loading",
        "credentialed production deployment",
        "external sandbox order emission",
    ):
        assert boundary in combined


def _combined_replay_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in (
            APPROVAL,
            RESULT,
            DELTA,
        )
    )
