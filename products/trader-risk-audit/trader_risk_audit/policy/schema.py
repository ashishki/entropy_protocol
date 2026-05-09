from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator

SUPPORTED_RULE_TYPES = frozenset(
    {
        "max_daily_loss",
        "max_drawdown",
        "cooldown_after_loss",
        "max_position_size",
        "forbidden_assets",
        "max_leverage",
    }
)

RuleType = Literal[
    "max_daily_loss",
    "max_drawdown",
    "cooldown_after_loss",
    "max_position_size",
    "forbidden_assets",
    "max_leverage",
]


class UnsupportedRuleTypeError(ValueError):
    def __init__(self, rule_id: str, unsupported_type: str) -> None:
        self.rule_id = rule_id
        self.unsupported_type = unsupported_type
        super().__init__(
            f"unsupported rule type {unsupported_type!r} for rule {rule_id!r}"
        )


class SessionDefinition(BaseModel):
    model_config = ConfigDict(frozen=True)

    start: str
    end: str


class PolicyRule(BaseModel):
    model_config = ConfigDict(frozen=True)

    rule_id: str
    type: RuleType
    threshold: Decimal | None = None
    unit: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)

    @field_validator("rule_id")
    @classmethod
    def _rule_id_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("rule_id must not be blank")
        return value


class RiskPolicy(BaseModel):
    model_config = ConfigDict(frozen=True)

    schema_version: str
    account_scope: tuple[str, ...]
    timezone: str
    session: SessionDefinition
    rules: tuple[PolicyRule, ...]

    @field_validator("schema_version", "timezone")
    @classmethod
    def _required_text_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("field must not be blank")
        return value

    @field_validator("account_scope")
    @classmethod
    def _account_scope_must_not_be_empty(
        cls,
        value: tuple[str, ...],
    ) -> tuple[str, ...]:
        if not value:
            raise ValueError("account_scope must not be empty")
        return tuple(account.strip() for account in value)

    @field_validator("rules")
    @classmethod
    def _rules_must_not_be_empty(
        cls,
        value: tuple[PolicyRule, ...],
    ) -> tuple[PolicyRule, ...]:
        if not value:
            raise ValueError("rules must not be empty")
        return value

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "account_scope": list(self.account_scope),
            "rules": [
                {
                    "params": rule.params,
                    "rule_id": rule.rule_id,
                    "threshold": _serialize_decimal(rule.threshold),
                    "type": rule.type,
                    "unit": rule.unit,
                }
                for rule in self.rules
            ],
            "schema_version": self.schema_version,
            "session": self.session.model_dump(mode="json"),
            "timezone": self.timezone,
        }


def load_policy(path: str | Path) -> RiskPolicy:
    policy_path = Path(path)
    with policy_path.open(encoding="utf-8") as policy_file:
        payload = yaml.safe_load(policy_file) or {}
    if not isinstance(payload, dict):
        raise ValueError("policy file must contain a mapping")
    _reject_unsupported_rule_types(payload)
    return RiskPolicy.model_validate(payload)


def serialize_policy(policy: RiskPolicy) -> str:
    return json.dumps(policy.to_canonical_dict(), sort_keys=True, separators=(",", ":"))


def _reject_unsupported_rule_types(payload: dict[str, Any]) -> None:
    rules = payload.get("rules", [])
    if not isinstance(rules, list):
        return
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        rule_type = str(rule.get("type", ""))
        if rule_type not in SUPPORTED_RULE_TYPES:
            raise UnsupportedRuleTypeError(
                rule_id=str(rule.get("rule_id", "")),
                unsupported_type=rule_type,
            )


def _serialize_decimal(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return format(value.normalize(), "f")
