"""Experiment Readiness Gate."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from entropy.models.registry import RegistryEntry


class ReadinessStatus(str, Enum):
    """Readiness gate outcomes."""

    READY = "READY"
    NOT_READY = "NOT_READY"


@dataclass(frozen=True)
class ReadinessResult:
    """Structured readiness gate result."""

    status: ReadinessStatus
    failures: tuple[str, ...] = ()


class TrialNotFoundError(Exception):
    """Raised when a requested trial does not exist."""


class RegistryReader(Protocol):
    """Read-only dependency needed by the readiness gate."""

    def get_by_trial_id(self, trial_id: str) -> RegistryEntry | None:
        """Return a registry entry by trial_id."""
        ...

    def count_trials_in_family(self, family_tag: str) -> int:
        """Return count of trials in a family."""
        ...


def check(registry: RegistryReader, trial_id: str) -> ReadinessResult:
    """Return READY only when a trial has all required registry fields."""
    entry = registry.get_by_trial_id(trial_id)
    if entry is None:
        raise TrialNotFoundError("Trial not found: " + trial_id)

    trial = entry.trial
    failures: list[str] = []
    if not trial.family_tag.strip():
        failures.append("missing_family_tag")
    if not trial.dataset_hash.strip():
        failures.append("missing_dataset_hash")
    if not trial.code_hash.strip():
        failures.append("missing_code_hash")
    if not trial.policy_hash.strip():
        failures.append("missing_policy_hash")
    if registry.count_trials_in_family(trial.family_tag) > 1:
        failures.append("duplicate_trial_id")

    if failures:
        return ReadinessResult(status=ReadinessStatus.NOT_READY, failures=tuple(failures))
    return ReadinessResult(status=ReadinessStatus.READY)
