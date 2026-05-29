from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, cast

import yaml

from trader_risk_audit.policy.profiles import STARTER_POLICY_DIR, STARTER_PROFILES
from trader_risk_audit.policy.rule_catalog import list_rule_catalog
from trader_risk_audit.policy.schema import (
    PolicyRule,
    RiskPolicy,
    RuleType,
    SessionDefinition,
    load_policy,
)


class PolicyBuilderError(ValueError):
    pass


@dataclass(frozen=True)
class ThresholdOverride:
    threshold: Decimal | None
    unit: str
    params: Mapping[str, Any] = field(default_factory=dict)


def build_policy_from_profile(
    *,
    profile: str,
    intake_session: Mapping[str, Any],
    account_scope: tuple[str, ...],
    threshold_overrides: Mapping[str, ThresholdOverride] | None = None,
) -> RiskPolicy:
    normalized_profile = profile.strip().casefold()
    overrides = threshold_overrides or {}
    if normalized_profile in STARTER_PROFILES:
        policy = _load_starter_policy(normalized_profile)
        rules = _apply_overrides(policy.rules, overrides)
    elif normalized_profile == "custom":
        if not overrides:
            raise PolicyBuilderError(
                "custom profile requires structured rule overrides"
            )
        rules = _rules_from_overrides(overrides)
    else:
        allowed = ", ".join((*STARTER_PROFILES, "custom"))
        raise PolicyBuilderError(f"profile must be one of: {allowed}")

    _validate_account_scope(account_scope)
    session = _session_from_intake(intake_session)
    return RiskPolicy(
        schema_version="1",
        account_scope=account_scope,
        timezone=str(intake_session["source_timezone"]),
        session=session,
        rules=rules,
    )


def policy_to_yaml(policy: RiskPolicy) -> str:
    return (
        yaml.safe_dump(
            policy.to_canonical_dict(),
            allow_unicode=False,
            sort_keys=True,
        )
        + "\n"
    )


def write_generated_policy(policy: RiskPolicy, output_dir: str | Path) -> Path:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_path = directory / "policy.yaml"
    output_path.write_text(policy_to_yaml(policy), encoding="utf-8")
    return output_path


def parse_threshold_overrides(values: tuple[str, ...]) -> dict[str, ThresholdOverride]:
    return dict(_parse_threshold_override(value) for value in values)


def _load_starter_policy(profile: str) -> RiskPolicy:
    return load_policy(STARTER_POLICY_DIR / f"starter_policy_{profile}.yaml")


def _apply_overrides(
    rules: tuple[PolicyRule, ...],
    overrides: Mapping[str, ThresholdOverride],
) -> tuple[PolicyRule, ...]:
    _validate_overrides(overrides)
    override_by_type = dict(overrides)
    updated: list[PolicyRule] = []
    for rule in rules:
        override = override_by_type.pop(rule.type, None)
        updated.append(_with_override(rule, override) if override else rule)
    updated.extend(
        _rule_from_override(rule_type, override)
        for rule_type, override in sorted(override_by_type.items())
    )
    return tuple(updated)


def _rules_from_overrides(
    overrides: Mapping[str, ThresholdOverride],
) -> tuple[PolicyRule, ...]:
    _validate_overrides(overrides)
    return tuple(
        _rule_from_override(rule_type, override)
        for rule_type, override in sorted(overrides.items())
    )


def _with_override(
    rule: PolicyRule,
    override: ThresholdOverride,
) -> PolicyRule:
    params = {**rule.params, **dict(override.params)}
    return PolicyRule(
        rule_id=rule.rule_id,
        type=rule.type,
        threshold=override.threshold,
        unit=override.unit,
        params=params,
    )


def _rule_from_override(
    rule_type: str,
    override: ThresholdOverride,
) -> PolicyRule:
    return PolicyRule(
        rule_id=f"generated_{rule_type}",
        type=cast(RuleType, rule_type),
        threshold=override.threshold,
        unit=override.unit,
        params=dict(override.params),
    )


def _validate_overrides(overrides: Mapping[str, ThresholdOverride]) -> None:
    catalog_units = {
        entry.rule_type: entry.threshold_unit for entry in list_rule_catalog()
    }
    for rule_type, override in overrides.items():
        if rule_type not in catalog_units:
            raise PolicyBuilderError(f"unsupported threshold override: {rule_type}")
        if override.unit != catalog_units[rule_type]:
            raise PolicyBuilderError(
                f"{rule_type} threshold unit must be {catalog_units[rule_type]}"
            )


def _validate_account_scope(account_scope: tuple[str, ...]) -> None:
    if not account_scope or any(not account.strip() for account in account_scope):
        raise PolicyBuilderError("account scope must include at least one account id")


def _session_from_intake(intake_session: Mapping[str, Any]) -> SessionDefinition:
    session = intake_session["session"]
    if not isinstance(session, Mapping):
        raise PolicyBuilderError("intake session must include a session mapping")
    return SessionDefinition(
        start=str(session["start"]),
        end=str(session["end"]),
    )


def _parse_threshold_override(value: str) -> tuple[str, ThresholdOverride]:
    rule_type, _, raw_setting = value.partition("=")
    threshold, _, unit = raw_setting.partition(":")
    if not rule_type or not threshold or not unit:
        raise PolicyBuilderError("threshold override must use rule_type=threshold:unit")
    try:
        parsed_threshold = Decimal(threshold.strip())
    except InvalidOperation as error:
        raise PolicyBuilderError("threshold must be a decimal value") from error
    return (rule_type.strip(), ThresholdOverride(parsed_threshold, unit.strip()))
