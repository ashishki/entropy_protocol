"""Unit tests for Trial Registry write path constraints."""

from __future__ import annotations

import ast
from datetime import datetime, timezone
from types import SimpleNamespace
from pathlib import Path
from typing import Any

import pytest

from entropy.models.registry import RegistryEntry, TrialSpec
from entropy.registry.gate import ReadinessStatus, TrialNotFoundError, check
from entropy.registry.read import (
    count_trials_in_family,
    get_by_family,
    get_by_status,
    get_by_trial_id,
    read_functions_issue_no_writes,
)
from entropy.registry.write import register_trial

PROJECT_ROOT = Path(__file__).resolve().parents[2]
WRITE_PATH = PROJECT_ROOT / "entropy" / "registry" / "write.py"


class EmptyResult:
    """Mock SQLAlchemy result with no duplicate row."""

    def scalar_one_or_none(self) -> None:
        return None


class GuardedSession:
    """Mock session that raises if write-path code tries UPDATE or DELETE helpers."""

    def __init__(self) -> None:
        self.added: list[Any] = []
        self.flushed = False

    def execute(self, statement: Any) -> EmptyResult:
        statement_text = str(statement).upper()
        if "UPDATE" in statement_text or "DELETE" in statement_text:
            raise AssertionError("write path attempted UPDATE or DELETE")
        return EmptyResult()

    def add(self, instance: Any) -> None:
        self.added.append(instance)

    def flush(self) -> None:
        self.flushed = True

    def update(self, *_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("write path attempted UPDATE")

    def delete(self, *_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("write path attempted DELETE")


class ScalarResult:
    """Mock scalar iterable result."""

    def __init__(self, rows: list[Any]) -> None:
        self.rows = rows

    def __iter__(self):
        return iter(self.rows)


class ExecuteResult:
    """Mock SQLAlchemy execute result."""

    def __init__(self, row: Any = None, rows: list[Any] | None = None, scalar: Any = None) -> None:
        self.row = row
        self.rows = rows or []
        self.scalar = scalar

    def scalar_one_or_none(self) -> Any:
        return self.row

    def scalars(self) -> ScalarResult:
        return ScalarResult(self.rows)

    def scalar_one(self) -> Any:
        return self.scalar


class QueueReadSession:
    """Mock read session with queued execute results and guarded write methods."""

    def __init__(self, results: list[ExecuteResult]) -> None:
        self.results = results

    def execute(self, _statement: Any) -> ExecuteResult:
        return self.results.pop(0)

    def add(self, *_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("read path attempted INSERT")

    def flush(self) -> None:
        raise AssertionError("read path attempted flush")

    def update(self, *_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("read path attempted UPDATE")

    def delete(self, *_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("read path attempted DELETE")


def make_trial_spec() -> TrialSpec:
    return TrialSpec(
        trial_id="trial-001",
        family_tag="mean-reversion",
        hypothesis="Mean reversion after large one-hour moves.",
        dataset_hash="dataset-sha",
        code_hash="code-sha",
        policy_hash="policy-sha",
        parameter_lock={"lookback": 24},
        registered_at=datetime(2026, 5, 3, 12, 0, tzinfo=timezone.utc),
    )


def make_registry_row(**overrides: Any) -> SimpleNamespace:
    data = make_trial_spec().model_dump()
    data["status"] = "PENDING"
    data.update(overrides)
    return SimpleNamespace(**data)


class InMemoryRegistryReader:
    """Read-only registry reader for readiness gate tests."""

    def __init__(
        self, entries: dict[str, RegistryEntry], family_counts: dict[str, int] | None = None
    ):
        self.entries = entries
        self.family_counts = family_counts or {}

    def get_by_trial_id(self, trial_id: str) -> RegistryEntry | None:
        return self.entries.get(trial_id)

    def count_trials_in_family(self, family_tag: str) -> int:
        return self.family_counts.get(family_tag, 1)


def test_write_path_uses_parameterized_sql() -> None:
    tree = ast.parse(WRITE_PATH.read_text(encoding="utf-8"))
    joined_strings = [node for node in ast.walk(tree) if isinstance(node, ast.JoinedStr)]
    string_literals = [
        node.value.upper()
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    ]

    assert joined_strings == []
    assert not any("UPDATE " in value or "DELETE " in value for value in string_literals)


def test_write_path_issues_no_update_or_delete() -> None:
    session = GuardedSession()

    trial_id = register_trial(session, make_trial_spec())  # type: ignore[arg-type]

    assert trial_id == "trial-001"
    assert len(session.added) == 1
    assert session.flushed is True


def test_gate_returns_ready_for_complete_trial() -> None:
    registry = InMemoryRegistryReader(
        {"trial-001": RegistryEntry(trial=make_trial_spec())},
        {"mean-reversion": 1},
    )

    result = check(registry, "trial-001")

    assert result.status is ReadinessStatus.READY
    assert result.failures == ()


def test_gate_lists_missing_dataset_hash() -> None:
    trial_data = make_trial_spec().model_dump()
    trial_data["dataset_hash"] = ""
    trial = TrialSpec.model_construct(**trial_data)
    registry = InMemoryRegistryReader({"trial-001": RegistryEntry(trial=trial)})

    result = check(registry, "trial-001")

    assert result.status is ReadinessStatus.NOT_READY
    assert result.failures == ("missing_dataset_hash",)


def test_gate_lists_missing_family_tag() -> None:
    trial_data = make_trial_spec().model_dump()
    trial_data["family_tag"] = ""
    trial = TrialSpec.model_construct(**trial_data)
    registry = InMemoryRegistryReader({"trial-001": RegistryEntry(trial=trial)}, {"": 1})

    result = check(registry, "trial-001")

    assert result.status is ReadinessStatus.NOT_READY
    assert result.failures == ("missing_family_tag",)


def test_gate_detects_duplicate_trial_id() -> None:
    registry = InMemoryRegistryReader(
        {"trial-001": RegistryEntry(trial=make_trial_spec())},
        {"mean-reversion": 2},
    )

    result = check(registry, "trial-001")

    assert result.status is ReadinessStatus.NOT_READY
    assert result.failures == ("duplicate_trial_id",)


def test_gate_raises_for_unknown_trial_id() -> None:
    registry = InMemoryRegistryReader({})

    with pytest.raises(TrialNotFoundError):
        check(registry, "unknown")


def test_read_by_trial_id_found_and_not_found() -> None:
    found_session = QueueReadSession([ExecuteResult(row=make_registry_row())])

    entry = get_by_trial_id(found_session, "trial-001")  # type: ignore[arg-type]

    assert entry.trial.trial_id == "trial-001"
    assert entry.status.value == "PENDING"

    missing_session = QueueReadSession([ExecuteResult(row=None)])
    with pytest.raises(TrialNotFoundError):
        get_by_trial_id(missing_session, "missing")  # type: ignore[arg-type]


def test_read_by_family_returns_correct_list() -> None:
    session = QueueReadSession(
        [
            ExecuteResult(
                rows=[
                    make_registry_row(trial_id="trial-001"),
                    make_registry_row(trial_id="trial-002"),
                ]
            )
        ]
    )

    entries = get_by_family(session, "mean-reversion")  # type: ignore[arg-type]

    assert [entry.trial.trial_id for entry in entries] == ["trial-001", "trial-002"]

    empty_session = QueueReadSession([ExecuteResult(rows=[])])
    assert get_by_family(empty_session, "unknown") == []  # type: ignore[arg-type]


def test_read_by_status_filters_correctly() -> None:
    pending_session = QueueReadSession([ExecuteResult(rows=[make_registry_row(status="PENDING")])])
    ready_session = QueueReadSession([ExecuteResult(rows=[make_registry_row(status="READY")])])

    assert [entry.status.value for entry in get_by_status(pending_session, "PENDING")] == [
        "PENDING"
    ]  # type: ignore[arg-type]
    assert [entry.status.value for entry in get_by_status(ready_session, "READY")] == ["READY"]  # type: ignore[arg-type]


def test_count_trials_in_family_includes_all_statuses() -> None:
    session = QueueReadSession([ExecuteResult(scalar=3)])

    assert count_trials_in_family(session, "mean-reversion") == 3  # type: ignore[arg-type]


def test_read_path_issues_no_writes() -> None:
    session = QueueReadSession(
        [
            ExecuteResult(rows=[]),
            ExecuteResult(rows=[]),
            ExecuteResult(scalar=0),
        ]
    )

    read_functions_issue_no_writes(session)
