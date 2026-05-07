from __future__ import annotations

import csv
from pathlib import Path

from trader_risk_audit.evaluation.attribution import (
    attribute_pnl,
    ensure_reconciled,
    serialize_attribution,
)
from trader_risk_audit.evaluation.violations import ViolationRecord
from trader_risk_audit.trades.schema import TradeRecord


def test_golden_attribution_fixture_matches_expected_json() -> None:
    trades = _load_trades()
    summary = ensure_reconciled(attribute_pnl(trades, _overlapping_violations(trades)))

    actual = serialize_attribution(summary)
    expected = (
        Path("tests/fixtures/expected/attribution_overlap_expected.json")
        .read_text(encoding="utf-8")
        .strip()
    )

    assert actual == expected


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
