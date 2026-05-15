from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from trader_risk_audit.policy.schema import SUPPORTED_RULE_TYPES, RuleType

STARTER_PROFILE_NAMES = ("soft", "medium", "hard")

_BASE_TRADE_FIELDS = ("timestamp", "symbol", "side", "quantity", "price")
_PNL_FIELDS = (*_BASE_TRADE_FIELDS, "fees")


@dataclass(frozen=True)
class RuleCatalogEntry:
    rule_type: RuleType
    required_source_fields: tuple[str, ...]
    threshold_unit: str
    safe_description: str
    starter_profiles: tuple[str, ...]
    required_profile_flags: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuleAvailability:
    rule_type: RuleType
    available: bool
    missing_requirements: tuple[str, ...]


RULE_CATALOG: tuple[RuleCatalogEntry, ...] = (
    RuleCatalogEntry(
        rule_type="max_daily_loss",
        required_source_fields=_PNL_FIELDS,
        threshold_unit="USD",
        safe_description=(
            "Flags trades after realized daily loss exceeds the approved audit "
            "threshold."
        ),
        starter_profiles=STARTER_PROFILE_NAMES,
        required_profile_flags=("pnl_available", "fee_available"),
    ),
    RuleCatalogEntry(
        rule_type="max_drawdown",
        required_source_fields=_PNL_FIELDS,
        threshold_unit="USD",
        safe_description=(
            "Flags trades after the reconstructed equity curve exceeds the "
            "approved drawdown threshold."
        ),
        starter_profiles=STARTER_PROFILE_NAMES,
        required_profile_flags=(
            "pnl_available",
            "fee_available",
            "account_balance_available",
        ),
    ),
    RuleCatalogEntry(
        rule_type="cooldown_after_loss",
        required_source_fields=_PNL_FIELDS,
        threshold_unit="minutes",
        safe_description=(
            "Flags trades opened inside an approved cooldown window after a "
            "realized loss event."
        ),
        starter_profiles=STARTER_PROFILE_NAMES,
        required_profile_flags=("pnl_available", "fee_available"),
    ),
    RuleCatalogEntry(
        rule_type="max_position_size",
        required_source_fields=_BASE_TRADE_FIELDS,
        threshold_unit="USD",
        safe_description=(
            "Flags rows where deterministic notional exposure is above the "
            "approved position-size threshold."
        ),
        starter_profiles=STARTER_PROFILE_NAMES,
    ),
    RuleCatalogEntry(
        rule_type="forbidden_assets",
        required_source_fields=("timestamp", "symbol", "side"),
        threshold_unit="symbol",
        safe_description=(
            "Flags source rows whose normalized symbol is on the approved "
            "forbidden-asset list."
        ),
        starter_profiles=STARTER_PROFILE_NAMES,
    ),
    RuleCatalogEntry(
        rule_type="max_leverage",
        required_source_fields=(*_BASE_TRADE_FIELDS, "leverage"),
        threshold_unit="ratio",
        safe_description=(
            "Requires explicit leverage data before any leverage threshold can "
            "be evaluated."
        ),
        starter_profiles=(),
        required_profile_flags=("leverage_available",),
    ),
)


def list_rule_catalog() -> tuple[RuleCatalogEntry, ...]:
    _assert_catalog_matches_schema()
    return RULE_CATALOG


def rule_availability(
    intake_profile: Any,
) -> tuple[RuleAvailability, ...]:
    profile = _profile_mapping(intake_profile)
    missing_required_fields = {
        str(field) for field in profile.get("missing_required_fields", ())
    }
    return tuple(
        RuleAvailability(
            rule_type=entry.rule_type,
            available=not (
                missing_requirements := _missing_requirements(
                    entry,
                    profile,
                    missing_required_fields,
                )
            ),
            missing_requirements=missing_requirements,
        )
        for entry in RULE_CATALOG
    )


def unavailable_rules(intake_profile: Any) -> tuple[RuleAvailability, ...]:
    return tuple(
        item for item in rule_availability(intake_profile) if not item.available
    )


def _missing_requirements(
    entry: RuleCatalogEntry,
    profile: Mapping[str, Any],
    missing_required_fields: set[str],
) -> tuple[str, ...]:
    missing = [
        field
        for field in entry.required_source_fields
        if field in missing_required_fields
    ]
    missing.extend(
        flag for flag in entry.required_profile_flags if not bool(profile.get(flag))
    )
    return tuple(dict.fromkeys(missing))


def _profile_mapping(intake_profile: Any) -> Mapping[str, Any]:
    if isinstance(intake_profile, Mapping):
        return intake_profile
    if hasattr(intake_profile, "to_dict"):
        payload = intake_profile.to_dict()
        if isinstance(payload, Mapping):
            return payload
    return {
        key: getattr(intake_profile, key)
        for key in (
            "missing_required_fields",
            "fee_available",
            "leverage_available",
            "pnl_available",
            "account_balance_available",
        )
        if hasattr(intake_profile, key)
    }


def _assert_catalog_matches_schema() -> None:
    catalog_rule_types = {entry.rule_type for entry in RULE_CATALOG}
    if catalog_rule_types != SUPPORTED_RULE_TYPES:
        missing = sorted(SUPPORTED_RULE_TYPES - catalog_rule_types)
        extra = sorted(catalog_rule_types - SUPPORTED_RULE_TYPES)
        raise RuntimeError(
            f"rule catalog mismatch: missing={missing!r}, extra={extra!r}"
        )
