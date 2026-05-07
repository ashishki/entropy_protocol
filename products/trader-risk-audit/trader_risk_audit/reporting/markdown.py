from __future__ import annotations

from trader_risk_audit.reporting.claim_guard import REQUIRED_DISCLAIMER
from trader_risk_audit.reporting.model import ReportModel

VIOLATION_COLUMNS = (
    "Rule ID",
    "Timestamp",
    "Source Row IDs",
    "Evaluated Value",
    "Threshold",
    "Severity",
    "P&L Impact",
)


def render_markdown_report(model: ReportModel) -> str:
    lines: list[str] = [
        "# Trader Risk Audit Report",
        "",
        REQUIRED_DISCLAIMER,
        "",
        "## Summary",
        "",
        f"- Trades reviewed: {model.input_summary.trade_count}",
        f"- Accounts reviewed: {model.input_summary.account_count}",
        f"- Source files: {_join_or_none(model.input_summary.source_files)}",
        "",
        "### Repeated Patterns",
        "",
        *_bullet_items(model.repeated_patterns.items),
        "",
        "### Worst Violation Days",
        "",
        *_bullet_items(model.worst_violation_days.items),
        "",
        "## Policy",
        "",
        f"- Schema version: {model.policy_summary.schema_version}",
        f"- Account scope: {_join_or_none(model.policy_summary.account_scope)}",
        f"- Rules reviewed: {model.policy_summary.rule_count}",
        f"- Rule IDs: {_join_or_none(model.policy_summary.rule_ids)}",
        "",
        "## Violations",
        "",
        *_violation_table(model),
        "",
        "## P&L Attribution",
        "",
        f"- Total P&L: {model.attribution_summary.total_pnl}",
        f"- Compliant P&L: {model.attribution_summary.compliant_pnl}",
        f"- Violating P&L: {model.attribution_summary.violating_pnl}",
        f"- Unclassified P&L: {model.attribution_summary.unclassified_pnl}",
        f"- Reconciliation delta: {model.attribution_summary.reconciliation_delta}",
        "",
        "## Limitations",
        "",
        *_limitations(model),
        "",
        "## Next Review",
        "",
        *_bullet_items(model.next_review_checklist.items),
        "",
    ]
    return "\n".join(lines)


def _violation_table(model: ReportModel) -> tuple[str, ...]:
    if not model.violation_table:
        return ("No deterministic violations were recorded.",)
    rows = [
        f"| {' | '.join(VIOLATION_COLUMNS)} |",
        f"| {' | '.join('---' for _ in VIOLATION_COLUMNS)} |",
    ]
    rows.extend(
        "| "
        + " | ".join(
            (
                _escape_cell(violation.rule_id),
                _escape_cell(violation.timestamp),
                _escape_cell(", ".join(violation.source_row_ids)),
                _escape_cell(violation.evaluated_value),
                _escape_cell(violation.threshold),
                _escape_cell(violation.severity),
                _escape_cell(violation.pnl_impact),
            )
        )
        + " |"
        for violation in model.violation_table
    )
    return tuple(rows)


def _limitations(model: ReportModel) -> tuple[str, ...]:
    if not model.limitations:
        return ("No unsupported-data limitations were recorded.",)
    return tuple(
        "- "
        f"{item.rule_id}: {item.reason_code}"
        f" ({_join_or_none(item.affected_source_fields)})"
        for item in model.limitations
    )


def _bullet_items(items: tuple[str, ...]) -> tuple[str, ...]:
    if not items:
        return ("- None",)
    return tuple(f"- {item}" for item in items)


def _join_or_none(values: tuple[str, ...]) -> str:
    if not values:
        return "none"
    return ", ".join(values)


def _escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")
