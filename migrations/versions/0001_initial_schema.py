"""Create core registry and run tables.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-03
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial schema."""
    op.create_table(
        "trial_registry",
        sa.Column("trial_id", sa.String(length=128), nullable=False),
        sa.Column("family_tag", sa.String(length=128), nullable=False),
        sa.Column("hypothesis", sa.Text(), nullable=False),
        sa.Column("dataset_hash", sa.String(length=128), nullable=False),
        sa.Column("code_hash", sa.String(length=128), nullable=False),
        sa.Column("policy_hash", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("parameter_lock", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("trial_id", name=op.f("pk_trial_registry")),
    )
    op.create_table(
        "runs",
        sa.Column("run_id", sa.String(length=128), nullable=False),
        sa.Column("trial_id", sa.String(length=128), nullable=False),
        sa.Column("dataset_hash", sa.String(length=128), nullable=False),
        sa.Column("code_hash", sa.String(length=128), nullable=False),
        sa.Column("policy_hash", sa.String(length=128), nullable=False),
        sa.Column("simbroker_version", sa.String(length=64), nullable=False),
        sa.Column("is_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("oos_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("oos_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("embargo_bars", sa.Integer(), nullable=False),
        sa.Column("leakage_status", sa.String(length=32), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["trial_id"],
            ["trial_registry.trial_id"],
            name=op.f("fk_runs_trial_id_trial_registry"),
        ),
        sa.PrimaryKeyConstraint("run_id", name=op.f("pk_runs")),
    )
    op.create_table(
        "market_datasets",
        sa.Column("dataset_hash", sa.String(length=128), nullable=False),
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("timeframe", sa.String(length=16), nullable=False),
        sa.Column("start_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("row_count", sa.Integer(), nullable=False),
        sa.Column("source_path", sa.Text(), nullable=False),
        sa.Column("parquet_path", sa.Text(), nullable=False),
        sa.Column("provenance", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("dataset_hash", name=op.f("pk_market_datasets")),
    )
    op.create_table(
        "fill_logs",
        sa.Column("fill_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.String(length=128), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("side", sa.String(length=16), nullable=False),
        sa.Column("quantity", sa.Numeric(precision=28, scale=10), nullable=False),
        sa.Column("fill_price", sa.Numeric(precision=28, scale=10), nullable=False),
        sa.Column("commission", sa.Numeric(precision=28, scale=10), nullable=False),
        sa.Column("slippage", sa.Numeric(precision=28, scale=10), nullable=False),
        sa.Column("market_impact", sa.Numeric(precision=28, scale=10), nullable=False),
        sa.Column("borrow_rate", sa.Numeric(precision=28, scale=10), nullable=False),
        sa.Column("funding_rate", sa.Numeric(precision=28, scale=10), nullable=False),
        sa.Column("total_cost", sa.Numeric(precision=28, scale=10), nullable=False),
        sa.Column("constrained", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["run_id"], ["runs.run_id"], name=op.f("fk_fill_logs_run_id_runs")),
        sa.PrimaryKeyConstraint("fill_id", name=op.f("pk_fill_logs")),
    )
    op.create_table(
        "governance_events",
        sa.Column("event_id", sa.String(length=128), nullable=False),
        sa.Column("trial_id", sa.String(length=128), nullable=False),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actor", sa.String(length=128), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("policy_hash", sa.String(length=128), nullable=False),
        sa.Column("prior_state", sa.String(length=32), nullable=True),
        sa.Column("next_state", sa.String(length=32), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["trial_id"],
            ["trial_registry.trial_id"],
            name=op.f("fk_governance_events_trial_id_trial_registry"),
        ),
        sa.PrimaryKeyConstraint("event_id", name=op.f("pk_governance_events")),
    )


def downgrade() -> None:
    """Drop initial schema."""
    op.drop_table("governance_events")
    op.drop_table("fill_logs")
    op.drop_table("market_datasets")
    op.drop_table("runs")
    op.drop_table("trial_registry")
