"""Walk-forward runner orchestration."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from datetime import datetime
from typing import Protocol

from sqlalchemy.orm import Session

from entropy.db.models import Run
from entropy.hashing import compute_run_hash
from entropy.models.market import Dataset
from entropy.models.registry import LeakageStatus, RunRecord
from entropy.walkforward.leakage import CheckStatus, LeakageReport
from entropy.walkforward.splitter import BarLike, split

SIMBROKER_VERSION = "simbroker-0.1.0"


class WalkForwardRunnerError(Exception):
    """Base error for walk-forward runner failures."""


class LeakageBlockError(WalkForwardRunnerError):
    """Raised when OOS evaluation is attempted before a passing leakage check."""


class IncompleteRunRecordError(WalkForwardRunnerError):
    """Raised before DB writes when run reproducibility metadata is incomplete."""


class WalkForwardStrategy(Protocol):
    """Strategy boundary used by the runner."""

    def run_is(self, window: Sequence[BarLike]) -> object:
        """Run IS computation on the in-sample window only."""

    def run_oos(self, window: Sequence[BarLike]) -> object:
        """Run OOS evaluation on the out-of-sample window only."""


LeakageCheck = Callable[[Sequence[BarLike], Sequence[BarLike]], LeakageReport]


def run_walk_forward(
    trial_id: str,
    dataset: Dataset | Sequence[BarLike],
    strategy: WalkForwardStrategy,
    *,
    oos_start: datetime,
    leakage_check: LeakageCheck | None,
    session: Session | None = None,
    embargo_bars: int = 0,
    dataset_hash: str | None = None,
    code_hash: str | None = None,
    policy_hash: str | None = None,
    simbroker_version: str | None = SIMBROKER_VERSION,
    run_id: str | None = None,
) -> RunRecord:
    """Run one strict IS/OOS evaluation and optionally persist its RunRecord."""

    bars = _bars_from_dataset(dataset)
    dataset_hash = dataset_hash or _metadata_value(dataset, "dataset_hash")
    code_hash = code_hash or _metadata_value(dataset, "code_hash")
    policy_hash = policy_hash or _metadata_value(dataset, "policy_hash")
    (
        resolved_trial_id,
        resolved_dataset_hash,
        resolved_code_hash,
        resolved_policy_hash,
        resolved_simbroker_version,
    ) = _require_reproducibility_fields(
        trial_id=trial_id,
        dataset_hash=dataset_hash,
        code_hash=code_hash,
        policy_hash=policy_hash,
        simbroker_version=simbroker_version,
    )

    split_result = split(bars, oos_start, embargo_bars=embargo_bars)
    strategy.run_is(split_result.is_window)

    if leakage_check is None:
        raise LeakageBlockError("Leakage checklist has not been run")
    leakage_report = leakage_check(split_result.is_window, split_result.oos_window)
    if leakage_report.overall_status is not CheckStatus.PASS:
        raise LeakageBlockError("Leakage checklist did not pass")

    strategy.run_oos(split_result.oos_window)

    resolved_run_id = run_id or compute_run_hash(
        dataset_hash=resolved_dataset_hash,
        code_hash=resolved_code_hash,
        policy_hash=resolved_policy_hash,
    )
    run_record = RunRecord(
        trial_id=resolved_trial_id,
        run_id=resolved_run_id,
        dataset_hash=resolved_dataset_hash,
        code_hash=resolved_code_hash,
        policy_hash=resolved_policy_hash,
        simbroker_version=resolved_simbroker_version,
        is_start=split_result.is_window[0].timestamp,
        is_end=split_result.is_window[-1].timestamp,
        oos_start=split_result.oos_window[0].timestamp,
        oos_end=split_result.oos_window[-1].timestamp,
        embargo_bars=embargo_bars,
        leakage_status=LeakageStatus.PASS,
    )
    if session is not None:
        _persist_run_record(session, run_record)
    return run_record


def _bars_from_dataset(dataset: Dataset | Sequence[BarLike]) -> tuple[BarLike, ...]:
    if isinstance(dataset, Dataset):
        return tuple(dataset.bars)
    return tuple(dataset)


def _metadata_value(dataset: Dataset | Sequence[BarLike], key: str) -> str | None:
    if not isinstance(dataset, Dataset):
        return None
    value = dataset.provenance.get(key)
    if value is None:
        return None
    return str(value)


def _require_reproducibility_fields(
    *,
    trial_id: str,
    dataset_hash: str | None,
    code_hash: str | None,
    policy_hash: str | None,
    simbroker_version: str | None,
) -> tuple[str, str, str, str, str]:
    fields = {
        "trial_id": trial_id,
        "dataset_hash": dataset_hash,
        "code_hash": code_hash,
        "policy_hash": policy_hash,
        "simbroker_version": simbroker_version,
    }
    missing = [
        field_name
        for field_name, value in fields.items()
        if value is None or not str(value).strip()
    ]
    if missing:
        raise IncompleteRunRecordError("Missing reproducibility fields: " + ", ".join(missing))
    return (
        trial_id,
        str(dataset_hash),
        str(code_hash),
        str(policy_hash),
        str(simbroker_version),
    )


def _persist_run_record(session: Session, run_record: RunRecord) -> None:
    session.add(
        Run(
            run_id=run_record.run_id,
            trial_id=run_record.trial_id,
            dataset_hash=run_record.dataset_hash,
            code_hash=run_record.code_hash,
            policy_hash=run_record.policy_hash,
            simbroker_version=run_record.simbroker_version,
            is_start=run_record.is_start,
            is_end=run_record.is_end,
            oos_start=run_record.oos_start,
            oos_end=run_record.oos_end,
            embargo_bars=run_record.embargo_bars,
            leakage_status=run_record.leakage_status.value,
        )
    )
    session.flush()
