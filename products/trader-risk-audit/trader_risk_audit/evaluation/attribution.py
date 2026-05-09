from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Literal

from trader_risk_audit.evaluation.violations import ViolationRecord
from trader_risk_audit.trades.schema import TradeRecord

PnlBucket = Literal["compliant", "violating", "unclassified"]


class AttributionReconciliationError(ValueError):
    def __init__(self, reconciliation_delta: Decimal) -> None:
        self.reconciliation_delta = reconciliation_delta
        super().__init__(
            f"non-zero attribution reconciliation delta: {reconciliation_delta}"
        )


@dataclass(frozen=True)
class RowAttribution:
    row_id: str
    bucket: PnlBucket
    pnl: Decimal
    rule_ids: tuple[str, ...]


@dataclass(frozen=True)
class RuleAttribution:
    rule_id: str
    pnl: Decimal
    source_row_ids: tuple[str, ...]


@dataclass(frozen=True)
class AttributionSummary:
    total_pnl: Decimal
    compliant_pnl: Decimal
    violating_pnl: Decimal
    unclassified_pnl: Decimal
    reconciliation_delta: Decimal
    rows: tuple[RowAttribution, ...]
    rules: tuple[RuleAttribution, ...]


def attribute_pnl(
    trades: tuple[TradeRecord, ...],
    violations: tuple[ViolationRecord, ...],
) -> AttributionSummary:
    row_pnl = _row_pnl(trades)
    violations_by_row = _violations_by_row(violations)
    rows = tuple(
        _row_attribution(trade, row_pnl[trade.row_id], violations_by_row[trade.row_id])
        for trade in sorted(
            trades, key=lambda item: (item.timestamp, item.source_row_number)
        )
    )
    compliant_pnl = sum(
        (row.pnl for row in rows if row.bucket == "compliant"), Decimal("0")
    )
    violating_pnl = sum(
        (row.pnl for row in rows if row.bucket == "violating"), Decimal("0")
    )
    unclassified_pnl = sum(
        (row.pnl for row in rows if row.bucket == "unclassified"), Decimal("0")
    )
    total_pnl = sum(row_pnl.values(), Decimal("0"))
    reconciliation_delta = total_pnl - compliant_pnl - violating_pnl - unclassified_pnl
    rules = _rule_attribution(row_pnl, violations)
    return AttributionSummary(
        total_pnl=total_pnl,
        compliant_pnl=compliant_pnl,
        violating_pnl=violating_pnl,
        unclassified_pnl=unclassified_pnl,
        reconciliation_delta=reconciliation_delta,
        rows=rows,
        rules=rules,
    )


def ensure_reconciled(summary: AttributionSummary) -> AttributionSummary:
    if summary.reconciliation_delta != 0:
        raise AttributionReconciliationError(summary.reconciliation_delta)
    return summary


def serialize_attribution(summary: AttributionSummary) -> str:
    return json.dumps(
        _summary_to_payload(summary), sort_keys=True, separators=(",", ":")
    )


def _row_attribution(
    trade: TradeRecord,
    pnl: Decimal,
    violations: tuple[ViolationRecord, ...],
) -> RowAttribution:
    rule_ids = tuple(sorted({violation.rule_id for violation in violations}))
    if rule_ids:
        bucket: PnlBucket = "violating"
    elif pnl == 0:
        bucket = "unclassified"
    else:
        bucket = "compliant"
    return RowAttribution(
        row_id=trade.row_id, bucket=bucket, pnl=pnl, rule_ids=rule_ids
    )


def _row_pnl(trades: tuple[TradeRecord, ...]) -> dict[str, Decimal]:
    row_pnl = {trade.row_id: -trade.fees for trade in trades}
    open_lots: defaultdict[tuple[str, str], list[tuple[str, str, Decimal, Decimal]]] = (
        defaultdict(list)
    )
    for trade in sorted(
        trades, key=lambda item: (item.timestamp, item.source_row_number)
    ):
        key = (trade.account_id, trade.symbol)
        quantity_to_match = trade.quantity
        lots = open_lots[key]
        while quantity_to_match > 0 and lots and lots[0][1] != trade.side:
            lot_row_id, lot_side, lot_quantity, lot_price = lots[0]
            matched_quantity = min(quantity_to_match, lot_quantity)
            row_pnl[trade.row_id] += _realized_pnl(
                lot_side,
                lot_price,
                trade.side,
                trade.price,
                matched_quantity,
            )
            lot_quantity -= matched_quantity
            quantity_to_match -= matched_quantity
            if lot_quantity == 0:
                lots.pop(0)
            else:
                lots[0] = (lot_row_id, lot_side, lot_quantity, lot_price)
        if quantity_to_match > 0:
            lots.append((trade.row_id, trade.side, quantity_to_match, trade.price))
    return row_pnl


def _realized_pnl(
    lot_side: str,
    lot_price: Decimal,
    closing_side: str,
    closing_price: Decimal,
    quantity: Decimal,
) -> Decimal:
    if lot_side == "buy" and closing_side == "sell":
        return (closing_price - lot_price) * quantity
    if lot_side == "sell" and closing_side == "buy":
        return (lot_price - closing_price) * quantity
    return Decimal("0")


def _violations_by_row(
    violations: tuple[ViolationRecord, ...],
) -> defaultdict[str, tuple[ViolationRecord, ...]]:
    grouped: defaultdict[str, list[ViolationRecord]] = defaultdict(list)
    for violation in violations:
        for row_id in violation.source_row_ids:
            grouped[row_id].append(violation)
    return defaultdict(
        tuple, {row_id: tuple(items) for row_id, items in grouped.items()}
    )


def _rule_attribution(
    row_pnl: dict[str, Decimal],
    violations: tuple[ViolationRecord, ...],
) -> tuple[RuleAttribution, ...]:
    rows_by_rule: defaultdict[str, set[str]] = defaultdict(set)
    for violation in violations:
        for row_id in violation.source_row_ids:
            rows_by_rule[violation.rule_id].add(row_id)
    return tuple(
        RuleAttribution(
            rule_id=rule_id,
            pnl=sum((row_pnl[row_id] for row_id in sorted(row_ids)), Decimal("0")),
            source_row_ids=tuple(sorted(row_ids)),
        )
        for rule_id, row_ids in sorted(rows_by_rule.items())
    )


def _summary_to_payload(summary: AttributionSummary) -> dict[str, Any]:
    return {
        "compliant_pnl": _decimal(summary.compliant_pnl),
        "reconciliation_delta": _decimal(summary.reconciliation_delta),
        "rows": [
            {
                "bucket": row.bucket,
                "pnl": _decimal(row.pnl),
                "row_id": row.row_id,
                "rule_ids": list(row.rule_ids),
            }
            for row in summary.rows
        ],
        "rules": [
            {
                "pnl": _decimal(rule.pnl),
                "rule_id": rule.rule_id,
                "source_row_ids": list(rule.source_row_ids),
            }
            for rule in summary.rules
        ],
        "total_pnl": _decimal(summary.total_pnl),
        "unclassified_pnl": _decimal(summary.unclassified_pnl),
        "violating_pnl": _decimal(summary.violating_pnl),
    }


def _decimal(value: Decimal) -> str:
    return format(value.normalize(), "f")
