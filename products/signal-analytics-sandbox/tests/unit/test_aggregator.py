from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from signal_sandbox.outcomes.aggregate import (
    SummaryRecord,
    aggregate_outcomes,
    aggregate_outcomes_parquet_bytes,
)
from signal_sandbox.outcomes.matcher import (
    Outcome,
    OutcomeRecord,
    outcomes_parquet_bytes,
)
from signal_sandbox.outcomes.rule_registry import (
    EXCLUDED_AMBIGUOUS_RULE_ID,
    EXCLUDED_NO_PRICE_RULE_ID,
    LONG_TARGET_STOP_RULE_ID,
)

SNAPSHOT_SHA = "b" * 64


def outcome(
    dedup_key: str,
    outcome_value: Outcome,
    *,
    minute: int,
    return_pct: str | None = None,
) -> OutcomeRecord:
    rule_id = LONG_TARGET_STOP_RULE_ID
    if outcome_value == Outcome.EXCLUDED_AMBIGUOUS:
        rule_id = EXCLUDED_AMBIGUOUS_RULE_ID
    if outcome_value == Outcome.EXCLUDED_NO_PRICE:
        rule_id = EXCLUDED_NO_PRICE_RULE_ID
    return OutcomeRecord(
        dedup_key=dedup_key,
        source_id="pilot",
        asset_symbol="BTC",
        extracted_timestamp_utc=datetime(2026, 5, 7, 10, minute, tzinfo=UTC),
        outcome=outcome_value,
        return_pct=Decimal(return_pct) if return_pct is not None else None,
        outcome_rule_id=rule_id,
        snapshot_sha256=SNAPSHOT_SHA,
    )


def test_summary_byte_identical() -> None:
    outcomes = [
        outcome("b" * 64, Outcome.STOP_HIT, minute=1, return_pct="-5"),
        outcome("a" * 64, Outcome.TARGET_HIT, minute=0, return_pct="10"),
    ]

    first_parquet = outcomes_parquet_bytes(outcomes)
    second_parquet = outcomes_parquet_bytes(list(reversed(outcomes)))
    first = aggregate_outcomes_parquet_bytes(first_parquet).canonical_json_bytes()
    second = aggregate_outcomes_parquet_bytes(second_parquet).canonical_json_bytes()

    assert first == second


def test_win_rate_excludes_excluded() -> None:
    summary = aggregate_outcomes(
        [
            outcome("a" * 64, Outcome.TARGET_HIT, minute=0, return_pct="10"),
            outcome("b" * 64, Outcome.STOP_HIT, minute=1, return_pct="-5"),
            outcome("c" * 64, Outcome.EXCLUDED_AMBIGUOUS, minute=2),
            outcome("d" * 64, Outcome.EXCLUDED_NO_PRICE, minute=3),
        ]
    )

    assert summary.total_signals == 4
    assert summary.evaluated_signals == 2
    assert summary.excluded_ambiguous == 1
    assert summary.excluded_no_price == 1
    assert summary.historical_win_rate == Decimal("0.500000")


def test_no_forward_looking_field_names() -> None:
    forbidden_fragments = {"expected", "predicted", "forecast", "future"}

    field_names = set(SummaryRecord.model_fields)

    assert not {
        field
        for field in field_names
        for fragment in forbidden_fragments
        if fragment in field
    }
    assert all(
        field.startswith("historical_")
        for field in field_names
        if field
        not in {
            "total_signals",
            "evaluated_signals",
            "excluded_ambiguous",
            "excluded_no_price",
        }
    )


def test_drawdown_deterministic() -> None:
    summary = aggregate_outcomes(
        [
            outcome("c" * 64, Outcome.TARGET_HIT, minute=2, return_pct="2"),
            outcome("a" * 64, Outcome.TARGET_HIT, minute=0, return_pct="10"),
            outcome("b" * 64, Outcome.STOP_HIT, minute=1, return_pct="-15"),
        ]
    )

    assert summary.historical_max_drawdown_pct == Decimal("-15.000000")
    assert summary.historical_mean_return_pct == Decimal("-1.000000")
    assert summary.historical_median_return_pct == Decimal("2.000000")
