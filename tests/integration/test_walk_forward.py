"""Integration tests for walk-forward harness boundaries."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import func, select
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session

from entropy.db.models import Base, Run
from entropy.models.registry import TrialSpec
from entropy.registry.write import register_trial
from entropy.walkforward import (
    FeatureAudit,
    IncompleteRunRecordError,
    LeakageBlockError,
    LeakageError,
    LeakageReport,
    OptimizationAudit,
    RegimeLabelAudit,
    UniverseSelectionAudit,
    run_checklist,
    run_walk_forward,
    split,
)


@dataclass(frozen=True)
class FeatureBar:
    timestamp: datetime
    close: float
    feature_computed_through: datetime | None = None


def make_bars(count: int, *, start: datetime | None = None) -> list[FeatureBar]:
    anchor = start or datetime(2026, 1, 1, tzinfo=timezone.utc)
    return [
        FeatureBar(
            timestamp=anchor + timedelta(hours=index),
            close=100.0 + index,
        )
        for index in range(count)
    ]


class RecordingStrategy:
    def __init__(self) -> None:
        self.is_timestamps: tuple[datetime, ...] = ()
        self.oos_timestamps: tuple[datetime, ...] = ()

    def run_is(self, window: tuple[FeatureBar, ...]) -> None:
        self.is_timestamps = tuple(bar.timestamp for bar in window)

    def run_oos(self, window: tuple[FeatureBar, ...]) -> None:
        self.oos_timestamps = tuple(bar.timestamp for bar in window)


def make_trial_spec(trial_id: str) -> TrialSpec:
    return TrialSpec(
        trial_id=trial_id,
        family_tag="mean-reversion",
        hypothesis="Mean reversion after large one-hour moves.",
        dataset_hash="dataset-sha",
        code_hash="code-sha",
        policy_hash="policy-sha",
        parameter_lock={"lookback": 24},
        registered_at=datetime(2026, 5, 3, 12, 0, tzinfo=timezone.utc),
    )


def prepare_run_tables(postgres_connection: Connection) -> None:
    Base.metadata.create_all(postgres_connection)


def count_runs(session: Session) -> int:
    return int(session.execute(select(func.count()).select_from(Run)).scalar_one())


def passing_leakage_check(
    is_window: tuple[FeatureBar, ...],
    oos_window: tuple[FeatureBar, ...],
) -> LeakageReport:
    return run_checklist(
        is_window,
        oos_window,
        feature_fn=lambda is_bars, oos_bars: FeatureAudit(
            computed_through=is_bars[-1].timestamp,
            description="features computed on IS only",
        ),
        regime_label_fn=lambda is_bars, oos_bars: RegimeLabelAudit(
            data_through=is_bars[-1].timestamp,
            description="regime labels computed on IS only",
        ),
        universe_selector=lambda is_bars, oos_bars: UniverseSelectionAudit(
            used_oos_returns=False,
            description="universe selected before OOS",
        ),
        optimizer=lambda is_bars, oos_bars: OptimizationAudit(
            refit_timestamps=(is_bars[-1].timestamp,),
            description="parameters fixed before OOS",
        ),
    )


def failing_leakage_check(
    is_window: tuple[FeatureBar, ...],
    oos_window: tuple[FeatureBar, ...],
) -> LeakageReport:
    return run_checklist(is_window, oos_window)


def test_splitter_is_window_ends_before_embargo() -> None:
    bars = make_bars(12)
    oos_start = bars[10].timestamp

    result = split(bars, oos_start, embargo_bars=5)

    assert result.bar_duration == timedelta(hours=1)
    assert result.is_cutoff == oos_start - 5 * result.bar_duration
    assert result.is_window[-1].timestamp < result.is_cutoff
    assert all(bar.timestamp < result.is_cutoff for bar in result.is_window)


def test_splitter_oos_window_starts_at_cutoff() -> None:
    bars = make_bars(12)
    oos_start = bars[10].timestamp

    result = split(bars, oos_start, embargo_bars=5)

    assert result.oos_window[0].timestamp == oos_start
    assert all(bar.timestamp >= oos_start for bar in result.oos_window)


def test_embargo_excludes_correct_bars() -> None:
    bars = make_bars(12)
    oos_start = bars[10].timestamp

    result = split(bars, oos_start, embargo_bars=5)

    assert [bar.timestamp for bar in result.embargo_window] == [bar.timestamp for bar in bars[5:10]]
    assert len(result.embargo_window) == 5


def test_no_future_leakage() -> None:
    bars = make_bars(12)
    oos_start = bars[10].timestamp
    leaking_bar = FeatureBar(
        timestamp=bars[2].timestamp,
        close=bars[2].close,
        feature_computed_through=bars[5].timestamp,
    )
    leaking_bars = [*bars[:2], leaking_bar, *bars[3:]]

    with pytest.raises(LeakageError, match="IS feature"):
        split(leaking_bars, oos_start, embargo_bars=5)


def test_splitter_zero_embargo() -> None:
    bars = make_bars(8)
    oos_start = bars[5].timestamp

    result = split(bars, oos_start, embargo_bars=0)

    assert result.is_window == tuple(bars[:5])
    assert result.embargo_window == ()
    assert result.is_window[-1].timestamp < oos_start
    assert result.oos_window == tuple(bars[5:])


def test_splitter_raises_for_empty_is_window() -> None:
    bars = make_bars(5)

    with pytest.raises(ValueError, match="IS window would be empty"):
        split(bars, bars[0].timestamp, embargo_bars=0)


def test_runner_produces_run_record_with_all_hashes() -> None:
    bars = make_bars(10)
    oos_start = bars[6].timestamp
    strategy = RecordingStrategy()

    record = run_walk_forward(
        "trial-runner-hashes",
        bars,
        strategy,
        oos_start=oos_start,
        leakage_check=passing_leakage_check,
        embargo_bars=1,
        dataset_hash="dataset-sha",
        code_hash="code-sha",
        policy_hash="policy-sha",
    )

    assert record.trial_id == "trial-runner-hashes"
    assert record.dataset_hash == "dataset-sha"
    assert record.code_hash == "code-sha"
    assert record.policy_hash == "policy-sha"
    assert record.simbroker_version == "simbroker-0.1.0"
    assert record.leakage_status.value == "PASS"
    assert strategy.is_timestamps == tuple(bar.timestamp for bar in bars[:5])
    assert strategy.oos_timestamps == tuple(bar.timestamp for bar in bars[6:])


def test_runner_blocks_oos_before_leakage_check() -> None:
    bars = make_bars(10)
    strategy = RecordingStrategy()

    with pytest.raises(LeakageBlockError, match="not been run"):
        run_walk_forward(
            "trial-runner-blocked",
            bars,
            strategy,
            oos_start=bars[6].timestamp,
            leakage_check=None,
            embargo_bars=1,
            dataset_hash="dataset-sha",
            code_hash="code-sha",
            policy_hash="policy-sha",
        )

    assert strategy.is_timestamps == tuple(bar.timestamp for bar in bars[:5])
    assert strategy.oos_timestamps == ()


def test_runner_blocks_oos_when_leakage_check_fails() -> None:
    bars = make_bars(10)
    strategy = RecordingStrategy()

    with pytest.raises(LeakageBlockError, match="did not pass"):
        run_walk_forward(
            "trial-runner-failed-leakage",
            bars,
            strategy,
            oos_start=bars[6].timestamp,
            leakage_check=failing_leakage_check,
            embargo_bars=1,
            dataset_hash="dataset-sha",
            code_hash="code-sha",
            policy_hash="policy-sha",
        )

    assert strategy.is_timestamps == tuple(bar.timestamp for bar in bars[:5])
    assert strategy.oos_timestamps == ()


def test_runner_persists_run_record_to_db(postgres_connection: Connection) -> None:
    prepare_run_tables(postgres_connection)
    bars = make_bars(10)
    strategy = RecordingStrategy()

    with Session(bind=postgres_connection) as session:
        register_trial(session, make_trial_spec("trial-runner-persist"))
        record = run_walk_forward(
            "trial-runner-persist",
            bars,
            strategy,
            oos_start=bars[6].timestamp,
            leakage_check=passing_leakage_check,
            session=session,
            embargo_bars=1,
            dataset_hash="dataset-sha",
            code_hash="code-sha",
            policy_hash="policy-sha",
            run_id="run-runner-persist",
        )

        persisted = session.get(Run, record.run_id)

    assert persisted is not None
    assert persisted.run_id == record.run_id
    assert persisted.trial_id == record.trial_id
    assert persisted.dataset_hash == record.dataset_hash
    assert persisted.code_hash == record.code_hash
    assert persisted.policy_hash == record.policy_hash
    assert persisted.simbroker_version == record.simbroker_version
    assert persisted.leakage_status == record.leakage_status.value


def test_runner_rejects_missing_code_hash(postgres_connection: Connection) -> None:
    prepare_run_tables(postgres_connection)
    bars = make_bars(10)
    strategy = RecordingStrategy()

    with Session(bind=postgres_connection) as session:
        before_count = count_runs(session)
        with pytest.raises(IncompleteRunRecordError, match="code_hash"):
            run_walk_forward(
                "trial-runner-missing-code",
                bars,
                strategy,
                oos_start=bars[6].timestamp,
                leakage_check=passing_leakage_check,
                session=session,
                embargo_bars=1,
                dataset_hash="dataset-sha",
                code_hash=None,
                policy_hash="policy-sha",
                run_id="run-missing-code",
            )

        assert count_runs(session) == before_count
    assert strategy.is_timestamps == ()
    assert strategy.oos_timestamps == ()
