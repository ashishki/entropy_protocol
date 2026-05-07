"""Trial Registry preregistration write path."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from entropy.db.models import TrialRegistry
from entropy.models.registry import RegistryStatus, TrialSpec


class RegistryWriteError(Exception):
    """Base error for Trial Registry write failures."""


class MissingHashError(RegistryWriteError):
    """Raised when a trial spec is missing required reproducibility hashes."""


class DuplicateTrialError(RegistryWriteError):
    """Raised when a trial_id already exists in the registry."""


class MissingRequiredFieldError(RegistryWriteError):
    """Raised when a required trial spec field is missing or blank."""


REQUIRED_STRING_FIELDS = (
    "trial_id",
    "family_tag",
    "hypothesis",
    "dataset_hash",
    "code_hash",
    "policy_hash",
)
HASH_FIELDS = ("dataset_hash", "code_hash", "policy_hash")


def _is_blank(value: Any) -> bool:
    """Return whether a value is absent or blank."""
    return value is None or (isinstance(value, str) and not value.strip())


def _validate_trial_spec(trial_spec: TrialSpec) -> None:
    """Validate fields that must be present before any DB write."""
    missing_fields = [
        field_name
        for field_name in REQUIRED_STRING_FIELDS
        if _is_blank(getattr(trial_spec, field_name))
    ]
    if missing_fields:
        missing_hashes = [field_name for field_name in missing_fields if field_name in HASH_FIELDS]
        if missing_hashes:
            raise MissingHashError("Missing required hash fields: " + ", ".join(missing_hashes))
        raise MissingRequiredFieldError("Missing required fields: " + ", ".join(missing_fields))


def register_trial(session: Session, trial_spec: TrialSpec) -> str:
    """Insert a validated trial spec and return its trial_id."""
    _validate_trial_spec(trial_spec)

    duplicate_trial_id = session.execute(
        select(TrialRegistry.trial_id).where(TrialRegistry.trial_id == trial_spec.trial_id)
    ).scalar_one_or_none()
    if duplicate_trial_id is not None:
        raise DuplicateTrialError("Trial already exists: " + trial_spec.trial_id)

    session.add(
        TrialRegistry(
            trial_id=trial_spec.trial_id,
            family_tag=trial_spec.family_tag,
            hypothesis=trial_spec.hypothesis,
            dataset_hash=trial_spec.dataset_hash,
            code_hash=trial_spec.code_hash,
            policy_hash=trial_spec.policy_hash,
            status=RegistryStatus.PENDING.value,
            parameter_lock=trial_spec.parameter_lock,
            registered_at=trial_spec.registered_at,
        )
    )
    session.flush()
    return trial_spec.trial_id
