from __future__ import annotations

import csv
from dataclasses import replace
from decimal import Decimal
from pathlib import Path

import pytest

from trader_risk_audit.evaluation.attribution import (
    AttributionReconciliationError,
    attribute_pnl,
    ensure_reconciled,
)
from trader_risk_audit.evaluation.violations import ViolationRecord
from trader_risk_audit.trades.schema import TradeRecord


def test_top_level_buckets_each_trade_once() -> None:
    trades = _load_trades()
    summary = attribute_pnl(trades, _overlapping_violations(trades))

    assert [row.bucket for row in summary.rows] == [
        "unclassified",
        "violating",
        "compliant",
        "unclassified",
    ]
    assert len({row.row_id for row in summary.rows}) == len(trades)
    assert summary.violating_pnl == Decimal("99")
    assert summary.compliant_pnl == Decimal("-1")
    assert summary.unclassified_pnl == Decimal("0")


def test_rule_overlap_reconciles_to_total_pnl() -> None:
    trades = _load_trades()
    summary = attribute_pnl(trades, _overlapping_violations(trades))

    assert summary.total_pnl == Decimal("98")
    assert summary.reconciliation_delta == Decimal("0")
    assert [(rule.rule_id, rule.pnl) for rule in summary.rules] == [
        ("rule_forbidden_assets", Decimal("99")),
        ("rule_max_position_size", Decimal("99")),
    ]


def test_nonzero_reconciliation_delta_blocks_report_generation() -> None:
    trades = _load_trades()
    summary = attribute_pnl(trades, _overlapping_violations(trades))
    broken = replace(summary, reconciliation_delta=Decimal("1"))

    with pytest.raises(AttributionReconciliationError):
        ensure_reconciled(broken)


def _load_trades() -> tuple[TradeRecord, ...]:
    fixture = Path("tests/fixtures/trades/attribution_overlap.csv")
    with fixture.open(newline="", encoding="utf-8") as trade_file:
        return tuple(
            TradeRecord.from_mapping(row) for row in csv.DictReader(trade_file)
        )


def _overlapping_violations(
    trades: tuple[TradeRecord, ...],
) -> tuple[ViolationRecord, ...]:
    violating_trade = trades[1]
    return (
        _violation("rule_forbidden_assets", "forbidden_asset", violating_trade),
        _violation("rule_max_position_size", "max_position_size", violating_trade),
    )


def _violation(rule_id: str, rule_type: str, trade: TradeRecord) -> ViolationRecord:
    return ViolationRecord(
        rule_id=rule_id,
        rule_type=rule_type,
        source_row_ids=(trade.row_id,),
        timestamp=trade.timestamp,
        evaluated_value=trade.symbol,
        threshold="test",
        severity="breach",
        message_code=f"{rule_type}_breach",
        symbol=trade.symbol,
    )
