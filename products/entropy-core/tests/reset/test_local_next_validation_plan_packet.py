"""Local next validation plan packet tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PLAN = PROJECT_ROOT / "docs" / "approvals" / "LOCAL_NEXT_VALIDATION_PLAN_PACKET.md"


def test_next_validation_plan_lists_required_sections() -> None:
    text = PLAN.read_text(encoding="utf-8")

    for section in (
        "## Objective",
        "## Hypothesis",
        "## Evidence Inputs",
        "## Candidate Validation Options",
        "## Recommended Next Step",
        "## Prerequisites",
        "## Risks",
        "## Rollback",
        "## Blocked Actions",
        "## Current Confirmation State",
    ):
        assert section in text
    for ref in (
        "docs/approvals/PRODUCT_HYPOTHESIS_CONFIRMATION_REQUEST.md",
        "docs/approvals/PRODUCT_VALIDATION_APPROVAL_INTAKE_CONTRACT.md",
        "docs/approvals/PRODUCT_HYPOTHESIS_VALIDATION_PATH_DECISION.md",
        "tests/reset/test_production_capital_non_approval_regression.py",
        "docs/audit/BROKER_SANDBOX_READINESS_REVIEW.md",
    ):
        assert f"`{ref}`" in text
        assert (PROJECT_ROOT / ref).is_file()


def test_next_validation_plan_records_no_confirmation() -> None:
    text = PLAN.read_text(encoding="utf-8").lower()

    for state in (
        "status: local_next_validation_plan_packet_no_approval",
        "recommendation status: plan_only_not_executed",
        "explicit human validation approval: missing",
        "current approval event: absent",
        "product hypothesis confirmation status: not_confirmed",
        "product hypothesis rejection status: not_rejected",
        "validation execution status: not_started",
        "no restricted execution approved: true",
    ):
        assert state in text


def test_next_validation_plan_rejects_restricted_execution() -> None:
    text = PLAN.read_text(encoding="utf-8").lower()

    for blocked in (
        "holdout read: blocked",
        "holdout unlock: blocked",
        "oos/performance conclusion: blocked",
        "live feed activation: blocked",
        "live order placement: blocked",
        "live broker/exchange execution: blocked",
        "production credential loading: blocked",
        "live capital action: blocked",
        "production label: blocked",
        "capital-ready label: blocked",
    ):
        assert blocked in text
    for rollback in (
        "external rollback required: false",
        "capital rollback required: false",
        "order rollback required: false",
        "credential rotation required: false",
    ):
        assert rollback in text
