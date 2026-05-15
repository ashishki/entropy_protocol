"""Trader Risk Audit bridge contract primitives."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from datetime import datetime
from decimal import Decimal
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

TRADER_RISK_AUDIT_BRIDGE_SCHEMA_VERSION = "trader-risk-audit-bridge/v1"

ALLOWED_CORE_PRIMITIVES = (
    "entropy.models.performance.PnLStreams",
    "entropy.attribution.archive_only_attribution_payload",
    "entropy.evidence.build_phase_gate_evidence_packet",
)
FORBIDDEN_CORE_CALLS = (
    "live_broker_api",
    "exchange_api_client",
    "order_blocking",
    "holdout_read",
    "oos_performance_label",
    "production_label",
    "capital_ready_label",
    "registry_write",
    "phase_gate_approval",
)
HUMAN_APPROVAL_BOUNDARIES = (
    "product_bridge_activation",
    "risk_policy_interpretation",
    "ambiguous_export_mapping",
    "new_rule_type",
    "paid_report_delivery",
)
NO_CLAIM_LABELS = (
    "not_live_trading",
    "not_order_blocking",
    "not_oos_performance",
    "not_production",
    "not_capital_ready",
)
LLM_OWNED_FIELD_MARKERS = ("llm", "prompt", "completion", "model_output", "ai_generated")


class BridgeContractError(ValueError):
    """Raised when a product bridge contract boundary is violated."""


class BridgeBaseModel(BaseModel):
    """Base model for deterministic bridge schemas."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    schema_version: Literal["trader-risk-audit-bridge/v1"] = TRADER_RISK_AUDIT_BRIDGE_SCHEMA_VERSION

    @model_validator(mode="after")
    def reject_llm_owned_fields(self) -> "BridgeBaseModel":
        ensure_no_llm_owned_fields(self.model_dump(mode="json"))
        return self


class TraderRiskPolicyRule(BaseModel):
    """One deterministic risk-policy rule exposed through the bridge."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    rule_id: str
    rule_type: Literal[
        "max_daily_loss",
        "max_drawdown",
        "cooldown",
        "position_size",
        "forbidden_asset",
        "leverage",
    ]
    threshold: Decimal
    unit: str
    account_scope: str = "all_accounts"

    @model_validator(mode="after")
    def reject_llm_owned_fields(self) -> "TraderRiskPolicyRule":
        ensure_no_llm_owned_fields(self.model_dump(mode="json"))
        return self


class TraderRiskPolicyBridge(BridgeBaseModel):
    """Risk policy bridge schema."""

    policy_id: str
    approval_id: str
    approved_by: str
    rules: tuple[TraderRiskPolicyRule, ...] = Field(min_length=1)
    deterministic_owner: Literal["core_bridge_contract"] = "core_bridge_contract"


class TraderRiskViolationBridge(BridgeBaseModel):
    """Violation record bridge schema with source-row traceability."""

    violation_id: str
    policy_id: str
    rule_id: str
    source_row_ids: tuple[str, ...] = Field(min_length=1)
    observed_value: Decimal
    threshold: Decimal
    unit: str
    severity: Literal["info", "warning", "breach"]
    occurred_at: datetime
    attributed_pnl: Decimal
    deterministic_owner: Literal["core_bridge_contract"] = "core_bridge_contract"


class TraderRiskAttributionBridge(BridgeBaseModel):
    """Attribution bridge primitive for compliant versus violating P&L."""

    attribution_id: str
    violation_id: str
    source_row_ids: tuple[str, ...] = Field(min_length=1)
    compliant_pnl: Decimal
    violating_pnl: Decimal
    attribution_method_id: Literal["TRA-PNL-ATTR-v1"] = "TRA-PNL-ATTR-v1"


class TraderRiskReportBridge(BridgeBaseModel):
    """Report bridge primitive that preserves no-claim labels."""

    report_id: str
    policy_id: str
    violation_ids: tuple[str, ...]
    report_hash: str
    no_claim_labels: tuple[str, ...] = NO_CLAIM_LABELS
    delivery_approval_required: bool = True


class TraderRiskBridgeContract(BaseModel):
    """Static contract describing the approved Core bridge surface."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    schema_version: Literal["trader-risk-audit-bridge/v1"] = TRADER_RISK_AUDIT_BRIDGE_SCHEMA_VERSION
    allowed_core_primitives: tuple[str, ...] = ALLOWED_CORE_PRIMITIVES
    forbidden_core_calls: tuple[str, ...] = FORBIDDEN_CORE_CALLS
    human_approval_boundaries: tuple[str, ...] = HUMAN_APPROVAL_BOUNDARIES
    no_claim_labels: tuple[str, ...] = NO_CLAIM_LABELS


def get_trader_risk_bridge_contract() -> TraderRiskBridgeContract:
    """Return the static Trader Risk Audit bridge contract."""
    return TraderRiskBridgeContract()


def validate_trader_risk_bridge_request(requested_surfaces: Sequence[str]) -> None:
    """Reject forbidden live, order-blocking, and claim surfaces."""
    forbidden = {_normalize_surface(surface) for surface in FORBIDDEN_CORE_CALLS}
    requested = {_normalize_surface(surface) for surface in requested_surfaces}
    blocked = tuple(sorted(surface for surface in requested if surface in forbidden))
    if blocked:
        raise BridgeContractError(
            "Forbidden Trader Risk Audit bridge surface: " + ", ".join(blocked)
        )


def deterministic_bridge_json(model: BaseModel) -> str:
    """Serialize bridge models with stable key ordering and compact separators."""
    return json.dumps(model.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))


def ensure_no_llm_owned_fields(payload: Mapping[str, object]) -> None:
    """Reject fields that would make runtime truth LLM-owned."""
    for key, value in payload.items():
        normalized_key = _normalize_surface(key)
        if any(marker in normalized_key for marker in LLM_OWNED_FIELD_MARKERS):
            raise BridgeContractError("LLM-owned bridge field is forbidden: " + key)
        if isinstance(value, Mapping):
            ensure_no_llm_owned_fields(value)
        elif isinstance(value, Sequence) and not isinstance(value, str):
            for item in value:
                if isinstance(item, Mapping):
                    ensure_no_llm_owned_fields(item)


def _normalize_surface(value: str) -> str:
    return re_sub_non_word(value.lower()).strip("_")


def re_sub_non_word(value: str) -> str:
    return "".join(character if character.isalnum() else "_" for character in value)


__all__ = [
    "ALLOWED_CORE_PRIMITIVES",
    "FORBIDDEN_CORE_CALLS",
    "HUMAN_APPROVAL_BOUNDARIES",
    "NO_CLAIM_LABELS",
    "TRADER_RISK_AUDIT_BRIDGE_SCHEMA_VERSION",
    "BridgeContractError",
    "TraderRiskAttributionBridge",
    "TraderRiskBridgeContract",
    "TraderRiskPolicyBridge",
    "TraderRiskPolicyRule",
    "TraderRiskReportBridge",
    "TraderRiskViolationBridge",
    "deterministic_bridge_json",
    "ensure_no_llm_owned_fields",
    "get_trader_risk_bridge_contract",
    "validate_trader_risk_bridge_request",
]
