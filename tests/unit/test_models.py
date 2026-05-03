"""Unit tests for domain models."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from zoneinfo import ZoneInfo

import pytest
from pydantic import ValidationError

from entropy.models.market import Dataset, DatasetKey, OHLCVBar, Timeframe
from entropy.models.performance import DrawdownRecord, NetSharpe, PerformanceMetrics, PnLStreams
from entropy.models.registry import (
    FillLog,
    GovernanceEvent,
    GovernanceEventType,
    LeakageStatus,
    RunRecord,
    TrialSpec,
)


UTC_TS = datetime(2026, 5, 3, 12, 0, tzinfo=timezone.utc)


def make_bar(**overrides: object) -> OHLCVBar:
    data = {
        "timestamp": UTC_TS,
        "open": 100.0,
        "high": 105.0,
        "low": 95.0,
        "close": 101.0,
        "volume": 10.0,
    }
    data.update(overrides)
    return OHLCVBar(**data)


def test_ohlcv_bar_validates_price_sanity() -> None:
    invalid_cases = [
        {"close": 0.0},
        {"volume": -1.0},
        {"high": 99.0},
        {"low": 102.0},
    ]

    for overrides in invalid_cases:
        with pytest.raises(ValidationError):
            make_bar(**overrides)


def test_ohlcv_bar_requires_utc_timestamp() -> None:
    invalid_timestamps = [
        datetime(2026, 5, 3, 12, 0),
        datetime(2026, 5, 3, 12, 0, tzinfo=ZoneInfo("Asia/Tbilisi")),
    ]

    for timestamp in invalid_timestamps:
        with pytest.raises(ValidationError):
            make_bar(timestamp=timestamp)


def test_dataset_requires_nonempty_bars() -> None:
    bar = make_bar()

    dataset = Dataset(bars=[bar], provenance={"provider": "fixture"})

    assert dataset.bars == [bar]
    assert dataset.provenance == {"provider": "fixture"}

    with pytest.raises(ValidationError):
        Dataset(bars=[])


def test_dataset_key_validates_date_range() -> None:
    key = DatasetKey(
        symbol="BTC-USD",
        timeframe=Timeframe.H1,
        start=UTC_TS,
        end=datetime(2026, 5, 4, 12, 0, tzinfo=timezone.utc),
    )

    assert key.symbol == "BTC-USD"
    assert key.timeframe is Timeframe.H1

    with pytest.raises(ValidationError):
        DatasetKey(
            symbol="BTC-USD",
            timeframe=Timeframe.H1,
            start=UTC_TS,
            end=UTC_TS,
        )


def test_timeframe_enum_members() -> None:
    assert [timeframe.name for timeframe in Timeframe] == [
        "M1",
        "M5",
        "M15",
        "M30",
        "H1",
        "H4",
        "D1",
        "W1",
    ]
    assert all(isinstance(timeframe.value, str) for timeframe in Timeframe)


def make_trial_spec(**overrides: object) -> TrialSpec:
    data = {
        "trial_id": "trial-001",
        "family_tag": "mean-reversion",
        "hypothesis": "Mean reversion after large one-hour moves.",
        "dataset_hash": "dataset-sha",
        "code_hash": "code-sha",
        "policy_hash": "policy-sha",
        "parameter_lock": {"lookback": 24, "threshold": 2.0},
        "registered_at": UTC_TS,
    }
    data.update(overrides)
    return TrialSpec(**data)


def make_run_record(**overrides: object) -> RunRecord:
    data = {
        "trial_id": "trial-001",
        "run_id": "run-001",
        "dataset_hash": "dataset-sha",
        "code_hash": "code-sha",
        "policy_hash": "policy-sha",
        "simbroker_version": "simbroker-0.1.0",
        "is_start": datetime(2026, 5, 1, tzinfo=timezone.utc),
        "is_end": datetime(2026, 5, 2, tzinfo=timezone.utc),
        "oos_start": datetime(2026, 5, 3, tzinfo=timezone.utc),
        "oos_end": datetime(2026, 5, 4, tzinfo=timezone.utc),
        "embargo_bars": 1,
        "leakage_status": LeakageStatus.NOT_RUN,
    }
    data.update(overrides)
    return RunRecord(**data)


def make_fill_log(**overrides: object) -> FillLog:
    data = {
        "timestamp": UTC_TS,
        "symbol": "BTC-USD",
        "side": "BUY",
        "quantity": Decimal("1.5"),
        "fill_price": Decimal("100.25"),
        "commission": Decimal("0.10"),
        "slippage": Decimal("0.20"),
        "market_impact": Decimal("0.30"),
        "borrow_rate": Decimal("0"),
        "funding_rate": Decimal("0.01"),
        "total_cost": Decimal("0.61"),
    }
    data.update(overrides)
    return FillLog(**data)


def test_trial_spec_requires_all_hash_fields() -> None:
    required_fields = [
        "trial_id",
        "family_tag",
        "hypothesis",
        "dataset_hash",
        "code_hash",
        "policy_hash",
    ]

    for field_name in required_fields:
        with pytest.raises(ValidationError):
            make_trial_spec(**{field_name: ""})

    with pytest.raises(ValidationError):
        TrialSpec.model_validate(
            {
                "trial_id": "trial-001",
                "family_tag": "mean-reversion",
                "hypothesis": "Mean reversion after large one-hour moves.",
                "dataset_hash": "dataset-sha",
                "code_hash": "code-sha",
                "parameter_lock": {"lookback": 24},
                "registered_at": UTC_TS,
            }
        )


def test_trial_spec_requires_family_tag() -> None:
    for family_tag in (None, ""):
        with pytest.raises(ValidationError):
            make_trial_spec(family_tag=family_tag)


def test_run_record_requires_simbroker_version() -> None:
    for simbroker_version in (None, ""):
        with pytest.raises(ValidationError):
            make_run_record(simbroker_version=simbroker_version)


def test_fill_log_cost_fields_nonnegative() -> None:
    fill_log = make_fill_log(
        commission=0.1,
        slippage=0.2,
        market_impact=0.3,
        borrow_rate=0.0,
        funding_rate=0.01,
        total_cost=0.61,
    )

    assert fill_log.timestamp == UTC_TS
    assert fill_log.symbol == "BTC-USD"
    assert fill_log.side.value == "BUY"
    assert fill_log.quantity == Decimal("1.5")
    assert fill_log.fill_price == Decimal("100.25")
    assert fill_log.commission == Decimal("0.1")
    assert fill_log.slippage == Decimal("0.2")
    assert fill_log.market_impact == Decimal("0.3")
    assert fill_log.borrow_rate == Decimal("0.0")
    assert fill_log.funding_rate == Decimal("0.01")
    assert fill_log.total_cost == Decimal("0.61")

    for field_name in [
        "commission",
        "slippage",
        "market_impact",
        "borrow_rate",
        "funding_rate",
        "total_cost",
    ]:
        with pytest.raises(ValidationError):
            make_fill_log(**{field_name: Decimal("-0.01")})


def test_governance_event_validates_event_type() -> None:
    event = GovernanceEvent(
        event_type=GovernanceEventType.APPROVAL,
        timestamp=UTC_TS,
        trial_id="trial-001",
        actor="operator",
        reason="Approved for registry admission.",
        policy_hash="policy-sha",
    )

    assert event.event_type is GovernanceEventType.APPROVAL

    valid_event_values = [
        "APPROVAL",
        "REJECTION",
        "PHASE_GATE",
        "P1_TRIP",
        "P1_RESET",
        "P3_FIRE",
        "P3_CLEAR",
    ]
    assert [event_type.value for event_type in GovernanceEventType] == valid_event_values

    with pytest.raises(ValidationError):
        GovernanceEvent.model_validate(
            {
                "event_type": "UNKNOWN",
                "timestamp": UTC_TS,
                "trial_id": "trial-001",
                "actor": "operator",
                "reason": "Invalid event.",
                "policy_hash": "policy-sha",
            }
        )


def make_net_sharpe(**overrides: object) -> NetSharpe:
    data = {
        "value": 0.31,
        "confidence_interval_68": (0.22, 0.40),
        "sample_length": 252,
        "M_total": 8,
    }
    data.update(overrides)
    return NetSharpe(**data)


def make_drawdown_record(**overrides: object) -> DrawdownRecord:
    data = {
        "start_ts": datetime(2026, 5, 1, tzinfo=timezone.utc),
        "end_ts": datetime(2026, 5, 2, tzinfo=timezone.utc),
        "peak_value": Decimal("100000"),
        "trough_value": Decimal("92000"),
        "drawdown_pct": 0.08,
        "recovery_ts": datetime(2026, 5, 10, tzinfo=timezone.utc),
    }
    data.update(overrides)
    return DrawdownRecord(**data)


def test_pnl_streams_net_sharpe_excludes_stream_d() -> None:
    streams = PnLStreams(
        stream_a=(Decimal("1.25"), Decimal("0.50")),
        stream_b=(Decimal("-0.25"), Decimal("0.10")),
        stream_c=(Decimal("-0.10"), Decimal("-0.20")),
        stream_d=(Decimal("999.00"), Decimal("999.00")),
    )

    assert streams.net_sharpe_streams == (Decimal("0.90"), Decimal("0.40"))
    assert streams.net_sharpe_streams != (Decimal("999.90"), Decimal("999.40"))

    with pytest.raises(ValidationError):
        PnLStreams(
            stream_a=(Decimal("1.25"),),
            stream_b=(Decimal("-0.25"),),
            stream_c=(Decimal("-0.10"),),
            stream_d=(Decimal("999.00"), Decimal("999.00")),
        )


def test_net_sharpe_requires_canonical_method_id() -> None:
    net_sharpe = make_net_sharpe()

    assert net_sharpe.method_id == "CI-SR-ACF-v1"

    with pytest.raises(ValidationError):
        make_net_sharpe(method_id="bootstrap-v0")


def test_drawdown_record_validates_values() -> None:
    valid_drawdown = make_drawdown_record()

    assert valid_drawdown.drawdown_pct == 0.08

    invalid_cases = [
        {"drawdown_pct": -0.01},
        {"drawdown_pct": 1.01},
        {"trough_value": Decimal("100001")},
    ]

    for overrides in invalid_cases:
        with pytest.raises(ValidationError):
            make_drawdown_record(**overrides)


def test_performance_metrics_allows_stub_fields() -> None:
    metrics = PerformanceMetrics(
        net_sharpe=make_net_sharpe(),
        max_drawdown=make_drawdown_record(),
        calmar_ratio=1.7,
        n_eff=None,
        harvey_liu_deflated_sharpe=None,
        reason_code="PHASE0_FORMULA_STUB",
    )

    assert metrics.n_eff is None
    assert metrics.harvey_liu_deflated_sharpe is None
    assert metrics.reason_code == "PHASE0_FORMULA_STUB"

    with pytest.raises(ValidationError):
        PerformanceMetrics(
            net_sharpe=make_net_sharpe(),
            max_drawdown=make_drawdown_record(),
            calmar_ratio=1.7,
            n_eff=None,
            harvey_liu_deflated_sharpe=None,
        )
