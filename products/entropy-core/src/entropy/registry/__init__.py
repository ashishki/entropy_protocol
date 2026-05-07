"""Registry package."""

from entropy.registry.gate import ReadinessResult, ReadinessStatus, TrialNotFoundError, check
from entropy.registry.read import (
    count_trials_in_family,
    get_by_family,
    get_by_status,
    get_by_trial_id,
)
from entropy.registry.write import (
    DuplicateTrialError,
    MissingHashError,
    MissingRequiredFieldError,
    RegistryWriteError,
    register_trial,
)

__all__ = [
    "DuplicateTrialError",
    "MissingHashError",
    "MissingRequiredFieldError",
    "ReadinessResult",
    "ReadinessStatus",
    "RegistryWriteError",
    "TrialNotFoundError",
    "check",
    "count_trials_in_family",
    "get_by_family",
    "get_by_status",
    "get_by_trial_id",
    "register_trial",
]
