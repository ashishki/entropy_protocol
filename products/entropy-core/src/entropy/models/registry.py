"""Trial registry and run record domain models."""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class RegistryStatus(str, Enum):
    """Lifecycle status for a registered trial."""

    PENDING = "PENDING"
    READY = "READY"
    REJECTED = "REJECTED"


class LeakageStatus(str, Enum):
    """Leakage audit status for a run."""

    PASS = "PASS"
    FAIL = "FAIL"
    NOT_RUN = "NOT_RUN"


class FillSide(str, Enum):
    """Supported fill directions."""

    BUY = "BUY"
    SELL = "SELL"


class GovernanceEventType(str, Enum):
    """Governance event types declared by the protocol."""

    APPROVAL = "APPROVAL"
    REJECTION = "REJECTION"
    PHASE_GATE = "PHASE_GATE"
    P1_TRIP = "P1_TRIP"
    P1_RESET = "P1_RESET"
    P3_FIRE = "P3_FIRE"
    P3_CLEAR = "P3_CLEAR"


class TrialSpec(BaseModel):
    """Complete preregistration specification for a research trial."""

    trial_id: str = Field(min_length=1)
    family_tag: str = Field(min_length=1)
    hypothesis: str = Field(min_length=1)
    dataset_hash: str = Field(min_length=1)
    code_hash: str = Field(min_length=1)
    policy_hash: str = Field(min_length=1)
    parameter_lock: dict[str, Any]
    registered_at: datetime

    @field_validator(
        "trial_id",
        "family_tag",
        "hypothesis",
        "dataset_hash",
        "code_hash",
        "policy_hash",
    )
    @classmethod
    def required_strings_must_not_be_blank(cls, value: str) -> str:
        """Reject whitespace-only values for required identity/hash fields."""
        if not value.strip():
            raise ValueError("required string field must not be blank")
        return value

    @field_validator("registered_at")
    @classmethod
    def timestamp_must_be_utc(cls, value: datetime) -> datetime:
        """Require timezone-aware UTC registration timestamps."""
        if value.tzinfo is None or value.utcoffset() != timedelta(0):
            raise ValueError("registered_at must be timezone-aware UTC")
        return value


class RegistryEntry(BaseModel):
    """Trial registry row as exposed by application read paths."""

    trial: TrialSpec
    status: RegistryStatus = RegistryStatus.PENDING


class RunRecord(BaseModel):
    """Immutable metadata needed to reproduce one evaluation run."""

    trial_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    dataset_hash: str = Field(min_length=1)
    code_hash: str = Field(min_length=1)
    policy_hash: str = Field(min_length=1)
    simbroker_version: str = Field(min_length=1)
    is_start: datetime
    is_end: datetime
    oos_start: datetime
    oos_end: datetime
    embargo_bars: int = Field(default=0, ge=0)
    leakage_status: LeakageStatus

    @field_validator(
        "trial_id",
        "run_id",
        "dataset_hash",
        "code_hash",
        "policy_hash",
        "simbroker_version",
    )
    @classmethod
    def required_strings_must_not_be_blank(cls, value: str) -> str:
        """Reject whitespace-only values for required run identity fields."""
        if not value.strip():
            raise ValueError("required string field must not be blank")
        return value

    @field_validator("is_start", "is_end", "oos_start", "oos_end")
    @classmethod
    def timestamps_must_be_utc(cls, value: datetime) -> datetime:
        """Require timezone-aware UTC run window timestamps."""
        if value.tzinfo is None or value.utcoffset() != timedelta(0):
            raise ValueError("run windows must use timezone-aware UTC timestamps")
        return value

    @model_validator(mode="after")
    def validate_windows(self) -> "RunRecord":
        """Require increasing IS/OOS windows in chronological order."""
        if self.is_end <= self.is_start:
            raise ValueError("is_end must be after is_start")
        if self.oos_end <= self.oos_start:
            raise ValueError("oos_end must be after oos_start")
        if self.oos_start <= self.is_end:
            raise ValueError("oos_start must be after is_end")
        return self


class FillLog(BaseModel):
    """Per-fill execution record with explicit cost decomposition."""

    timestamp: datetime
    symbol: str = Field(min_length=1)
    side: FillSide
    quantity: Decimal = Field(gt=Decimal("0"))
    fill_price: Decimal = Field(gt=Decimal("0"))
    commission: Decimal = Field(ge=Decimal("0"))
    slippage: Decimal = Field(ge=Decimal("0"))
    market_impact: Decimal = Field(ge=Decimal("0"))
    borrow_rate: Decimal = Field(ge=Decimal("0"))
    funding_rate: Decimal = Field(ge=Decimal("0"))
    total_cost: Decimal = Field(ge=Decimal("0"))
    constrained: bool = False

    @field_validator("timestamp")
    @classmethod
    def timestamp_must_be_utc(cls, value: datetime) -> datetime:
        """Require timezone-aware UTC fill timestamps."""
        if value.tzinfo is None or value.utcoffset() != timedelta(0):
            raise ValueError("timestamp must be timezone-aware UTC")
        return value

    @field_validator("symbol")
    @classmethod
    def symbol_must_not_be_blank(cls, value: str) -> str:
        """Reject whitespace-only symbols."""
        if not value.strip():
            raise ValueError("symbol must not be blank")
        return value


class GovernanceEvent(BaseModel):
    """Append-only governance event record."""

    event_type: GovernanceEventType
    timestamp: datetime
    trial_id: str = Field(min_length=1)
    actor: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    policy_hash: str = Field(min_length=1)
    prior_state: str | None = None
    next_state: str | None = None

    @field_validator("timestamp")
    @classmethod
    def timestamp_must_be_utc(cls, value: datetime) -> datetime:
        """Require timezone-aware UTC governance timestamps."""
        if value.tzinfo is None or value.utcoffset() != timedelta(0):
            raise ValueError("timestamp must be timezone-aware UTC")
        return value

    @field_validator("trial_id", "actor", "reason", "policy_hash")
    @classmethod
    def required_strings_must_not_be_blank(cls, value: str) -> str:
        """Reject whitespace-only governance identity fields."""
        if not value.strip():
            raise ValueError("required string field must not be blank")
        return value
