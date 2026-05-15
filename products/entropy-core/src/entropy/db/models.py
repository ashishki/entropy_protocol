"""SQLAlchemy table models for Entropy Protocol persistence."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, MetaData, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Declarative base shared by migrations and DB access code."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class TrialRegistry(Base):
    """Append-only preregistered trial specification table."""

    __tablename__ = "trial_registry"

    trial_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    family_tag: Mapped[str] = mapped_column(String(128), nullable=False)
    hypothesis: Mapped[str] = mapped_column(Text, nullable=False)
    dataset_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    code_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    policy_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    parameter_lock: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class Run(Base):
    """Immutable reproducibility metadata for an evaluation run."""

    __tablename__ = "runs"

    run_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    trial_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("trial_registry.trial_id"),
        nullable=False,
    )
    dataset_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    code_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    policy_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    simbroker_version: Mapped[str] = mapped_column(String(64), nullable=False)
    is_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    oos_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    oos_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    embargo_bars: Mapped[int] = mapped_column(Integer, nullable=False)
    leakage_status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class MarketDataset(Base):
    """Immutable local market dataset provenance record."""

    __tablename__ = "market_datasets"

    dataset_hash: Mapped[str] = mapped_column(String(128), primary_key=True)
    symbol: Mapped[str] = mapped_column(String(64), nullable=False)
    timeframe: Mapped[str] = mapped_column(String(16), nullable=False)
    start_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    row_count: Mapped[int] = mapped_column(Integer, nullable=False)
    source_path: Mapped[str] = mapped_column(Text, nullable=False)
    parquet_path: Mapped[str] = mapped_column(Text, nullable=False)
    provenance: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class FillLog(Base):
    """Per-fill cost decomposition persisted for run attribution."""

    __tablename__ = "fill_logs"

    fill_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(String(128), ForeignKey("runs.run_id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    symbol: Mapped[str] = mapped_column(String(64), nullable=False)
    side: Mapped[str] = mapped_column(String(16), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(28, 10), nullable=False)
    fill_price: Mapped[Decimal] = mapped_column(Numeric(28, 10), nullable=False)
    commission: Mapped[Decimal] = mapped_column(Numeric(28, 10), nullable=False)
    slippage: Mapped[Decimal] = mapped_column(Numeric(28, 10), nullable=False)
    market_impact: Mapped[Decimal] = mapped_column(Numeric(28, 10), nullable=False)
    borrow_rate: Mapped[Decimal] = mapped_column(Numeric(28, 10), nullable=False)
    funding_rate: Mapped[Decimal] = mapped_column(Numeric(28, 10), nullable=False)
    total_cost: Mapped[Decimal] = mapped_column(Numeric(28, 10), nullable=False)
    constrained: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class GovernanceEvent(Base):
    """Append-only governance event log."""

    __tablename__ = "governance_events"

    event_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    trial_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("trial_registry.trial_id"),
        nullable=False,
    )
    event_type: Mapped[str] = mapped_column(String(32), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    actor: Mapped[str] = mapped_column(String(128), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    policy_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    prior_state: Mapped[str | None] = mapped_column(String(32), nullable=True)
    next_state: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class ArtifactRecordMetadata(Base):
    """Artifact registry metadata persisted for internal audit lookup."""

    __tablename__ = "artifact_records"

    artifact_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    artifact_contract_version: Mapped[str] = mapped_column(String(64), nullable=False)
    product: Mapped[str] = mapped_column(String(128), nullable=False)
    source_run_id: Mapped[str] = mapped_column(String(128), nullable=False)
    validation_status: Mapped[str] = mapped_column(String(32), nullable=False)
    current_governance_state: Mapped[str] = mapped_column(String(64), nullable=False)
    artifact_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    policy_config_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    code_version_ref: Mapped[str] = mapped_column(String(256), nullable=False)
    metadata_payload: Mapped[dict[str, object]] = mapped_column("metadata", JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class ArtifactValidationEvent(Base):
    """Append-only artifact validation event metadata."""

    __tablename__ = "artifact_validation_events"

    event_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    artifact_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("artifact_records.artifact_id"),
        nullable=False,
    )
    validation_status: Mapped[str] = mapped_column(String(32), nullable=False)
    error_count: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class ArtifactReproducibilityEvent(Base):
    """Append-only artifact reproducibility event metadata."""

    __tablename__ = "artifact_reproducibility_events"

    event_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    artifact_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("artifact_records.artifact_id"),
        nullable=False,
    )
    reproducibility_status: Mapped[str] = mapped_column(String(64), nullable=False)
    manifest_ref: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class ArtifactEvidencePacketMetadata(Base):
    """Artifact evidence packet metadata persisted for internal audit lookup."""

    __tablename__ = "artifact_evidence_packets"

    packet_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    artifact_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("artifact_records.artifact_id"),
        nullable=False,
    )
    packet_version: Mapped[str] = mapped_column(String(64), nullable=False)
    packet_ref: Mapped[str] = mapped_column(Text, nullable=False)
    packet_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    approval_state: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class ArtifactGovernanceTransitionMetadata(Base):
    """Append-only artifact governance transition event metadata."""

    __tablename__ = "artifact_governance_transition_events"

    event_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    artifact_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("artifact_records.artifact_id"),
        nullable=False,
    )
    prior_state: Mapped[str] = mapped_column(String(64), nullable=False)
    next_state: Mapped[str] = mapped_column(String(64), nullable=False)
    approval_event_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    actor: Mapped[str] = mapped_column(String(128), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
