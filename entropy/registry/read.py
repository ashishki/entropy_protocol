"""Trial Registry read path."""

from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from entropy.db.models import TrialRegistry
from entropy.models.registry import RegistryEntry, RegistryStatus, TrialSpec
from entropy.registry.gate import TrialNotFoundError


def _entry_from_row(row: TrialRegistry) -> RegistryEntry:
    """Convert a registry ORM row into a domain RegistryEntry."""
    return RegistryEntry(
        trial=TrialSpec(
            trial_id=row.trial_id,
            family_tag=row.family_tag,
            hypothesis=row.hypothesis,
            dataset_hash=row.dataset_hash,
            code_hash=row.code_hash,
            policy_hash=row.policy_hash,
            parameter_lock=row.parameter_lock,
            registered_at=row.registered_at,
        ),
        status=RegistryStatus(row.status),
    )


def get_by_trial_id(session: Session, trial_id: str) -> RegistryEntry:
    """Return one registry entry by trial_id."""
    row = session.execute(
        select(TrialRegistry).where(TrialRegistry.trial_id == trial_id)
    ).scalar_one_or_none()
    if row is None:
        raise TrialNotFoundError("Trial not found: " + trial_id)
    return _entry_from_row(row)


def get_by_family(session: Session, family_tag: str) -> list[RegistryEntry]:
    """Return all entries for a family tag."""
    rows = session.execute(
        select(TrialRegistry).where(TrialRegistry.family_tag == family_tag)
    ).scalars()
    return [_entry_from_row(row) for row in rows]


def get_by_status(session: Session, status: RegistryStatus | str) -> list[RegistryEntry]:
    """Return all entries with the given registry status."""
    status_value = status.value if isinstance(status, RegistryStatus) else status
    rows = session.execute(
        select(TrialRegistry).where(TrialRegistry.status == status_value)
    ).scalars()
    return [_entry_from_row(row) for row in rows]


def count_trials_in_family(session: Session, family_tag: str) -> int:
    """Return count of all entries in a family."""
    return int(
        session.execute(
            select(func.count())
            .select_from(TrialRegistry)
            .where(TrialRegistry.family_tag == family_tag)
        ).scalar_one()
    )


def read_functions_issue_no_writes(session: Any) -> None:
    """Exercise read functions against a guard session for no-write tests."""
    get_by_family(session, "family")
    get_by_status(session, RegistryStatus.PENDING)
    count_trials_in_family(session, "family")
