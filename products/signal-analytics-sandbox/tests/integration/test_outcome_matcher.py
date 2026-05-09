from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from decimal import Decimal
from io import BytesIO

import polars as pl

from signal_sandbox.ledger.record import Direction, SignalRecord
from signal_sandbox.outcomes.matcher import (
    Outcome,
    match_outcomes,
    outcomes_parquet_bytes,
)
from signal_sandbox.outcomes.rule_registry import RULE_REGISTRY_VERSION, RULES
from signal_sandbox.prices.base import make_price_snapshot

TEXT_SHA = "a" * 64


def make_signal(
    *,
    asset_symbol: str = "BTC",
    direction: Direction = Direction.LONG,
    entry: str | None = "100",
    stop: str | None = "90",
    target: str | None = "110",
    minute: int = 0,
    ambiguity_flags: list[str] | None = None,
) -> SignalRecord:
    return SignalRecord(
        source_id="pilot",
        capture_id=f"capture-{asset_symbol}-{minute}",
        evidence_url=f"https://t.me/example/{minute}",
        text_sha256=TEXT_SHA,
        capture_timestamp_utc=datetime(2026, 5, 7, 9, minute, tzinfo=UTC),
        extracted_timestamp_utc=datetime(2026, 5, 7, 10, minute, tzinfo=UTC),
        asset_symbol=asset_symbol,
        direction=direction,
        entry=Decimal(entry) if entry is not None else None,
        stop=Decimal(stop) if stop is not None else None,
        target=Decimal(target) if target is not None else None,
        ambiguity_flags=ambiguity_flags or [],
    )


def make_snapshot(rows: list[dict[str, object]]):
    return make_price_snapshot(
        provider_id="operator-file",
        provider_status="operator_supplied",
        as_of_utc=datetime(2026, 5, 7, 12, tzinfo=UTC),
        range_start_utc=datetime(2026, 5, 7, 10, tzinfo=UTC),
        range_end_utc=datetime(2026, 5, 7, 11, tzinfo=UTC),
        assets=["BTC"],
        rows=rows,
    )


def price_row(
    minute: int,
    *,
    high: str,
    low: str,
    close: str,
    asset: str = "BTC",
) -> dict[str, object]:
    return {
        "asset": asset,
        "timestamp_utc": datetime(2026, 5, 7, 10, minute, tzinfo=UTC),
        "open": "100",
        "high": high,
        "low": low,
        "close": close,
        "volume": "10",
    }


def test_byte_identical_re_run() -> None:
    snapshot = make_snapshot(
        [
            price_row(0, high="105", low="95", close="101"),
            price_row(1, high="111", low="98", close="110"),
        ]
    )
    records = [make_signal()]

    first = outcomes_parquet_bytes(match_outcomes(records, snapshot))
    second = outcomes_parquet_bytes(match_outcomes(records, snapshot))

    assert first == second
    assert hashlib.sha256(first).hexdigest() == hashlib.sha256(second).hexdigest()


def test_long_target_and_stop() -> None:
    target_snapshot = make_snapshot(
        [
            price_row(0, high="105", low="95", close="101"),
            price_row(1, high="111", low="98", close="110"),
        ]
    )
    stop_snapshot = make_snapshot(
        [
            price_row(0, high="105", low="95", close="101"),
            price_row(1, high="106", low="89", close="90"),
        ]
    )

    target = match_outcomes([make_signal()], target_snapshot)[0]
    stop = match_outcomes([make_signal()], stop_snapshot)[0]

    assert target.outcome == Outcome.TARGET_HIT
    assert target.return_pct == Decimal("10.000000")
    assert target.mae_pct == Decimal("-5.000000")
    assert target.mfe_pct == Decimal("11.000000")
    assert stop.outcome == Outcome.STOP_HIT
    assert stop.return_pct == Decimal("-10.000000")


def test_timeout_no_hit() -> None:
    snapshot = make_snapshot(
        [
            price_row(0, high="105", low="95", close="101"),
            price_row(1, high="106", low="96", close="104"),
        ]
    )

    outcome = match_outcomes([make_signal()], snapshot)[0]

    assert outcome.outcome == Outcome.TIMEOUT_NO_HIT
    assert outcome.return_pct == Decimal("4.000000")
    assert outcome.exit_timestamp == datetime(2026, 5, 7, 10, 1, tzinfo=UTC)


def test_short_metrics_are_directional() -> None:
    snapshot = make_snapshot(
        [
            price_row(0, high="105", low="95", close="101"),
            price_row(1, high="102", low="89", close="90"),
        ]
    )
    record = make_signal(
        direction=Direction.SHORT,
        entry="100",
        stop="110",
        target="90",
    )

    outcome = match_outcomes([record], snapshot)[0]

    assert outcome.outcome == Outcome.TARGET_HIT
    assert outcome.return_pct == Decimal("10.000000")
    assert outcome.mae_pct == Decimal("-5.000000")
    assert outcome.mfe_pct == Decimal("11.000000")


def test_excluded_ambiguous() -> None:
    snapshot = make_snapshot([price_row(0, high="111", low="95", close="110")])
    records = [
        make_signal(direction=Direction.FLAT),
        make_signal(direction=Direction.UNKNOWN, minute=1),
        make_signal(ambiguity_flags=["duplicate_dedup_key"], minute=2),
    ]

    outcomes = match_outcomes(records, snapshot)

    assert [outcome.outcome for outcome in outcomes] == [
        Outcome.EXCLUDED_AMBIGUOUS,
        Outcome.EXCLUDED_AMBIGUOUS,
        Outcome.EXCLUDED_AMBIGUOUS,
    ]
    assert all(outcome.return_pct is None for outcome in outcomes)


def test_excluded_no_price() -> None:
    snapshot = make_snapshot([price_row(0, high="111", low="95", close="110")])

    outcome = match_outcomes([make_signal(asset_symbol="ETH")], snapshot)[0]

    assert outcome.outcome == Outcome.EXCLUDED_NO_PRICE
    assert outcome.return_pct is None


def test_rule_id_cited() -> None:
    snapshot = make_snapshot([price_row(0, high="111", low="95", close="110")])
    outcomes = match_outcomes(
        [
            make_signal(),
            make_signal(direction=Direction.UNKNOWN, minute=1),
            make_signal(asset_symbol="ETH", minute=2),
        ],
        snapshot,
    )
    parquet_bytes = outcomes_parquet_bytes(outcomes)
    metadata_path = BytesIO(parquet_bytes)

    assert all(outcome.outcome_rule_id in RULES for outcome in outcomes)
    assert pl.read_parquet_metadata(metadata_path)["rule_registry_version"] == (
        RULE_REGISTRY_VERSION
    )


def test_rounding_determinism() -> None:
    snapshot = make_snapshot([price_row(0, high="100.0000015", low="100", close="100")])
    record = make_signal(entry="100", stop="90", target="100.0000015")

    outcome = match_outcomes([record], snapshot)[0]
    frame = pl.read_parquet(BytesIO(outcomes_parquet_bytes([outcome])))

    assert outcome.return_pct == Decimal("0.000002")
    assert frame["return_pct"].to_list() == [0.000002]
