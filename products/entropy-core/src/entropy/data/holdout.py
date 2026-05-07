"""Holdout access guards."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal


HoldoutLockStatus = Literal["LOCKED", "UNLOCKED"]


@dataclass(frozen=True)
class HoldoutReadRequest:
    """Holdout read request checked before any path access."""

    path: str
    lock_status: HoldoutLockStatus
    approval_id: str | None = None


@dataclass(frozen=True)
class HoldoutReadDecision:
    """Holdout read decision."""

    status: Literal["ALLOWED", "BLOCKED"]
    reason_code: str
    path: str
    approval_id: str | None = None


def authorize_holdout_read(
    request: HoldoutReadRequest,
    *,
    reader: Callable[[str], Any] | None = None,
) -> HoldoutReadDecision:
    """Check holdout lock status before opening or reading a holdout path."""
    if request.lock_status == "LOCKED":
        return HoldoutReadDecision(
            status="BLOCKED",
            reason_code="HOLDOUT_LOCKED",
            path=request.path,
        )
    if request.approval_id is None or not request.approval_id.strip():
        return HoldoutReadDecision(
            status="BLOCKED",
            reason_code="MISSING_HOLDOUT_APPROVAL",
            path=request.path,
        )
    if reader is not None:
        reader(request.path)
    return HoldoutReadDecision(
        status="ALLOWED",
        reason_code="HOLDOUT_UNLOCK_APPROVED",
        path=request.path,
        approval_id=request.approval_id,
    )
