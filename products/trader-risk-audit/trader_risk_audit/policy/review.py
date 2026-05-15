from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from trader_risk_audit.policy.schema import PolicyRule, RiskPolicy


@dataclass(frozen=True)
class ReviewPacketItem:
    rule_id: str
    source_text: str
    missing_deterministic_fields: tuple[str, ...]
    required_operator_decision: str
    resolved: bool = False


@dataclass(frozen=True)
class PolicyReviewPacket:
    items: tuple[ReviewPacketItem, ...]

    @property
    def unresolved_items(self) -> tuple[ReviewPacketItem, ...]:
        return tuple(item for item in self.items if not item.resolved)


@dataclass(frozen=True)
class ReviewDecision:
    rule_id: str
    deterministic_fields: Mapping[str, Any]


def build_review_packet(policy: RiskPolicy) -> PolicyReviewPacket:
    return PolicyReviewPacket(
        items=tuple(
            item
            for rule in policy.rules
            if (item := _review_item_for_rule(rule)) is not None
        )
    )


def apply_review_decisions(
    policy: RiskPolicy,
    decisions: Iterable[ReviewDecision],
) -> RiskPolicy:
    decisions_by_rule = {decision.rule_id: decision for decision in decisions}
    updated_rules = tuple(
        _apply_decision_to_rule(rule, decisions_by_rule[rule.rule_id])
        if rule.rule_id in decisions_by_rule
        else rule
        for rule in policy.rules
    )
    return RiskPolicy.model_validate(
        {
            **policy.model_dump(mode="python"),
            "rules": [rule.model_dump(mode="python") for rule in updated_rules],
        }
    )


def _review_item_for_rule(rule: PolicyRule) -> ReviewPacketItem | None:
    missing_fields = _missing_deterministic_fields(rule)
    if not missing_fields:
        return None
    source_text = str(rule.params.get("source_text", "")).strip()
    return ReviewPacketItem(
        rule_id=rule.rule_id,
        source_text=source_text,
        missing_deterministic_fields=missing_fields,
        required_operator_decision=(
            "Approve deterministic values for "
            + ", ".join(missing_fields)
            + " before evaluation."
        ),
    )


def _missing_deterministic_fields(rule: PolicyRule) -> tuple[str, ...]:
    missing: list[str] = []
    if rule.type in {
        "max_daily_loss",
        "max_drawdown",
        "cooldown_after_loss",
        "max_position_size",
        "max_leverage",
    }:
        if rule.threshold is None:
            missing.append("threshold")
        if not rule.unit:
            missing.append("unit")
    if rule.type == "forbidden_assets" and not rule.params.get("symbols"):
        missing.append("params.symbols")
    return tuple(missing)


def _apply_decision_to_rule(rule: PolicyRule, decision: ReviewDecision) -> PolicyRule:
    data = rule.model_dump(mode="python")
    params = dict(data.get("params", {}))
    for field, value in decision.deterministic_fields.items():
        if field.startswith("params."):
            params[field.removeprefix("params.")] = value
        elif field == "params":
            params.update(value)
        else:
            data[field] = value
    data["params"] = params
    return PolicyRule.model_validate(data)
