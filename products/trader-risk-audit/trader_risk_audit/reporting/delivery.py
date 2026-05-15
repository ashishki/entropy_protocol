from __future__ import annotations

from pathlib import Path

from trader_risk_audit.reporting.claim_guard import (
    REQUIRED_DISCLAIMER,
    ensure_report_claims_valid,
)
from trader_risk_audit.reporting.model import ReportModel

DEFAULT_TELEGRAM_CHARACTER_LIMIT = 4096


def render_delivery_packet(
    *,
    model: ReportModel,
    report_text: str,
    report_path: str | Path,
    character_limit: int = DEFAULT_TELEGRAM_CHARACTER_LIMIT,
) -> str:
    ensure_report_claims_valid(report_text)
    repeated_patterns = _top_repeated_patterns(model.repeated_patterns.items)
    for visible_count in range(len(repeated_patterns), -1, -1):
        packet = _render_packet(
            model=model,
            report_path=str(report_path),
            repeated_patterns=repeated_patterns[:visible_count],
            omitted_repeated_count=len(repeated_patterns) - visible_count,
        )
        if len(packet) <= character_limit:
            return packet
    raise ValueError("delivery packet cannot fit within character limit")


def _render_packet(
    *,
    model: ReportModel,
    report_path: str,
    repeated_patterns: tuple[str, ...],
    omitted_repeated_count: int,
) -> str:
    lines = [
        "Trader Risk Audit Summary",
        f"Trades reviewed: {model.input_summary.trade_count}",
        f"Violations recorded: {len(model.violation_table)}",
        f"Violating P&L: {model.attribution_summary.violating_pnl}",
        "",
        "Top violation counts:",
        *_repeated_pattern_items(repeated_patterns, omitted_repeated_count),
    ]
    if omitted_repeated_count:
        lines.append(f"- {omitted_repeated_count} repeated pattern details omitted")
    lines.extend(
        [
            "",
            "Limitations:",
            *_limitation_items(model),
            "",
            f"Report: {report_path}",
            REQUIRED_DISCLAIMER,
        ]
    )
    return "\n".join(lines)


def _top_repeated_patterns(items: tuple[str, ...]) -> tuple[str, ...]:
    parsed = [_parse_repeated_pattern(item) for item in items]
    return tuple(
        f"{rule_id}: {count}"
        for rule_id, count in sorted(parsed, key=lambda item: (-item[1], item[0]))
    )


def _parse_repeated_pattern(item: str) -> tuple[str, int]:
    rule_id, _, raw_count = item.partition(":")
    try:
        count = int(raw_count.strip())
    except ValueError:
        count = 0
    return rule_id.strip(), count


def _limitation_items(model: ReportModel) -> tuple[str, ...]:
    if not model.limitations:
        return ("- None",)
    return tuple(
        f"- {item.rule_id}: {item.reason_code}"
        for item in sorted(model.limitations, key=lambda item: item.rule_id)
    )


def _bullet_items(items: tuple[str, ...]) -> tuple[str, ...]:
    if not items:
        return ("- None",)
    return tuple(f"- {item}" for item in items)


def _repeated_pattern_items(
    repeated_patterns: tuple[str, ...],
    omitted_repeated_count: int,
) -> tuple[str, ...]:
    if not repeated_patterns and omitted_repeated_count:
        return ()
    return _bullet_items(repeated_patterns)
