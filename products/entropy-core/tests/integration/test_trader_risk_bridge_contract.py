"""Trader Risk Audit bridge contract tests."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from entropy.bridges import (
    TRADER_RISK_AUDIT_BRIDGE_SCHEMA_VERSION,
    BridgeContractError,
    TraderRiskPolicyBridge,
    TraderRiskPolicyRule,
    TraderRiskViolationBridge,
    deterministic_bridge_json,
    ensure_no_llm_owned_fields,
    get_trader_risk_bridge_contract,
    validate_trader_risk_bridge_request,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BRIDGE_DOC = PROJECT_ROOT / "docs" / "bridges" / "trader-risk-audit.md"


def test_bridge_contract_lists_allowed_and_forbidden_surfaces() -> None:
    contract = get_trader_risk_bridge_contract()
    document = BRIDGE_DOC.read_text(encoding="utf-8")

    assert contract.schema_version == TRADER_RISK_AUDIT_BRIDGE_SCHEMA_VERSION
    assert TRADER_RISK_AUDIT_BRIDGE_SCHEMA_VERSION in document
    for primitive in contract.allowed_core_primitives:
        assert primitive in document
    for forbidden_call in contract.forbidden_core_calls:
        assert forbidden_call in document
    for boundary in contract.human_approval_boundaries:
        assert boundary in document
    assert "Contract only" in document


def test_bridge_schemas_are_deterministic_and_no_llm_owned_fields() -> None:
    policy = TraderRiskPolicyBridge(
        policy_id="policy-max-daily-loss",
        approval_id="approval-001",
        approved_by="risk-owner",
        rules=(
            TraderRiskPolicyRule(
                rule_id="rule-max-daily-loss",
                rule_type="max_daily_loss",
                threshold=Decimal("500.00"),
                unit="USD",
            ),
        ),
    )
    violation = TraderRiskViolationBridge(
        violation_id="violation-001",
        policy_id=policy.policy_id,
        rule_id="rule-max-daily-loss",
        source_row_ids=("row-001", "row-002"),
        observed_value=Decimal("650.00"),
        threshold=Decimal("500.00"),
        unit="USD",
        severity="breach",
        occurred_at=datetime(2026, 5, 7, 12, 0, tzinfo=timezone.utc),
        attributed_pnl=Decimal("-150.00"),
    )

    assert deterministic_bridge_json(policy) == deterministic_bridge_json(policy)
    assert deterministic_bridge_json(violation) == deterministic_bridge_json(violation)
    assert deterministic_bridge_json(policy).startswith('{"approval_id"')
    assert "llm" not in deterministic_bridge_json(policy).lower()
    assert "prompt" not in deterministic_bridge_json(violation).lower()

    with pytest.raises(BridgeContractError, match="LLM-owned"):
        ensure_no_llm_owned_fields({"llm_summary": "not allowed"})


@pytest.mark.parametrize(
    "requested_surface",
    [
        "live_broker_api",
        "exchange_api_client",
        "order_blocking",
        "production_label",
        "capital_ready_label",
        "oos_performance_label",
    ],
)
def test_bridge_rejects_live_and_claim_surfaces(requested_surface: str) -> None:
    with pytest.raises(BridgeContractError, match="Forbidden Trader Risk Audit bridge surface"):
        validate_trader_risk_bridge_request((requested_surface,))

    validate_trader_risk_bridge_request(("risk_policy_schema", "violation_record_schema"))
