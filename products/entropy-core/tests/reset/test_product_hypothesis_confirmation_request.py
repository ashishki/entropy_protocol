"""Product hypothesis confirmation request packet tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REQUEST = PROJECT_ROOT / "docs" / "approvals" / "PRODUCT_HYPOTHESIS_CONFIRMATION_REQUEST.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
PHASE_HANDOFF = PROJECT_ROOT / "PHASE_HANDOFF.md"

CURRENT_EVIDENCE = (
    "docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md",
    "docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md",
    "docs/audit/PHASE_GATE_READINESS_REVIEW.md",
    "docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md",
    "docs/audit/HOLDOUT_APPROVAL_DECISION_REVIEW.md",
    "docs/audit/LIVE_FEED_READINESS_REVIEW.md",
    "docs/audit/BROKER_SANDBOX_READINESS_REVIEW.md",
    "docs/research/REPRODUCIBILITY_MATRIX.md",
)


def test_product_hypothesis_request_lists_current_evidence() -> None:
    text = REQUEST.read_text(encoding="utf-8")

    assert "Status: PRODUCT_HYPOTHESIS_CONFIRMATION_REQUEST_LOCAL_ONLY" in text
    assert "confirmation status: not_confirmed_pending_future_validation" in text
    assert "requested next outcome: identify the safest future validation step" in text
    for evidence in CURRENT_EVIDENCE:
        assert f"`{evidence}`" in text
        assert (PROJECT_ROOT / evidence).is_file()
    for option in (
        "archive-only reproducibility extension: allowed_local_only",
        "no-read holdout approval decision packet: allowed_local_only",
        "live-feed fixture replay extension: allowed_local_only",
        "broker sandbox no-capital replay extension: allowed_local_only",
    ):
        assert option in text


def test_product_hypothesis_request_rejects_restricted_actions() -> None:
    text = REQUEST.read_text(encoding="utf-8").lower()

    for missing in (
        "explicit human holdout approval: absent",
        "explicit human live-feed activation approval: absent",
        "explicit human broker/exchange execution approval: absent",
        "explicit human production credential approval: absent",
        "explicit human live capital approval: absent",
        "explicit human production/capital gate approval: absent",
        "product hypothesis confirmation approval: absent",
    ):
        assert missing in text
    for blocked in (
        "holdout read: blocked",
        "holdout unlock: blocked",
        "live feed activation: blocked",
        "live order placement: blocked",
        "live broker/exchange execution: blocked",
        "production credential loading: blocked",
        "production credential deployment: blocked",
        "live capital action: blocked",
        "production label: blocked",
        "capital-ready label: blocked",
    ):
        assert blocked in text
    assert "no restricted action requested: true" in text
    assert "no product hypothesis confirmation claimed: true" in text


def test_state_docs_open_phase13_local_only_decision_work() -> None:
    prompt = CODEX_PROMPT.read_text(encoding="utf-8").lower()
    handoff = PHASE_HANDOFF.read_text(encoding="utf-8").lower()
    combined = f"{prompt}\n{handoff}"

    assert "phase: 14" in prompt
    assert "product hypothesis confirmation decision" in combined
    assert "current active task is t66 local replay evidence delta decision" in prompt
    assert "active task: t66 local replay evidence delta decision" in handoff
    assert "local-only approval decision work" in combined
    assert "no live orders" in combined
    assert "no broker/exchange execution" in combined
    assert "no production credentials" in combined
    assert "no live capital" in combined
    assert "no holdout access" in combined
