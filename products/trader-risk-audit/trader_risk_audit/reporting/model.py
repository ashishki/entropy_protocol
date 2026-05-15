from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from trader_risk_audit.evaluation.attribution import AttributionSummary
from trader_risk_audit.evaluation.violations import (
    UnsupportedDataWarning,
    ViolationRecord,
)
from trader_risk_audit.policy.schema import RiskPolicy
from trader_risk_audit.trades.schema import TradeRecord


@dataclass(frozen=True)
class Section:
    title: str
    items: tuple[str, ...]


@dataclass(frozen=True)
class InputSummarySection:
    title: str
    trade_count: int
    account_count: int
    source_files: tuple[str, ...]


@dataclass(frozen=True)
class PolicySummarySection:
    title: str
    schema_version: str
    account_scope: tuple[str, ...]
    rule_count: int
    rule_ids: tuple[str, ...]


@dataclass(frozen=True)
class ExecutiveSummarySection:
    title: str
    rule_count: int
    violation_count: int
    affected_pnl: str
    selected_policy_profile: str


@dataclass(frozen=True)
class ReportViolationRow:
    rule_id: str
    timestamp: str
    source_row_ids: tuple[str, ...]
    evaluated_value: str
    threshold: str
    severity: str
    pnl_impact: str


@dataclass(frozen=True)
class AttributionReportSection:
    title: str
    total_pnl: str
    compliant_pnl: str
    violating_pnl: str
    unclassified_pnl: str
    reconciliation_delta: str


@dataclass(frozen=True)
class LimitationItem:
    rule_id: str
    reason_code: str
    affected_source_fields: tuple[str, ...]


@dataclass(frozen=True)
class ReportModel:
    executive_summary: ExecutiveSummarySection
    input_summary: InputSummarySection
    policy_summary: PolicySummarySection
    violation_table: tuple[ReportViolationRow, ...]
    repeated_patterns: Section
    worst_violation_days: Section
    attribution_summary: AttributionReportSection
    limitations: tuple[LimitationItem, ...]
    next_review_checklist: Section

    @property
    def section_titles(self) -> tuple[str, ...]:
        return (
            self.executive_summary.title,
            self.input_summary.title,
            self.policy_summary.title,
            "Violations",
            self.repeated_patterns.title,
            self.worst_violation_days.title,
            self.attribution_summary.title,
            "Limitations",
            self.next_review_checklist.title,
        )


def build_report_model(
    *,
    trades: tuple[TradeRecord, ...],
    policy: RiskPolicy,
    violations: tuple[ViolationRecord, ...],
    warnings: tuple[UnsupportedDataWarning, ...],
    attribution: AttributionSummary,
) -> ReportModel:
    pnl_by_row = {row.row_id: row.pnl for row in attribution.rows}
    return ReportModel(
        executive_summary=_executive_summary(policy, violations, attribution),
        input_summary=_input_summary(trades),
        policy_summary=_policy_summary(policy),
        violation_table=_violation_rows(violations, pnl_by_row),
        repeated_patterns=_repeated_patterns(violations),
        worst_violation_days=_worst_violation_days(violations),
        attribution_summary=_attribution_summary(attribution),
        limitations=_limitations(warnings),
        next_review_checklist=Section(
            title="Next Review",
            items=(
                "Review any unresolved unsupported-data limitations.",
                "Confirm policy thresholds before report delivery.",
                "Re-run the audit after rule or export changes.",
            ),
        ),
    )


def _executive_summary(
    policy: RiskPolicy,
    violations: tuple[ViolationRecord, ...],
    attribution: AttributionSummary,
) -> ExecutiveSummarySection:
    return ExecutiveSummarySection(
        title="Executive Summary",
        rule_count=len(policy.rules),
        violation_count=len(violations),
        affected_pnl=_stringify(attribution.violating_pnl),
        selected_policy_profile=_selected_policy_profile(policy),
    )


def _input_summary(trades: tuple[TradeRecord, ...]) -> InputSummarySection:
    return InputSummarySection(
        title="Input Summary",
        trade_count=len(trades),
        account_count=len({trade.account_id for trade in trades}),
        source_files=tuple(sorted({trade.source_file for trade in trades})),
    )


def _policy_summary(policy: RiskPolicy) -> PolicySummarySection:
    return PolicySummarySection(
        title="Policy Summary",
        schema_version=policy.schema_version,
        account_scope=policy.account_scope,
        rule_count=len(policy.rules),
        rule_ids=tuple(rule.rule_id for rule in policy.rules),
    )


def _selected_policy_profile(policy: RiskPolicy) -> str:
    profiles = {
        str(profile).strip()
        for rule in policy.rules
        if (profile := rule.params.get("starter_profile")) is not None
        and str(profile).strip()
    }
    if len(profiles) == 1:
        return profiles.pop()
    if len(profiles) > 1:
        return "mixed"
    return "custom/unspecified"


def _violation_rows(
    violations: tuple[ViolationRecord, ...],
    pnl_by_row: dict[str, Decimal],
) -> tuple[ReportViolationRow, ...]:
    return tuple(
        ReportViolationRow(
            rule_id=violation.rule_id,
            timestamp=violation.timestamp.isoformat(),
            source_row_ids=violation.source_row_ids,
            evaluated_value=_stringify(violation.evaluated_value),
            threshold=_stringify(violation.threshold),
            severity=violation.severity,
            pnl_impact=_stringify(
                sum(
                    (
                        pnl_by_row.get(row_id, Decimal("0"))
                        for row_id in violation.source_row_ids
                    ),
                    Decimal("0"),
                )
            ),
        )
        for violation in sorted(
            violations,
            key=lambda item: (item.timestamp, item.rule_id, item.source_row_ids),
        )
    )


def _repeated_patterns(violations: tuple[ViolationRecord, ...]) -> Section:
    counts = Counter(violation.rule_id for violation in violations)
    items = tuple(f"{rule_id}: {count}" for rule_id, count in sorted(counts.items()))
    return Section(title="Repeated Patterns", items=items)


def _worst_violation_days(violations: tuple[ViolationRecord, ...]) -> Section:
    by_day: defaultdict[str, int] = defaultdict(int)
    for violation in violations:
        by_day[violation.timestamp.date().isoformat()] += 1
    items = tuple(f"{day}: {count}" for day, count in sorted(by_day.items()))
    return Section(title="Worst Violation Days", items=items)


def _attribution_summary(attribution: AttributionSummary) -> AttributionReportSection:
    return AttributionReportSection(
        title="P&L Attribution",
        total_pnl=_stringify(attribution.total_pnl),
        compliant_pnl=_stringify(attribution.compliant_pnl),
        violating_pnl=_stringify(attribution.violating_pnl),
        unclassified_pnl=_stringify(attribution.unclassified_pnl),
        reconciliation_delta=_stringify(attribution.reconciliation_delta),
    )


def _limitations(
    warnings: tuple[UnsupportedDataWarning, ...],
) -> tuple[LimitationItem, ...]:
    return tuple(
        LimitationItem(
            rule_id=warning.rule_id,
            reason_code=warning.message_code,
            affected_source_fields=warning.missing_fields,
        )
        for warning in sorted(
            warnings, key=lambda item: (item.rule_id, item.message_code)
        )
    )


def _stringify(value: Any) -> str:
    if isinstance(value, Decimal):
        return format(value.normalize(), "f")
    return str(value)
