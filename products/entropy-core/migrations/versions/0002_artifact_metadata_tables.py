"""Create artifact metadata and append-only event tables.

Revision ID: 0002_artifact_metadata_tables
Revises: 0001_initial_schema
Create Date: 2026-05-14
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0002_artifact_metadata_tables"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create artifact metadata tables."""
    op.create_table(
        "artifact_records",
        sa.Column("artifact_id", sa.String(length=128), nullable=False),
        sa.Column("artifact_contract_version", sa.String(length=64), nullable=False),
        sa.Column("product", sa.String(length=128), nullable=False),
        sa.Column("source_run_id", sa.String(length=128), nullable=False),
        sa.Column("validation_status", sa.String(length=32), nullable=False),
        sa.Column("current_governance_state", sa.String(length=64), nullable=False),
        sa.Column("artifact_hash", sa.String(length=128), nullable=False),
        sa.Column("policy_config_hash", sa.String(length=128), nullable=False),
        sa.Column("code_version_ref", sa.String(length=256), nullable=False),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("artifact_id", name=op.f("pk_artifact_records")),
    )
    op.create_table(
        "artifact_validation_events",
        sa.Column("event_id", sa.String(length=128), nullable=False),
        sa.Column("artifact_id", sa.String(length=128), nullable=False),
        sa.Column("validation_status", sa.String(length=32), nullable=False),
        sa.Column("error_count", sa.Integer(), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["artifact_id"],
            ["artifact_records.artifact_id"],
            name=op.f("fk_artifact_validation_events_artifact_id_artifact_records"),
        ),
        sa.PrimaryKeyConstraint("event_id", name=op.f("pk_artifact_validation_events")),
    )
    op.create_table(
        "artifact_reproducibility_events",
        sa.Column("event_id", sa.String(length=128), nullable=False),
        sa.Column("artifact_id", sa.String(length=128), nullable=False),
        sa.Column("reproducibility_status", sa.String(length=64), nullable=False),
        sa.Column("manifest_ref", sa.Text(), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["artifact_id"],
            ["artifact_records.artifact_id"],
            name=op.f("fk_artifact_reproducibility_events_artifact_id_artifact_records"),
        ),
        sa.PrimaryKeyConstraint("event_id", name=op.f("pk_artifact_reproducibility_events")),
    )
    op.create_table(
        "artifact_evidence_packets",
        sa.Column("packet_id", sa.String(length=128), nullable=False),
        sa.Column("artifact_id", sa.String(length=128), nullable=False),
        sa.Column("packet_version", sa.String(length=64), nullable=False),
        sa.Column("packet_ref", sa.Text(), nullable=False),
        sa.Column("packet_hash", sa.String(length=128), nullable=False),
        sa.Column("approval_state", sa.String(length=64), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["artifact_id"],
            ["artifact_records.artifact_id"],
            name=op.f("fk_artifact_evidence_packets_artifact_id_artifact_records"),
        ),
        sa.PrimaryKeyConstraint("packet_id", name=op.f("pk_artifact_evidence_packets")),
    )
    op.create_table(
        "artifact_governance_transition_events",
        sa.Column("event_id", sa.String(length=128), nullable=False),
        sa.Column("artifact_id", sa.String(length=128), nullable=False),
        sa.Column("prior_state", sa.String(length=64), nullable=False),
        sa.Column("next_state", sa.String(length=64), nullable=False),
        sa.Column("approval_event_ref", sa.String(length=128), nullable=True),
        sa.Column("actor", sa.String(length=128), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["artifact_id"],
            ["artifact_records.artifact_id"],
            name=op.f("fk_artifact_governance_transition_events_artifact_id_artifact_records"),
        ),
        sa.PrimaryKeyConstraint("event_id", name=op.f("pk_artifact_governance_transition_events")),
    )


def downgrade() -> None:
    """Drop artifact metadata tables."""
    op.drop_table("artifact_governance_transition_events")
    op.drop_table("artifact_evidence_packets")
    op.drop_table("artifact_reproducibility_events")
    op.drop_table("artifact_validation_events")
    op.drop_table("artifact_records")
