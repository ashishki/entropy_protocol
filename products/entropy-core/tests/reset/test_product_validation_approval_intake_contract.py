"""Product validation approval intake contract tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACT = PROJECT_ROOT / "docs" / "approvals" / "PRODUCT_VALIDATION_APPROVAL_INTAKE_CONTRACT.md"

EVIDENCE_REFS = (
    "docs/approvals/PRODUCT_HYPOTHESIS_CONFIRMATION_REQUEST.md",
    "docs/audit/BROKER_SANDBOX_READINESS_REVIEW.md",
    "docs/audit/HOLDOUT_APPROVAL_DECISION_REVIEW.md",
    "docs/audit/LIVE_FEED_READINESS_REVIEW.md",
    "docs/research/REPRODUCIBILITY_MATRIX.md",
)


def test_product_validation_intake_lists_required_fields() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    assert "Status: PRODUCT_VALIDATION_APPROVAL_INTAKE_CONTRACT_NO_APPROVAL" in text
    for field in (
        "`approval_event_id`",
        "`approval_type`",
        "`scope`",
        "`validation_path`",
        "`human_approver`",
        "`risk_owner`",
        "`requested_by`",
        "`created_at_utc`",
        "`expires_at_utc`",
        "`revocation_status`",
        "`approval_status`",
        "`evidence_packet_hash`",
        "`risk_signoff_hash`",
        "`rollback_plan_hash`",
        "`maximum_allowed_effect`",
        "`blocked_action_overrides`",
    ):
        assert field in text
    for ref in EVIDENCE_REFS:
        assert f"`{ref}`" in text
        assert (PROJECT_ROOT / ref).is_file()


def test_product_validation_intake_rejects_invalid_approvals() -> None:
    text = CONTRACT.read_text(encoding="utf-8").lower()

    for rejected in (
        "approval source: explicit_human_operator_only",
        "generated approval: rejected",
        "inferred approval: rejected",
        "stale approval: rejected",
        "revoked approval: rejected",
        "incomplete approval: rejected",
        "overbroad approval: rejected",
        "missing expiry: rejected",
        "missing risk owner: rejected",
        "missing rollback plan hash: rejected",
        "missing evidence packet hash: rejected",
        "blocked action override present: rejected",
    ):
        assert rejected in text


def test_product_validation_intake_preserves_no_approval_state() -> None:
    text = CONTRACT.read_text(encoding="utf-8").lower()

    for state in (
        "current approval event: absent",
        "intake decision: rejected",
        "rejection reason: missing_explicit_human_validation_approval",
        "product hypothesis confirmation approval: absent",
        "holdout approval: absent",
        "live-feed activation approval: absent",
        "broker/exchange execution approval: absent",
        "production credential approval: absent",
        "live capital approval: absent",
    ):
        assert state in text
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
    assert "no approval event created: true" in text
    assert "no product hypothesis confirmation claimed: true" in text
